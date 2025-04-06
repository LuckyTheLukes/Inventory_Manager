import database_handler
from flask import Flask, redirect, request, url_for, render_template


database_handler.create_database_and_tables()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add_items")
def add_items():
    return render_template("add_items.html")

@app.route("/users", methods=["POST", "GET"])
def manage_users():
    database_handler.read_from_database("users")
    if request.method == "POST":
        empID = request.form["emp_id"]
        username = request.form["user_name"]
        database_handler.write_to_database("users", (empID, username, 1))
    return render_template("/users.html")

if __name__ == '__main__':
    app.run(debug=True)