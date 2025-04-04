import database_handler
from flask import Flask, redirect, url_for, render_template


database_handler.create_database_and_tables()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)