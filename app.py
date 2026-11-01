from flask import Flask, render_template, request, jsonify
from calculator import safe_calculate
from config import HISTORY_FILE, MAX_HISTORY, SECRET_KEY, DATA_DIR

import os
import json
from datetime import datetime


app = Flask(__name__)

app.config["SECRET_KEY"] = SECRET_KEY


def load_history():

    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return []


def save_history(history):

    os.makedirs(DATA_DIR, exist_ok=True)

    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/api/calculate", methods=["POST"])
def calculate():

    data = request.get_json(silent=True) or {}

    expression = data.get("expression", "")

    try:

        result = safe_calculate(expression)

        history = load_history()

        history.insert(0, {
            "expression": expression,
            "result": str(result),
            "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        })

        save_history(history[:MAX_HISTORY])

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "error": str(error)
        }), 400


@app.route("/api/history")
def history():

    return jsonify(load_history())


@app.route("/api/history/clear", methods=["POST"])
def clear_history():

    save_history([])

    return jsonify({
        "success": True,
        "message": "History cleared"
    })


@app.route("/api/health")
def health():

    return jsonify({
        "status": "online",
        "application": "Vanshidhun Pro Calculator",
        "version": "1.0"
    })


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )