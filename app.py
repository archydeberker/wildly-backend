from flask import Flask, jsonify, request
import json

app = Flask(__name__)


@app.route("/ping")
def ping():
    return json.dumps({"result": "pong"})


@app.after_request
def after_request(response):
    header = response.headers
    header["Access-Control-Allow-Origin"] = "*"
    return response


if __name__ == "__main__":
    app.run(
        debug=True, host="127.0.0.1", port=5000
    )  # run app in debug mode on port 5000

