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