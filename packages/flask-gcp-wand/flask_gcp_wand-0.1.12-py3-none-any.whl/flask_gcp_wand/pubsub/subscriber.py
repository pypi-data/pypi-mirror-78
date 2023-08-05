from google.cloud import pubsub_v1
import time
from collections import Counter
from ..consts.pubsub import PULL_MAX
from ..model.message import PullMessage


class Subscriber:
    def __init__(
        self,
        subscription_path,
        once_pull_num=PULL_MAX,
        ack_limit_sec=None,
        client=None,
    ):
        if client:
            self._client = client
        else:
            self._client = pubsub_v1.SubscriberClient()
        self.subscription_path = subscription_path
        self._once_pull_num = int(once_pull_num)
        if self._once_pull_num <= 0:
            raise ValueError(f"Invalid once_pull_num {once_pull_num}")
        self._ack_limit_sec = ack_limit_sec

        self._messages = None
        self._pool_ack_ids = []
        self._last_pull_unix_time = None
        self.accumulate_count = Counter()

    def pull(self, immediately=True):
        self._last_pull_unix_time = time.time()

        self._messages = self._client.pull(
            self.subscription_path,
            self._once_pull_num,
            return_immediately=immediately,
        )
        pull_message_num = len(self._messages.received_messages)
        self.accumulate_count["pull"] += pull_message_num
        return pull_message_num

    def pull_gen(self, immediately=True, auto_ack=True):
        while self.pull(immediately) > 0:
            for message in self._messages.received_messages:
                self.accumulate_count["yield"] += 1
                yield PullMessage(message)
                if (
                    self._ack_limit_sec
                    and self._ack_limit_sec < self._how_long_from_last_pull()
                ):
                    break
            if auto_ack:
                self.ack_exec()

    def _how_long_from_last_pull(self):
        return time.time() - self._last_pull_unix_time

    def ack_pool(self, item):
        if isinstance(item, PullMessage):
            ack_id = item.ack_id
        elif isinstance(item, (list, tuple, dict)):
            for v in item:
                self.ack_pool(v)
            return
        else:
            ack_id = str(item)
        if ack_id:
            self._pool_ack_ids.append(ack_id)

    def ack_exec(self):
        ack_num = len(self._pool_ack_ids)
        if ack_num > 0:
            self._client.acknowledge(
                self.subscription_path, self._pool_ack_ids
            )
            self.accumulate_count["ack"] += ack_num
            self._pool_ack_ids = []
        return ack_num
