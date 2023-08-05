import json
import base64
from flask import request
from google.cloud import pubsub_v1


class AbstractMessage:
    def __init__(self):
        self.payload = self.attributes = self.message_id = self.json = None

    def _parse_payload_to_json(self):
        try:
            self.json = json.loads(self.payload)
        except json.JSONDecodeError:
            self.json = None


class PushMessage(AbstractMessage):
    def __init__(self):
        try:
            super().__init__()
            envelope = json.loads(request.data.decode("utf-8"))
            self.message_id = envelope["message"]["messageId"]
            self.attributes = envelope["message"].get("attributes")
            self.payload = base64.b64decode(envelope["message"]["data"])
            self._parse_payload_to_json()
            self.subscription = envelope["subscription"]
        except Exception as e:
            raise MessageInitialError(f'{e.__class__.__name__}: {e}')


class PullMessage(AbstractMessage):
    def __init__(self, received_message: pubsub_v1.types.ReceivedMessage):
        try:
            super().__init__()
            self.message_id = received_message.message.message_id
            self.attributes = received_message.message.attributes
            self.payload = received_message.message.data.decode("utf-8")
            self._parse_payload_to_json()
            self.ack_id = received_message.ack_id
        except Exception as e:
            raise MessageInitialError(f'{e.__class__.__name__}: {e}')


class Message(AbstractMessage):
    def __init__(self, payload=None, attributes=None):
        try:
            super().__init__()
            self.payload = payload
            self.attributes = attributes
            self._parse_payload_to_json()
        except Exception as e:
            raise MessageInitialError(f'{e.__class__.__name__}: {e}')


class MessageInitialError(Exception):
    pass
