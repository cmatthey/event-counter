import logging
from bisect import bisect
from collections import deque, defaultdict
from datetime import datetime, timezone

from src.constants import MAX_EVENT_COUNT_STORED_LENGTH
from src.event_counter_errors import INSERT_EVENT_FAILED, SUCCESS
from src.validate_input import validate_input

logger = logging.getLogger(__name__)


class EventData:
    """
    A singleton class to store the events in a given duration defined by maxsize. Older events will be purged.
    Events are indexed by timestamp.
    """
    _instance = None
    maxsize = MAX_EVENT_COUNT_STORED_LENGTH # Max size to keep the event records
    queue = deque() # Store event timestamp by chronological order incremented by 1
    map = defaultdict(int)  # Store events by timestamp

    def __init__(self):
        raise RuntimeError('Please call instance() instead') # Enforce singleton

    @classmethod
    def instance(cls):
        if cls._instance is None: # Enforce singleton
            logger.info("Creating a new EventData instance")
            cls._instance = cls.__new__(cls)
        return cls._instance

    @validate_input
    def put_event(self, event):
        """
        Insert events into self.map and prune oldest events if they exceed the size limit.

        Args:
            event: dict event to be tracked. Its integrity is validated by validate_input

        Returns:

        """
        try:
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
                return {"error_code": SUCCESS["code"], "error_message": SUCCESS["message"]}
        except Exception:
            return {"error_code": INSERT_EVENT_FAILED["code"], "error_message": INSERT_EVENT_FAILED["message"]}

    def get_event_counts(self):
        """
        Return event records, a hashmap indexed by timestamp

        Returns: dict Event records, a hashmap indexed by timestamp

        """
        return self.map
