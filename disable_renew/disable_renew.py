"""Disable EventBridge scheduler

Disables the schedule that executes the renewal of S3 credentials every 50 
minutes.
"""

# Standard imports
import logging
import sys

# Third-party imports
import boto3
import botocore

def disable_renew():
    """Disable the hourly renewal of PO.DAAC S3 credentials."""
    
    logger = get_logger()
    
    scheduler = boto3.client("scheduler")
    try:
        # Get schedule
        get_response = scheduler.get_schedule(Name="confluence-renew")
        
        # Update schedule
        update_response = scheduler.update_schedule(
            Name=get_response["Name"],
            GroupName=get_response["GroupName"],
            FlexibleTimeWindow=get_response["FlexibleTimeWindow"],
            ScheduleExpression=get_response["ScheduleExpression"],
            Target=get_response["Target"],
            State="DISABLED"
        )
        logger.info("Disabled 'renew' Lambda function.")
    except botocore.exceptions.ClientError as e:
        handle_error(e, logger)
    
def get_logger():
    """Return a formatted logger object."""
    
    # Create a Logger object and set log level
    logger = logging.getLogger(__name__)
    
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)

        # Create a handler to console and set level
        console_handler = logging.StreamHandler()

        # Create a formatter and add it to the handler
        console_format = logging.Formatter("%(asctime)s - %(module)s - %(levelname)s : %(message)s")
        console_handler.setFormatter(console_format)

        # Add handlers to logger
        logger.addHandler(console_handler)

    # Return logger
    return logger
        
def handle_error(error, logger):
    """Print out error message and exit."""
    
    logger.error("Error encountered.")
    logger.error(error)
    logger.error("System exiting.")
    sys.exit(1)
    
if __name__ == "__main__":
    disable_renew()