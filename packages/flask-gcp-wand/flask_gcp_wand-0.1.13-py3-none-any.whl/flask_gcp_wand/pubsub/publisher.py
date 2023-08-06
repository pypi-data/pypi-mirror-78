import os
from google.cloud import pubsub_v1
from ..consts.pubsub import PUBLISH_TIMEOUT_SEC
from ..model.message import AbstractMessage


_gcp_publisher_client = None


class Publisher:
    def __init__(self, project_id=None, timeout=PUBLISH_TIMEOUT_SEC):
        if project_id:
            self.project_id = project_id
        else:
            self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("Empty project_id")

        self._futures = []
        self._timeout = timeout

    def publish(
        self,
        topic: str,
        message: AbstractMessage = None,
        data: str = None,
        **kwargs,
    ):
        global _gcp_publisher_client
        if _gcp_publisher_client is None:
            _gcp_publisher_client = pubsub_v1.PublisherClient()

        topic_path = _gcp_publisher_client.topic_path(self.project_id, topic)
        if message:
            data = message.payload
            if message.attributes:
                for k, v in message.attributes:
                    kwargs[k] = v
        future = _gcp_publisher_client.publish(
            topic_path, data.encode("utf-8"), **kwargs
        )
        self._futures.append(
            {
                "future": future,
                "info": {"topic": topic, "data": data, "attrs": kwargs},
            }
        )

    def wait_publish_results(self):
        results = []
        errors = []
        for f in self._futures:
            try:
                results.append(f["future"].result(self._timeout))
            except Exception as e:
                errors.append(
                    f"Failed publish {f['info']} '"
                    f"by {e.__class__.__name__}: {e}"
                )
        self._futures = []
        if errors:
            raise PublisherError("\n".join(errors))
        return results

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.wait_publish_results()


class PublisherError(Exception):
    pass
