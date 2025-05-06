from flask import Flask, jsonify, request, render_template, redirect, url_for
from models import db, Tasks
from dotenv import load_dotenv

load_dotenv()
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', "False").lower() == "true"

db.init_app(app)

@app.before_request
def create_tables():
    with app.app_context():
        db.create_all()
        
@app.route("/", methods=["GET"])
def home():
    """Render a home page for tasks."""
    tasks = Tasks.get_tasks()  # Fetch tasks
    return render_template("index.html", tasks=tasks)

@app.route("/tasks", methods=["GET"])
def get_tasks():
    """Return JSON data for API requests."""
    tasks = Tasks.get_tasks()
    return jsonify([{"id": task.id, "task": task.task, "time": task.time} for task in tasks])

@app.route("/add_task", methods=["GET", "POST"])
def create_task():
    if request.method == "POST":
        task_data = request.form
        task = Tasks(task=task_data["task"], time=task_data["time"])
        task.create_task()
        return redirect(url_for("get_tasks"))
    return render_template("add.html")

