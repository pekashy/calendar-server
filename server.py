import logging
from flask import Flask

app = Flask(__name__)


@app.route('/event_list', methods=['GET'])
def event_list():
    pass


@app.route('/event', methods=['GET'])
def event_info():
    pass


@app.route('/create_event', methods=['POST'])
def create_event():
    pass


@app.route('/approve_event', methods=['POST'])
def approve_event():
    pass


@app.route('/add_user', methods=['POST'])
def add_user():
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=False)
