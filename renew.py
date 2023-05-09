"""AWS Lambda that renews S3 credentials from PO.DAAC.

Retrieves S3 credentials from S3 endpoint and stores them in AWS SSM Parameter
Store.
"""

# Standard imports
import base64
import json
import sys

# Third-party imports
import boto3
import botocore
import requests

# Constants
S3_ENDPOINT = "https://archive.podaac.earthdata.nasa.gov/s3credentials"

def handler(event, context):
    """Handles error events delivered from EventBridge."""
    
    ssm_key = event["ssm_key"]
    
    username, password = get_edl()
    try:
        get_s3_creds(username, password, ssm_key)
    except botocore.exceptions.ClientError as e:
        print("Error encountered.")
        print(e)
        print("System exiting.")
        sys.exit(1)

def get_edl():
    """Return Eartdata login credentials"""
    
    try:
        ssm_client = boto3.client('ssm', region_name="us-west-2")
        username = ssm_client.get_parameter(Name="edl_username", WithDecryption=True)["Parameter"]["Value"]
        password = ssm_client.get_parameter(Name="edl_password", WithDecryption=True)["Parameter"]["Value"]
        print("Obtained EDL username and password.")
    except botocore.exceptions.ClientError as e:
        raise e
    else:
        return username, password    
        
def get_s3_creds(edl_username, edl_password, key_id):
    """Retreive S3 credentials from endpoint, write to SSM parameter store
    and return them."""
    
    s3_creds = get_creds(edl_username, edl_password)

    ssm_client = boto3.client('ssm', region_name="us-west-2")
    try:
        response = ssm_client.put_parameter(
            Name="s3_creds_key",
            Description="Temporary SWOT S3 bucket key",
            Value=s3_creds["accessKeyId"],
            Type="SecureString",
            KeyId=key_id,
            Overwrite=True,
            Tier="Standard"
        )
        response = ssm_client.put_parameter(
            Name="s3_creds_secret",
            Description="Temporary SWOT S3 bucket secret",
            Value=s3_creds["secretAccessKey"],
            Type="SecureString",
            KeyId=key_id,
            Overwrite=True,
            Tier="Standard"
        )
        response = ssm_client.put_parameter(
            Name="s3_creds_token",
            Description="Temporary SWOT S3 bucket token",
            Value=s3_creds["sessionToken"],
            Type="SecureString",
            KeyId=key_id,
            Overwrite=True,
            Tier="Standard"
        )
        response = ssm_client.put_parameter(
            Name="s3_creds_expiration",
            Description="Temporary SWOT S3 bucket expiration",
            Value=s3_creds["expiration"],
            Type="SecureString",
            KeyId=key_id,
            Overwrite=True,
            Tier="Standard"
        )
        print("Stored temporary S3 credentials in Parameter Store.")
        print(f"S3 credentials expire: {s3_creds['expiration']}")
    except botocore.exceptions.ClientError as e:
        raise e
    else:
        return s3_creds
    
def get_creds(edl_username, edl_password):
    """Request and return temporary S3 credentials.
    
    Taken from: https://archive.podaac.earthdata.nasa.gov/s3credentialsREADME
    """
    
    login = requests.get(
        S3_ENDPOINT, allow_redirects=False
    )
    login.raise_for_status()

    auth = f"{edl_username}:{edl_password}"
    encoded_auth  = base64.b64encode(auth.encode('ascii'))

    auth_redirect = requests.post(
        login.headers['location'],
        data = {"credentials": encoded_auth},
        headers= { "Origin": S3_ENDPOINT },
        allow_redirects=False
    )
    auth_redirect.raise_for_status()
    final = requests.get(auth_redirect.headers['location'], allow_redirects=False)
    results = requests.get(S3_ENDPOINT, cookies={'accessToken': final.cookies['accessToken']})
    results.raise_for_status()
    return json.loads(results.content)