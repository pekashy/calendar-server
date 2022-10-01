import logging
from flask import Flask, request, jsonify
from events_db import EventDB
import schemas

app = Flask(__name__)
events_db = EventDB()


@app.route('/event_list', methods=['GET'])
def event_list():
    pass


@app.route('/event', methods=['GET'])
def event_info():
    pass


@app.route('/create_event', methods=['POST'])
def create_event():
    event = schemas.get_event_from_schema(schemas.EventSchema.from_dict(request.json))
    events_db.save_event(event)
    return jsonify({"Result": "Ok"})


@app.route('/approve_event', methods=['POST'])
def approve_event():
    pass


@app.route('/add_user', methods=['POST'])
def add_user():
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=False)
