import logging
import time

from src.constants import MAX_EVENT_COUNT_STORED_LENGTH
from src.event_counter import EventCounter
from src.event_data import EventData

logger = logging.getLogger(__name__)


def test_put_event():
    expected_count = 3
    event = {"payload": {}}
    ec = EventCounter(event_data=EventData.instance())
    existing_count = ec.get_event_count_by_time(secs=MAX_EVENT_COUNT_STORED_LENGTH)
    for i in range(3):
        ec.put_event(event=event)
    count = ec.get_event_count_by_time(secs=MAX_EVENT_COUNT_STORED_LENGTH)
    assert count - existing_count == expected_count


def test_put_event_invalid_input():
    expected_count = 1
    event = {"invalid payload": {}}
    ec = EventCounter(EventData.instance())
    existing_count = ec.get_event_count_by_time(secs=MAX_EVENT_COUNT_STORED_LENGTH)
    ec.put_event(event=event)
    count = ec.get_event_count_by_time(secs=MAX_EVENT_COUNT_STORED_LENGTH)
    assert count - existing_count == expected_count


def test_get_event_count_by_time():
    expected_counts = [1, 2, 3]
    event = {"payload": {}}
    ec = EventCounter(EventData.instance())
    for i in range(3):
        time.sleep(1)
        ec.put_event(event)
    for i in range(3):
        count = ec.get_event_count_by_time(secs=i)
        assert count == expected_counts[i]
