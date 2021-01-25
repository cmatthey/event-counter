import json
from datetime import datetime, timezone

from src.event_data import EventData
from src.validate_input import validate_input


class EventCounter:
    """
    A small library which helps to track the number of events that happened during a specified window of time
    """

    def __init__(self, event_data: EventData):
        """

        Args:
            event_data: EventData event data of type EventData to store events
        """
        self.event_data = event_data

    @validate_input
    def signal_event(self, event):
        """
        Receive single when an event happened and store it in EventData

        Args:
            event: dict a json a like object in Python's dict format with some payload

        Returns: None

        """
        self.event_data.put_event(event=event)

    def get_event_count_by_duration_window(self, secs=1):
        """
        Return the number of events that happened over a user-specified amount of time until the current time

        Args:
            secs: int duration in seconds until the current time

        Returns: int the number of events in over a user-specified amount of time until the current time

        """
        count = 0
        current_timestamp_in_sec = int(datetime.now(tz=timezone.utc).timestamp())  # Current timestamp
        earliest_timestamp_in_sec = current_timestamp_in_sec - secs  # The earliest timestamp to fetch event counts from
        event_counts_by_timestamp_map = self.event_data.get_event_counts()  # Get count records indexed by timestamp
        # Interate through the key of timestamp from current to early chronologically and total up the counter for the given window
        keys = sorted(list(event_counts_by_timestamp_map.keys()), reverse=True)
        for k in keys:
            # If the events happened to far in the past, stop counting.
            if k < earliest_timestamp_in_sec:
                break
            count += event_counts_by_timestamp_map[k]
        return json.dumps({"count": count, "request": {"secs_from_now": secs, "request_timestamp_in_sec": current_timestamp_in_sec}})
