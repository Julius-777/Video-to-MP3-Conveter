import logging, json
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
sqs = boto3.resource('sqs')

def get_queue(name):
    """
    Gets an SQS queue by name.

    :param name: The name that was used to create the queue.
    :return: A Queue object.
    """
    try:
        queue = sqs.get_queue_by_name(QueueName=name)
        logger.info("Got queue '%s' with URL=%s", name, queue.url)
    except ClientError as error:
        logger.exception("Couldn't get queue named %s.", name)
        raise error
    else:
        return queue

def receive_message(queue):
  """
    Receive a batch of messages in a single request from an SQS queue.

    :param queue: The queue from which to receive messages.
    :return: The list of Message objects received. These each contain the body
             of the message and metadata and custom attributes.
    """
  try:
      message = queue.receive_messages(
          MessageAttributeNames=['All'],
          MaxNumberOfMessages=1,
          WaitTimeSeconds=5
      )
  except ClientError as error:
    logger.exception("Couldn't recieve message from queue: %s", queue)
    raise error
  else:
      return message

def send_message(queue, message):
    """
    Send a message to an Amazon SQS queue.

    :param queue: The queue that receives the message.
    :param message_body: The body text of the message.
    :param message_attributes: Custom attributes of the message. These are key-value
                               pairs that can be whatever you want.
    :return: The response from SQS that contains the assigned message ID.
    """
    try:
         response = queue.send_message(
            queue=queue,
            message_attributes={
                "Processed" : {
                    'StringValue': "No",
                    'DataType': 'string'
                }
            },
            message_body=json.dumps(message)
        )
    except ClientError as error:
        logger.exception("Send message failed: %s", message)
        raise error
    else:
        return response

def delete_message(message):
    """
    Delete a message from a queue. Clients must delete messages after they
    are received and processed to remove them from the queue.

    :param message: The message to delete. The message's queue URL is contained in
                    the message's metadata.
    :return: None
    """
    try:
        message.delete()
        logger.info("Deleted message: %s", message.message_id)
    except ClientError as error:
        logger.exception("Couldn't delete message: %s", message.message_id)
        raise error