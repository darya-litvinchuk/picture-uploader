import boto3
from botocore.exceptions import ClientError

from api import get_settings, logger
from api.domain.interfaces.services.subscription import ICloudSubscriptionService
from api.exceptions import LogicalException


class AWSSubscriptionService(ICloudSubscriptionService):

    def _sns_client(self):
        return boto3.client(
            "sns",
            region_name=self._region,
            aws_access_key_id=self._access_key_id,
            aws_secret_access_key=self._access_key,
        )

    def _topic_arn(self):
        topic_name = get_settings().subscription.sns_topic_name
        return self._sns.create_topic(Name=topic_name)["TopicArn"]

    def _sqs_client(self):
        return boto3.client(
            "sqs",
            region_name=self._region,
            aws_access_key_id=self._access_key_id,
            aws_secret_access_key=self._access_key,
        )

    def _queue_url(self):
        queue_name = get_settings().subscription.sqs_queue_name
        return self._sqs.create_queue(QueueName=queue_name)["QueueUrl"]

    def __init__(self):
        self._region = get_settings().aws_credentials.region_name
        self._access_key = get_settings().aws_credentials.aws_secret_access_key
        self._access_key_id = get_settings().aws_credentials.aws_access_key_id

        self._sns = self._sns_client()
        self._sns_topic_arn = self._topic_arn()

        self._sqs = self._sqs_client()
        self._sqs_queue_url = self._queue_url()

    def subscribe(self, email: str) -> str:
        try:
            subscription = self._sns.subscribe(
                TopicArn=self._sns_topic_arn,
                Protocol="email",
                Endpoint=email,
                ReturnSubscriptionArn=True
            )
            logger.debug(f"User {email} was subscribed on the {self._sns_topic_arn}")
        except ClientError:
            error_msg = f"Could't subscribe user {email} on the {self._sns_topic_arn}"
            logger.error(error_msg)
            raise LogicalException(error_msg)
        return subscription["SubscriptionArn"]

    def unsubscribe(self, subscription_arn: str) -> None:
        try:
            self._sns.unsubscribe(SubscriptionArn=subscription_arn)
            logger.debug(f"User was unsubscribed from the {subscription_arn}")
        except ClientError:
            error_msg = f"Could't unsubscribe user from the {subscription_arn}"
            logger.error(error_msg)
            raise LogicalException(error_msg)

    def message_to_queue(self, message: str) -> None:
        try:
            self._sqs.send_message(QueueUrl=self._sqs_queue_url, MessageBody=message)
            logger.debug(f"Sent message {message} to the {self._sqs_queue_url}")
        except ClientError:
            error_msg = f"Could't send message {message} to the {self._sqs_queue_url}"
            logger.error(error_msg)
            raise LogicalException(error_msg)

    def message_to_topic(self):
        response = self._sqs.receive_message(
            QueueUrl=self._sqs_queue_url,
            MaxNumberOfMessages=10,
        )

        try:
            messages = response["Messages"]
        except KeyError:
            logger.warning("No messages")
            return

        entries = []
        for message in messages:
            entries.append(
                {
                    "Id": message["MessageId"],
                    "ReceiptHandle": message["ReceiptHandle"]
                }
            )
            self._sns.publish(TopicArn=self._sns_topic_arn, Message=message["Body"])
            logger.warning(f"Published message {message}")

        self._sqs.delete_message_batch(QueueUrl=self._sqs_queue_url, Entries=entries)
