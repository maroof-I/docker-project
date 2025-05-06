from flask import Flask, jsonify, request, render_template, redirect, url_for
from models import db, Users
from dotenv import load_dotenv

load_dotenv()
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', "False").lower() == "true"

db.init_app(app)

@app.before_request
def create_tables():
    with app.app_context():  # Ensure the app context is available
        db.create_all()

@app.route("/", methods=["GET"])
def home():
    """Render a home page for users."""
    users = Users.get_users()  # Fetch users
    return render_template("index.html", users=users)

@app.route("/users", methods=["GET"])
def get_users():
    """Return JSON data for API requests."""
    users = Users.get_users()
    return jsonify([{"id": user.id, "name": user.name, "email": user.email} for user in users])

@app.route("/add_user", methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        user_data = request.form
        user = Users(name=user_data["name"], email=user_data["email"], password=user_data["password"])
        user.create_user()
        return redirect(url_for("get_users"))
    return render_template("add.html")

@app.route("/edit_user/<int:id>", methods=["GET", "POST"])
def edit_user(id):
    user = Users.query.get(id)
    if request.method == "POST":
        user_data = request.form
        user.name = user_data["name"]
        user.email = user_data["email"]
        user.password = user_data["password"]
        user.edit_user()
        return redirect(url_for("get_users"))
    return render_template("edit.html", user=user)

@app.route("/delete_user/<int:id>", methods=["GET", "POST"])
def delete_user(id):
    user = Users.query.get(id)
    if request.method == "POST":
        user.delete_user()
        return redirect(url_for("get_users"))
    return render_template("delete.html", user=user)

if __name__ == "__main__":
    app.run(debug=True)
