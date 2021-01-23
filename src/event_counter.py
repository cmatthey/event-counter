from datetime import datetime, timezone


class EventCounter:
    def __init__(self, event_data):
        self.event_data = event_data

    def put_event(self, event):
        self.event_data.put_event(event=event)

    def get_event_count_by_time(self, secs=1):
        count = 0
        current_timestamp_in_sec = int(datetime.now(tz=timezone.utc).timestamp())
        earliest_timestamp_in_sec = current_timestamp_in_sec - secs
        event_counts_by_timestamp_map = self.event_data.get_event_counts()
        keys = sorted(list(event_counts_by_timestamp_map.keys()), reverse=True)
        for k in keys:
            if k < earliest_timestamp_in_sec:
                break
            count += event_counts_by_timestamp_map[k]
        return count
