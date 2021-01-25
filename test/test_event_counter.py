import json
import logging
import time

from src.constants import MAX_EVENT_COUNT_STORED_LENGTH
from src.event_counter import EventCounter
from src.event_data import EventData

logger = logging.getLogger(__name__)

"""
Few basic positive test cases to assure two main features: signal events and get event counts work properly
"""


def test_put_event():
    """
    Validate signal a small set of events
    """
    expected_count = 3
    event = {"payload": {}}
    ec = EventCounter(event_data=EventData.instance())
    existing_count = json.loads(ec.get_event_count_by_duration_window(secs=MAX_EVENT_COUNT_STORED_LENGTH))["count"]
    for i in range(3):
        ec.signal_event(event=event)
    count = json.loads(ec.get_event_count_by_duration_window(secs=MAX_EVENT_COUNT_STORED_LENGTH))["count"]
    assert count - existing_count == expected_count


def test_put_event_invalid_input():
    """
    Validate an invalid event
    """
    expected_count = 1
    event = {"invalid payload": {}}
    ec = EventCounter(EventData.instance())
    existing_count = json.loads(ec.get_event_count_by_duration_window(secs=MAX_EVENT_COUNT_STORED_LENGTH))["count"]
    ec.signal_event(event=event)
    count = json.loads(ec.get_event_count_by_duration_window(secs=MAX_EVENT_COUNT_STORED_LENGTH))["count"]
    assert count - existing_count == expected_count


def test_get_event_count_by_time():
    """
    Validate with events signaled one second apart, the count only retrieves the right counts given the right window.
    """
    expected_counts = [1, 2, 3]
    event = {"payload": {}}
    ec = EventCounter(EventData.instance())
    for i in range(3):
        time.sleep(1)
        ec.signal_event(event)
    for i in range(3):
        count = json.loads(ec.get_event_count_by_duration_window(secs=i))["count"]
        assert count == expected_counts[i]


def test_put_large_number_events():
    """
    Validate signal a larger set of events
    """
    raise NotImplementedError
