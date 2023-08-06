import os
import logging
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.types import ExpirationPolicy
from google.api_core import exceptions as google_exceptions
from pubsub_utils.topic.base import TopicClient
from pubsub_utils.errors import SubscriberError
from concurrent.futures import TimeoutError


logging.basicConfig(level=logging.INFO)
# TODO: Test to figure out apt value in dev and make it configurable
# PUB SUB MESSAGE ACK DEADLINE
ACK_DEADLINE = 300


class Subscriber:
    def __init__(self):

        self.client = pubsub_v1.SubscriberClient()
        self.project = os.environ.get("GOOGLE_CLOUD_PROJECT")
        # Limit the subscriber to only have 20 outstanding messages at a time.
        self.flow_control = pubsub_v1.types.FlowControl(max_messages=20)
        self.params = {}

    def process_message(self, message):
        """
        Call back function to process/perform differnt operations on the message 
        based on specific task/app
        """
        raise NotImplmentedError("Subclasses should implement this!")

    def receive_message(self, sub_name, topic_name):
        """
        Receive messages from the given subscription
        """

        subscription_path = self.client.subscription_path(self.project, sub_name)
        # Returns a StreamingPullFuture a background thread to receive messages asynchronously
        subs = True
        while subs:
            try:
                processing_thread = self.client.subscribe(
                    subscription_path, self.process_message, self.flow_control
                )
                # Wait for an exception in processing thread if NotFound create subscription-name
                error = processing_thread.exception(timeout=2)
                if isinstance(error, google_exceptions.NotFound):
                    logging.info(f"Subscription {sub_name} Not Found")
                    self.create_subscription(sub_name, topic_name)

            except TimeoutError:
                logging.info(f"Starting processing thread for {sub_name}")
                subs = False
            except Exception as error:
                subs = False
                raise SubscriberError(
                    {"processing_thread error": error, "sub_name": sub_name}
                )

    def create_subscription(self, sub_name, topic_name):
        """
        Create a new pull subscription on the given topic.
        """
        create_subs = True
        while create_subs:
            try:
                topic_path = self.client.topic_path(self.project, topic_name)
                subscription_path = self.client.subscription_path(
                    self.project, sub_name
                )
                subscription = self.client.create_subscription(
                    name=subscription_path,
                    topic=topic_path,
                    ack_deadline_seconds=ACK_DEADLINE,
                    expiration_policy=ExpirationPolicy(),
                )
                logging.info(f"Subscription created: {subscription}")
                create_subs = False
            # Create Topic if it does not exist
            except google_exceptions.NotFound as error:
                logging.info(f"Topic {topic_name} Not found Creating it")
                tp = TopicClient()
                tp.create_topic(topic_name)
            except Exception as error:
                create_subs = False
                raise SubscriberError(
                    {"msg": "create_subscription_error", "error": error}
                )

