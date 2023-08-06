import json
import logging
from typing import Any, Callable
import os

from google.cloud import pubsub_v1
from google.api_core.exceptions import AlreadyExists

from . import Engine

LOGGER = logging.getLogger(__name__)

ENV_PROJECT_ID = "GOOGLE_PROJECT_ID"
ENV_TOPIC_ID = "GOOGLE_TOPIC_ID"
ENV_SUBSCRIPTION = "GOOGLE_SUBSCRIPTION"
ENV_DECODER = "GOOGLE_DECODER"
DEFAULT_DECODER = "identity"

PULL_TIMEOUT = 60


def identity_decoder(raw):
    return raw.decode("utf-8")


def json_decoder(raw):
    return json.loads(raw)


def create_decoder_from_env():
    decoder = os.environ.get(ENV_DECODER, DEFAULT_DECODER)
    if decoder == "json":
        decoder = json_decoder
    else:
        decoder = identity_decoder
    return decoder


class GooglePubSub(Engine):
    """Synchronous engine based on google pub/sub.

    Requires GOOGLE_APPLICATION_CREDENTIALS to be set in the environment
    """

    def __init__(
        self,
        project_id: str,
        topic_id: str,
        subscription: str,
        *,
        decoder: Callable[[bytes], Any] = lambda x: x,
    ):
        self.subscriber = pubsub_v1.SubscriberClient()
        self.subscription_path = self.subscriber.subscription_path(
            project_id, subscription
        )
        self.decoder = decoder
        topic_path = self.subscriber.topic_path(project_id, topic_id)
        # create the subscription
        try:
            self.subscriber.create_subscription(self.subscription_path, topic_path)
        except AlreadyExists as e:
            LOGGER.error(e)

    @classmethod
    def from_env(cls):
        project_id = os.environ.get(ENV_PROJECT_ID, None)
        if project_id is None:
            raise ValueError(f"{ENV_PROJECT_ID} must be set")

        topic_id = os.environ.get(ENV_TOPIC_ID, None)
        if topic_id is None:
            raise ValueError(f"{ENV_TOPIC_ID} must be set")

        subscription = os.environ.get(ENV_SUBSCRIPTION, None)
        if subscription is None:
            raise ValueError(f"{ENV_SUBSCRIPTION} must be set")

        decoder = create_decoder_from_env()
        return cls(project_id, topic_id, subscription, decoder=decoder)

    def next(self):
        response = self.subscriber.pull(
            self.subscription_path, max_messages=1, timeout=PULL_TIMEOUT
        )
        for msg in response.received_messages:
            self.current_msg = msg
            return self.decoder(msg.message.data)

    def ack(self, param):
        self.subscriber.acknowledge(self.subscription_path, [self.current_msg.ack_id])

    def nack(self, param):
        # semantic here => redeliver message
        self.subscriber.modify_ack_deadline(
            self.subscription_path, [self.current_msg.ack_id], 0
        )
