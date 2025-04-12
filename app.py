from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'S9uh4b$meDiJ#nBr'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sql:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)

class Users(db.Model):
    emp_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/users")
def users():
     return render_template("users.html")


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)