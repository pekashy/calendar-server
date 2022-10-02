import logging

from flask import Flask, request

import schemas.requests as requests_schemas
from handlers.event_handler import EventHandler
from handlers.events_db import EventDB
from handlers.user_handler import UserHandler

logger = logging.getLogger('calendar')
app = Flask(__name__)
events_db = EventDB(logger)
events_handler = EventHandler(logger=logger, db=events_db)
user_handler = UserHandler(logger=logger, db=events_db)


@app.route('/user_events', methods=['GET'])
def user_events():
    get_user_events_request: requests_schemas.UserEventsRequest = requests_schemas.UserEventsRequest.from_dict(
        request.args)
    get_user_events_request.interval_duration_sec = int(get_user_events_request.interval_duration_sec)
    return user_handler.user_events(get_user_events_request)


@app.route('/event', methods=['GET'])
def event_info():
    get_event_info_request: requests_schemas.GetEventRequest = requests_schemas.GetEventRequest.from_dict(request.args)
    return events_handler.event_info(get_event_info_request)


@app.route('/create_event', methods=['POST'])
def create_event():
    create_request = requests_schemas.CreateEventRequest.from_dict(request.json)
    return events_handler.create_event(creation_request=create_request)


@app.route('/find_interval', methods=['POST'])
def find_interval():
    get_free_interval_request: requests_schemas.FirstFreeIntervalRequest = (
        requests_schemas.FirstFreeIntervalRequest.from_dict(request.json)
    )
    get_free_interval_request.interval_duration_sec = int(get_free_interval_request.interval_duration_sec)
    get_free_interval_request.search_interval_duration_sec = int(get_free_interval_request.search_interval_duration_sec)
    return events_handler.free_interval(get_free_interval_request)


@app.route('/approve_event', methods=['POST'])
def approve_event():
    approve_request = requests_schemas.ApproveEventRequest.from_dict(request.json)
    return user_handler.approve_event(approve_request=approve_request)


@app.route('/add_user', methods=['POST'])
def add_user():
    create_request = requests_schemas.CreateUserRequest.from_dict(request.json)
    return user_handler.create_user(create_request=create_request)


def _setup_logger():
    formatter = logging.Formatter(
        fmt=
        "%(asctime)s.%(msecs)03d %(levelname)s %(module)s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler("/logs/calendar.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


if __name__ == '__main__':
    events_db.connect()
    _setup_logger()
    app.run(host='0.0.0.0', port=8050, debug=False)
