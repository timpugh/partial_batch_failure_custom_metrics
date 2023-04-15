import os
import boto3
import logging
import traceback
import json
import sys
import random
import string

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

sqs_client = boto3.client('sqs')

queue_url = os.environ.get('SqsQueueUrl')

def lambda_handler(event, context):

    try:
        for i in range(1):
            entries = []
            for j in range(10):
                #Give the message a random body. This helps identify specific messages by making the messages unique
                random_string = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
                random_message = {'Id':random_string, 'MessageBody': random_string}
                entries.append(random_message)
                
            #Ship a batch of 10 messages to our queue
            sent_message = sqs_client.send_message_batch(QueueUrl=queue_url, Entries=entries)

        return {'statusCode': 200,'body': 'Successfully published data!'}

    except Exception as exp:
        exception_type, exception_value, exception_traceback = sys.exc_info()

        traceback_string = traceback.format_exception(exception_type, exception_value, exception_traceback)

        err_msg = json.dumps({"errorType": exception_type.__name__, "errorMessage": str(exception_value), "stackTrace": traceback_string, "event": event})

        logger.error(err_msg)

        raise