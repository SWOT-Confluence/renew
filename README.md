# renew

Retrieves S3 credentials from S3 endpoint and stores them in AWS SSM Parameter
Store.

This can be run every 50 minutes in order to renew credentials during an 
execution of Confluence.

## aws infrastructure

The renew program includes the following AWS services:
- Lambda function to execute code deployed via zip file.
- IAM role and policy for Lambda function execution.
- EventBridge schedule to run Lambda function every 50 minutes.
- IAM role and policy for EventBridge schedule execution.
- Permissions that allow EventBridge to invoke the Lambda function.

## terraform 

Deploys AWS infrastructure and stores state in an S3 backend using a DynamoDB table for locking.

To deploy:
1. Edit `terraform.tfvars` for environment to deploy to.
3. Initialize terraform: `terraform init`
4. Plan terraform modifications: `terraform plan -out=tfplan`
5. Apply terraform modifications: `terraform apply tfplan`

# disable renew

Disables renew Lambda function so that it no longer runs every 50 minutes to
retrieves and stores temporary S3 credentials.

This is a docker container meant to be run as an AWS Batch job after the input
module.

## installation

Build a Docker image: `docker build -t disable_renew .`

## execution

AWS credentials will need to be passed as environment variables to the container so that `renew` may access AWS infrastructure to generate JSON files.

```
# Credentials
export aws_key=XXXXXXXXXXXXXX
export aws_secret=XXXXXXXXXXXXXXXXXXXXXXXXXX

# Docker run command
docker run --rm --name disable_renew -e AWS_ACCESS_KEY_ID=$aws_key -e AWS_SECRET_ACCESS_KEY=$aws_secret -e AWS_DEFAULT_REGION=us-west-2 diable_renew:latest
```