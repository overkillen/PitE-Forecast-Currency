from flask import Flask
import flask
import json

app = Flask(__name__)


@app.route("/")
def index():
    return "Currency forecast"

@app.route("/currency")
def get_currency():
    response = flask.Response(json.dumps({'GBP':5.01}))
    response.headers['Content-Type'] = "application/json"
    return response


if __name__ == '__main__':
    app.run()