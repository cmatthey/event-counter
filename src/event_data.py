from bisect import bisect
from collections import deque, defaultdict
from datetime import datetime, timezone
import logging

from src.constants import MAX_EVENT_COUNT_STORED_LENGTH
from src.validate_input import validate_input

logger = logging.getLogger(__name__)

class EventData:
    _instance = None
    maxsize = MAX_EVENT_COUNT_STORED_LENGTH
    queue = deque()
    map = defaultdict(int)

    def __init__(self):
        raise RuntimeError('Please call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            logger.info("Creating a new EventData instance")
            cls._instance = cls.__new__(cls)
        return cls._instance

    @validate_input
    def put_event(self, event):
        current_timestamp_in_sec = int(datetime.now(tz=timezone.utc).timestamp())
        if not self.queue:
            self.queue.append(current_timestamp_in_sec)
        elif current_timestamp_in_sec not in self.queue:
            if current_timestamp_in_sec > self.queue[-1]:
                self.queue.append(current_timestamp_in_sec)
            else:
                # Handle the case when timestamp is out of sync
                bisect.insort(self.queue, current_timestamp_in_sec)
        self.map[current_timestamp_in_sec] += 1
        if len(self.queue) > self.maxsize:
            expired = self.queue.popleft()
            del self.map[expired]

    def get_event_counts(self):
        return self.map


