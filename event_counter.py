import bisect
from collections import deque, defaultdict
from datetime import datetime, timezone
from time import sleep


# TODO: decorator
# TODO: log

class EventCounter:
    def __init__(self, maxsize=300):
        self.maxsize = maxsize
        self.queue = deque()
        self.map = defaultdict(int)

    def putEvent(self, event):
        self.sanitizeInput(event)
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

    def getEventCountByTime(self, secs=1):
        count = 0
        current_timestamp_in_sec = int(datetime.now(tz=timezone.utc).timestamp())
        earliest_timestamp_in_sec = current_timestamp_in_sec - secs
        for i in range(len(self.queue) - 1, -1, -1):
            if self.queue[i] < earliest_timestamp_in_sec:
                break
            count += self.map[self.queue[i]]
        return count

    def sanitizeInput(self, event):
        """Not implemented"""
        pass


if __name__ == '__main__':
    event = {"payload": {}}
    e = EventCounter()
    for i in range(3):
        e.putEvent(event)
        sleep(1)
    count = e.getEventCountByTime(secs=4)
    print(count)
