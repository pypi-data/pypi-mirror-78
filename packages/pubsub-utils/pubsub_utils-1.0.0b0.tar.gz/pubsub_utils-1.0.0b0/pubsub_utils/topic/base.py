import os
import logging
from google.cloud import pubsub_v1
from google.api_core import exceptions as google_exceptions
from pubsub_utils.errors import TopicError


logging.basicConfig(level=logging.INFO)


class TopicClient:
    """
    Class to create,list,delete publisher topics in Google Cloud
    """

    def __init__(self):
        self.client = pubsub_v1.PublisherClient()
        self.project = os.environ.get("GOOGLE_CLOUD_PROJECT")

    def get_topic(self, topic_name):
        """
        Get a Pub/Sub Topic and return a topic name as string
        """
        topic = None
        try:
            topic_path = self.client.topic_path(self.project, topic_name)
            topic = self.client.get_topic(topic_path).name
            logging.info(f"Get Topic: {topic}")
        except Exception as error:
            raise TopicError({"msg": "pubsub get_topic error", "error": error})

        return topic

    def get_topics(self):
        """
        Returns a list of all Pub/Sub topics in the given project
        """
        topics = []
        try:
            project_path = self.client.project_path(self.project)
            topics = [topic.name for topic in self.client.list_topics(project_path)]
            logging.info(f"Topics list: {topics}")
        except Exception as error:
            raise TopicError({"msg": "pubsub get_topics error", "error": error})

        return topics

    def get_subscriptions(self, topic_name):
        """
        Returns a list of subscriptions associated to a topic name
        """
        subs = []
        try:
            topic_path = self.client.topic_path(self.project, topic_name)
            subs = [sub for sub in self.client.list_topic_subscriptions(topic_path)]
            logging.info(f"Subscriptions for topic {topic_name}: {subs}")
        except google_exceptions.NotFound as error:
            raise TopicError(
                {
                    "msg": "pubsub get_subscriptions error",
                    "error": f"Topic {topic_name} Not found",
                }
            )
        except Exception as error:
            raise TopicError({"msg": "pubsub get_subscriptions error", "error": error})

        return subs

    def delete_topic(self, topic_name):
        """
        Deletes the Pub/Sub topic with the given name if there are no subscriptions mapped to it
        """
        try:

            topic_path = self.client.topic_path(self.project, topic_name)
            subs = self.get_subscriptions(topic_name)
            if not subs:
                self.client.delete_topic(topic_path)
                logging.info(f"Topic deleted: {topic_name}")
            else:
                raise Exception(f"Topic has associated subscriptions: {subs}")

        except Exception as error:
            raise TopicError({"msg": "pubsub delete_topic error", "error": error})

    def create_topic(self, topic_name):
        """
        Create a new Pub/Sub topic.
        Params: Topic name as a string
        """
        try:
            topic_path = self.client.topic_path(self.project, topic_name)
            topic = self.client.create_topic(topic_path)
            logging.info(f"Topic created: {topic.name}")
        except Exception as error:
            raise TopicError({"msg": "pubsub create_topic error", "error": error})

    def create_topics(self, topic_list):
        """
        Create Multiple Pub/Sub topics
        params: List of topics to be created 
        """
        for topic in topic_list:
            self.create_topic(topic)

