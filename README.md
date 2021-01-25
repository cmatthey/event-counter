# Event Counter project
Event Counter is a small library which helps to track the number of events that happened during a specified window of time.

## Features
Event counter supports two operations:
- Receives a signal from the client when a single event happened
- Answer the request the number of events that happened over a user-specified amount of time until the current time

## Setup
git clone https://github.com/cmatthey/event-counter

## Usage 
Thie library provides two callable functions. Usage examples are in the below:
- EventCounter(event_data=EventData.instance()).signal_event(event={"payload": {}})
- EventCounter(event_data=EventData.instance()).get_event_count_by_duration_window(window_in_secs=MAX_EVENT_COUNT_STORED_LENGTH))["count"]

## High level design
Event Counter supports two operations and store the event data count in a light weight class in the memory.
 
## Testing
In the project root directory run pytest
