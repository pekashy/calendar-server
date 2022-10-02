import logging

from flask import Flask, request

import common
import schemas.event
import schemas.requests as requests_schemas
import schemas.responses as responses_schemas
from events_db import EventDB

logger = logging.getLogger('calendar')
app = Flask(__name__)
events_db = EventDB(logger)


@app.route('/event_list', methods=['GET'])
def event_list():
    pass


@app.route('/event', methods=['GET'])
def event_info():
    event_id = request.args.get('id')
    event = events_db.get_event(event_id)
    if not event:
        return responses_schemas.make_response(
            data=responses_schemas.BadResponse(error_code='not_found', message='Event was not found'),
            status=404
        )
    event_schema = schemas.event.get_schema_from_event(event)
    return responses_schemas.make_response(
        data=responses_schemas.GetEventResponse(event=event_schema),
    )


def _ensure_event_users_lists_guarantees(event: common.Event):
    if event.created_by not in event.invited:
        event.invited.append(event.created_by)
    if event.created_by not in event.accepted:
        event.accepted.append(event.created_by)


@app.route('/create_event', methods=['POST'])
def create_event():
    create_request = requests_schemas.CreateEventRequest.from_dict(request.json)
    event_schema = create_request.event
    event = schemas.event.get_event_from_schema(event_schema)
    _ensure_event_users_lists_guarantees(event)
    events_db.save_event(event)
    return responses_schemas.make_response(
        data=responses_schemas.OkResponse(message='Event Created')
    )


@app.route('/approve_event', methods=['POST'])
def approve_event():
    pass


@app.route('/add_user', methods=['POST'])
def add_user():
    pass


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
