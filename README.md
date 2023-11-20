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

## deployment

There is a script to deploy the Docker container image and Terraform AWS infrastructure found in the `deploy` directory.

Script to deploy Terraform and Docker image AWS infrastructure

REQUIRES:

- jq (<https://jqlang.github.io/jq/>)
- docker (<https://docs.docker.com/desktop/>) > version Docker 1.5
- AWS CLI (<https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html>)
- Terraform (<https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli>)

Command line arguments:

[1] registry: Registry URI
[2] repository: Name of repository to create
[3] prefix: Prefix to use for AWS resources associated with environment deploying to
[4] s3_state_bucket: Name of the S3 bucket to store Terraform state in (no need for s3:// prefix)
[5] profile: Name of profile used to authenticate AWS CLI commands

Example usage: ``./deploy.sh "account-id.dkr.ecr.region.amazonaws.com" "container-image-name" "prefix-for-environment" "s3-state-bucket-name" "confluence-named-profile"`