import os
import logging
from google.cloud import pubsub_v1
from google.api_core import exceptions as google_exceptions
from pubsub_utils.errors import PublisherError
from pubsub_utils.topic.base import TopicClient


logging.basicConfig(level=logging.INFO)


class Publisher:
    """
    Publisher Base class to instatiate Google Pub/Sub client and 
    publish message to the pub/sub topic
    
    """

    def __init__(self):
        self.client = pubsub_v1.PublisherClient()
        self.project = os.environ.get("GOOGLE_CLOUD_PROJECT")

    def publish_data(self, topic, data):
        """
        Publish message to a Pub/Sub topic & creates a topic if it doesnot exist
        Params:
        topic (str): topic name 
        data(bytes): data in bytes to be published
        Returns:
        status (int) : status value 
        """
        status = 400
        publish = True
        while publish:
            try:
                topic_path = self.client.topic_path(self.project, topic)
                # publish a message and returns a future response
                response = self.client.publish(topic_path, data=data)
                msg_id = response.result()
                logging.info({"publish_status": True, "topic": topic, "msg_id": msg_id})
                status = 200
                publish = False
            # Create Topic if it does not exist
            except google_exceptions.NotFound:
                logging.info(f"Topic {topic} Not found Creating it")
                tp = TopicClient()
                tp.create_topic(topic)
            except Exception as e:
                raise PublisherError(
                    {
                        "publish_status": False,
                        "publisher_error": e,
                        "topic": topic,
                        "data": data,
                    }
                )

        return status

