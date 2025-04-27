from datetime import datetime, timezone
from flask import Flask, flash, redirect, render_template, request, url_for
from models import db, User, Inventory


app = Flask(__name__)
app.secret_key = "S9uh4b$meDiJ#nBr"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///workshop_inventory.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

""" db = SQLAlchemy(app)

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
    is_active = db.Column(db.Boolean, default=True) """


@app.route("/")
def index():
    inventory = Inventory.query.filter_by(is_active=True).all()
    users = User.query.all()
    return render_template("index.html", inventory=inventory, users=users)


@app.route("/add_item", methods=["POST"])
def add_item():
    try:
        new_item = Inventory(
            item_name=request.form["item_name"],
            brand=request.form["brand"] or "-",
            model=request.form["model"] or "-",
            serial_number=request.form["serial_number"] or "-",
            quantity=int(request.form["quantity"] or 0),
            unit=request.form["unit"] or "-",
            category=request.form["category"] or "-",
            location=request.form["location"] or "-",
            min_stock=int(request.form["min_stock"] or 0),
            remarks=request.form["remarks"] or "-",
        )
        db.session.add(new_item)
        db.session.commit()
        flash(f"New item {new_item.item_name} added successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {e}", "danger")
    return redirect(url_for("index"))


@app.route("/retrieve_item/<int:id>", methods=["POST"])
def retrieve_item(id):
    item = Inventory.query.get_or_404(id)

    try:
        retrieve_amount = request.form.get("retrieve_amount", type=int)
        user_id = request.form.get("user_id", type=int)
        justification = request.form.get("justification", type=str)

        if retrieve_amount is None:
            flash("Please enter a valid quantity to retrieve.", "warning")
        elif retrieve_amount <= 0:
            flash("Please enter a positive quantity to retrieve.", "warning")
        elif item.quantity <= 0:
            flash(f"Item {item.item_name} is out of stock.", "warning")
        elif retrieve_amount > item.quantity:
            flash("Cannot retrieve more than available quantity.", "warning")
        else:
            item.quantity -= retrieve_amount
            db.session.commit()
            flash(
                f"Successfully retrieved {retrieve_amount} {item.unit} of {item.item_name}.",
                "success",
            )

    except Exception as e:
        db.session.rollback()
        flash(f"Error: {e}", "danger")

    return redirect(url_for("index"))


@app.route("/edit_item/<int:id>", methods=["POST"])
def edit_item(id):
    item = Inventory.query.get_or_404(id)
    has_changes = False

    def check_update(field, value, cast_type=str):
        nonlocal has_changes
        current = getattr(item, field)

        if value == "":
            value = None

        if value is not None and cast_type != str:
            try:
                value = cast_type(value)
            except ValueError:
                value = None

        if current != value:
            setattr(item, field, value)
            has_changes = True

    check_update("item_name", request.form.get("item_name"))
    check_update("brand", request.form.get("brand"))
    check_update("model", request.form.get("model"))
    check_update("serial_number", request.form.get("serial_number"))
    check_update("quantity", request.form.get("quantity"), int)
    check_update("unit", request.form.get("unit"))
    check_update("category", request.form.get("category"))
    check_update("location", request.form.get("location"))
    check_update("min_stock", request.form.get("min_stock"), int)
    check_update("remarks", request.form.get("remarks"))

    if has_changes:
        item.last_updated = datetime.now(timezone.utc)
        try:
            db.session.commit()
            flash(f"Item {item.item_name} updated successfully.", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {e}", "danger")

    return redirect(url_for("index"))


@app.route("/delete_item/<int:id>", methods=["POST"])
def delete_item(id):
    item = Inventory.query.get_or_404(id)
    try:
        item.is_active = False
        db.session.commit()
        flash(f"Item {item.item_name} has been archived.", "warning")
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {e}", "danger")
    return redirect(url_for("index"))


@app.route("/users")
def users():
    users = User.query.all()
    return render_template("users.html", users=users)


@app.route("/add_user", methods=["POST"])
def add_user():
    try:
        new_user = User(
            emp_id=request.form["emp_id"], user_name=request.form["user_name"]
        )
        db.session.add(new_user)
        db.session.commit()
        flash(f"User {new_user.user_name} added successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {e}", "danger")
    return redirect(url_for("users"))


@app.route("/edit_user/<int:id>", methods=["POST"])
def edit_user(id):
    user = User.query.get_or_404(id)
    try:
        user.emp_id = request.form["emp_id"]
        user.user_name = request.form["user_name"]
        db.session.commit()
        flash(f"User {user.user_name} updated successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {e}", "danger")
    return redirect(url_for("users"))


@app.route("/delete_user/<int:id>", methods=["POST"])
def delete_user(id):
    user = User.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash(f"User {user.user_name} deleted.", "danger")
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {e}", "danger")
    return redirect(url_for("users"))


# with app.app_context():
#    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
