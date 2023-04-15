import boto3
import logging
import traceback
import json
import sys
import os

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

cloudwatch = boto3.client('cloudwatch')

def lambda_handler(event, context):

    records = event.get("Records")

    batchItemFailures = []
    SQSBatchResponse = {}
    
    for record in records:
        try:
            # Process your message as normal
            message = record["body"]

        except Exception as exp:
            exception_type, exception_value, exception_traceback = sys.exc_info()

            traceback_string = traceback.format_exception(exception_type, exception_value, exception_traceback)

            err_msg = json.dumps({"errorType": exception_type.__name__, "errorMessage": str(exception_value), "stackTrace": traceback_string, "event": event})

            logger.error(err_msg)

            batchItemFailures.append({"itemIdentifier": record['messageId']})

            # If you're using batchItemFailures do not raise an exception here else we won't loop through the entire batch! Simply log the error and continue on looping, we'll report the batch on line 39
            # raise

    #Report the custom metrics before returning
    cloudwatch.put_metric_data(
        MetricData=[
            {
                'MetricName': 'BATCH_ITEM_FAILURES',
                'Dimensions': [
                    {
                        'Name': 'NUMBER_OF_MESSAGES',
                        'Value': 'COUNT'
                    },
                ],
                'Unit': 'None',
                'Value': len(batchItemFailures)
            },
        ],
        Namespace='EXAMPLE/BATCH_ITEM_FAILURES'
    )

    SQSBatchResponse["batchItemFailures"] = batchItemFailures
    return SQSBatchResponse