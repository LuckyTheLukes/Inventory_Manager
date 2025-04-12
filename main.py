import database_handler
from flask import Flask, flash, redirect, request, url_for, render_template


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
    if request.method == "POST":
        empID = request.form["emp_id"]
        username = request.form["user_name"]
        database_handler.write_to_database("users", (empID, username, 1))
    
    headings = ('Employee ID', 'Name', '', '')
    data = database_handler.read_from_database("users")
    print(data)
    return render_template("/users.html", headings=headings, data=data)

@app.route("/edit/<string:empID>", methods=["POST", "GET"])
def edit_user(empID):
    return f"Edit page for {empID}"

@app.route("/delete/<string:empID>", methods=["POST", "GET"])
def delete_user(empID):
    return f"User with Employee ID {empID} has been deleted!"


if __name__ == '__main__':
    app.run(debug=True)