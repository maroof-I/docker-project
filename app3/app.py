from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

# URLs of the other Flask apps (update these with the actual container names in docker-compose)
FLASK1_URL = "http://flask1:5001"
FLASK2_URL = "http://flask2:5002"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/aggregated", methods=["GET"])
def get_aggregated_data():
    # Fetch users from flask1
    users_response = requests.get(f"{FLASK1_URL}/users")
    print("Users Response:", users_response.status_code, users_response.text)  # Debugging

    # Check if response is valid before parsing
    users = users_response.json() if users_response.status_code == 200 and users_response.text else []

    # Fetch tasks from flask2
    tasks_response = requests.get(f"{FLASK2_URL}/tasks")
    print("Tasks Response:", tasks_response.status_code, tasks_response.text)  # Debugging

    # Check if response is valid before parsing
    tasks = tasks_response.json() if tasks_response.status_code == 200 and tasks_response.text else []

    # Combine both datasets
    data = {
        "users": users,
        "tasks": tasks
    }
    return jsonify(data)