from datetime import datetime, timezone
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "S9uh4b$meDiJ#nBr"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.Integer, unique=True, nullable=False)
    user_name = db.Column(db.String(100), nullable=False)


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100))
    model = db.Column(db.String(100))
    serial_number = db.Column(db.String(100))
    quantity = db.Column(db.Integer, nullable=False, default=0)
    unit = db.Column(db.String(50))
    category = db.Column(db.String(100))
    location = db.Column(db.String(100))
    min_stock = db.Column(db.Integer)
    remarks = db.Column(db.String(255))
    date_added = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_updated = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))
    is_active = db.Column(db.Boolean, default=True)


@app.route("/")
def index():
    inventory = Inventory.query.all()
    return render_template("index.html", inventory=inventory)


@app.route("/add_item", methods=["POST"])
def add_item():
    item_name = request.form["item_name"]
    brand = request.form["brand"]
    model = request.form["model"]
    serial_number = request.form["serial_number"]
    quantity = request.form["quantity"]
    unit = request.form["unit"]
    category = request.form["category"]
    location = request.form["location"]
    min_stock = request.form["min_stock"]
    remarks = request.form["remarks"]

    new_item = Inventory(
        item_name=item_name,
        brand=brand,
        model=model,
        serial_number=serial_number,
        quantity=quantity,
        unit=unit,
        category=category,
        location=location,
        min_stock=min_stock,
        remarks=remarks,
    )

    try:
        db.session.add(new_item)
        db.session.commit()
        flash(f"New item {item_name} has been added successfully", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {e}", "danger")

    return redirect(url_for("index"))


@app.route("/edit_item/<int:id>", methods=["POST"])
def edit_item(id):
    item = Inventory.query.get_or_404(id)
    has_changes = False

    def check_update(field_name, form_field):
        nonlocal has_changes
        new_value = request.form.get(form_field)
        if getattr(item, field_name) != new_value:
            setattr(item, field_name, new_value)
            has_changes = True

    check_update('item_name', 'item_name')
    check_update('brand', 'brand')
    check_update('model', 'model')
    check_update('serial_number', 'serial_number')
    check_update('quantity', 'quantity')
    check_update('unit', 'unit')
    check_update('category', 'category')
    check_update('location', 'location')
    check_update('min_stock', 'min_stock')
    check_update('remarks', 'remarks')

    if has_changes:
        item.last_updated = lambda: datetime.now(timezone.utc)


@app.route("/delete_item/<int:id>", methods=["POST"])
def delete_item(id):
    item = Inventory.query.get_or_404(id)
    flash(f"Item {item.item_name} has been removed!", "danger")
    return redirect(url_for("index"))


@app.route("/users")
def users():
    users = User.query.all()
    return render_template("users.html", users=users)


@app.route("/add_user", methods=["POST"])
def add_user():
    emp_id = request.form["emp_id"]
    user_name = request.form["user_name"]
    new_user = User(emp_id=emp_id, user_name=user_name)

    try:
        db.session.add(new_user)
        db.session.commit()
        flash(f"User {user_name} was successfully added!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {e}", "danger")

    return redirect(url_for("users"))


@app.route("/edit_user/<int:id>", methods=["POST"])
def edit_user(id):
    try:
        user = User.query.get_or_404(id)
        user.emp_id = request.form["emp_id"]
        user.user_name = request.form["user_name"]
        db.session.commit()
        flash(f"User {user.user_name} has been successfully updated!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {e}", "danger")

    return redirect(url_for("users"))


@app.route("/delete_user/<int:id>", methods=["POST"])
def delete_user(id):
    try:
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        flash(f"User {user.user_name} has been removed!", "danger")
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {e}", "danger")

    return redirect(url_for("users"))


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
