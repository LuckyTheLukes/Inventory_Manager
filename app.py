from datetime import datetime
import os
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    make_response,
)
from models import db, User, Inventory, InventoryHistory
from flask_migrate import Migrate
import json
from weasyprint import HTML
import csv
import backup_setup
import backup_script
import configparser
from version import __version__


app_version = __version__
app_name = "Workshop Inventory Management System"

print(f"Running {app_name} - Version: {app_version}")

app = Flask(__name__)
app.secret_key = "S9uh4b$meDiJ#nBr"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///workshop_inventory.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrage = Migrate(app, db)


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
        db.session.flush()  # Flush to get the ID for the history record

        history_record = InventoryHistory(
            inventory_id=new_item.id,
            user_id=request.form["user_id"],
            action="added",
            quantity_changed=int(request.form["quantity"] or 0),
            remarks=request.form["remarks"] or "-",
        )
        db.session.add(history_record)

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
            item.last_updated = datetime.now()

            db.session.flush()  # Flush to get the ID for the history record

            history_record = InventoryHistory(
                inventory_id=item.id,
                user_id=request.form["user_id"],
                action="retrieved",
                quantity_changed=retrieve_amount,
                remarks=request.form["remarks"] or "-",
            )
            db.session.add(history_record)

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
    previous_quantity = item.quantity
    changes = []

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
            changes.append(f"{field} changed from '{current}' to '{value}'")

    check_update("item_name", request.form.get("item_name"))
    check_update("brand", request.form.get("brand") or "-")
    check_update("model", request.form.get("model") or "-")
    check_update("serial_number", request.form.get("serial_number") or "-")
    check_update("quantity", request.form.get("quantity") or 0, int)
    check_update("unit", request.form.get("unit") or "-")
    check_update("category", request.form.get("category") or "-")
    check_update("location", request.form.get("location") or "-")
    check_update("min_stock", request.form.get("min_stock") or 0, int)
    check_update("remarks", request.form.get("remarks") or "-")

    if has_changes:
        item.last_updated = datetime.now()

        try:
            new_quantity = request.form.get("quantity", type=int)
            remarks_note = request.form.get("remarks") or "-"
            changes_description = "; ".join(changes)

            history_record = InventoryHistory(
                inventory_id=item.id,
                user_id=request.form["user_id"],
                action="updated",
                quantity_changed=(
                    new_quantity - previous_quantity if new_quantity is not None else 0
                ),
                remarks=f"{remarks_note} | changes: {changes_description}",
            )
            db.session.add(history_record)

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

        history_record = InventoryHistory(
            inventory_id=item.id,
            user_id=request.form["user_id"],
            action="deleted",
            quantity_changed=item.quantity,
            remarks=request.form.get("remarks") or "-",
        )

        db.session.add(history_record)
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


@app.route("/low_stock")
def low_stock():
    low_stock_items = Inventory.query.filter(
        Inventory.is_active == True, Inventory.quantity <= Inventory.min_stock
    ).all()
    return render_template("low_stock.html", low_stock_items=low_stock_items)


@app.route("/history")
def history():
    history = InventoryHistory.query.all()
    return render_template("history.html", history=history)


@app.route("/export/history_pdf", methods=["POST"])
def export_history_pdf():
    raw_data = request.form.get("table_data")
    if not raw_data:
        flash("No data to export.", "warning")
        return redirect(url_for("history"))

    try:
        table_data = json.loads(raw_data)
        rendered = render_template(
            "pdf_template_history.html", rows=table_data, now=datetime.now()
        )
        pdf = HTML(string=rendered).write_pdf()
        response = make_response(pdf)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"history_report_{timestamp}.pdf"

        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = f"inline; filename={filename}"
        return response

    except Exception as e:
        flash(f"Error generating PDF: {e}", "danger")
        return redirect(url_for("history"))


@app.route("/export/history_csv", methods=["POST"])
def export_history_csv():
    raw_data = request.form.get("table_data")
    if not raw_data:
        flash("No data to export.", "warning")
        return redirect(url_for("history"))

    try:
        rows = json.loads(raw_data)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"history_report_{timestamp}.csv"
        response = make_response()
        response.headers["Content-Disposition"] = f"attachment; filename={filename}"
        response.headers["Content-Type"] = "text/csv"

        writer = csv.writer(response.stream)
        writer.writerow(
            ["Date", "User Name", "Item Name", "Action", "Quantity Changed", "Remarks"]
        )
        writer.writerows(rows)

        return response

    except Exception as e:
        flash(f"Error generating CSV: {e}", "danger")
        return redirect(url_for("history"))


@app.route("/export/inventory_pdf", methods=["POST"])
def export_inventory_pdf():
    raw_data = request.form.get("table_data")
    if not raw_data:
        flash("No data to export.", "warning")
        return redirect(url_for("index"))

    try:
        table_data = json.loads(raw_data)
        rendered = render_template(
            "pdf_template_inventory.html", rows=table_data, now=datetime.now()
        )
        pdf = HTML(string=rendered).write_pdf()
        response = make_response(pdf)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"AVL_Inventory_{timestamp}.pdf"

        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = f"inline; filename={filename}"
        return response

    except Exception as e:
        flash(f"Error generating PDF: {e}", "danger")
        return redirect(url_for("index"))


@app.route("/export/inventory_csv", methods=["POST"])
def export_inventory_csv():
    raw_data = request.form.get("table_data")
    if not raw_data:
        flash("No data to export.", "warning")
        return redirect(url_for("index"))

    try:
        rows = json.loads(raw_data)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"Inventory_{timestamp}.csv"
        response = make_response()
        response.headers["Content-Disposition"] = f"attachment; filename={filename}"
        response.headers["Content-Type"] = "text/csv"

        writer = csv.writer(response.stream)
        writer.writerow(
            [
                "Item Name",
                "Brand",
                "Model",
                "Serial Number",
                "Quantity",
                "Unit",
                "Category",
                "Location",
                "Min Stock",
                "Remarks",
                "Date Added",
                "Last Updated",
            ]
        )
        writer.writerows(rows)

        return response

    except Exception as e:
        flash(f"Error generating CSV: {e}", "danger")
        return redirect(url_for("index"))
    

@app.route("/settings")
def settings():
    try:
        config = configparser.ConfigParser()
        settings_path = os.path.join(os.path.dirname(__file__), "settings.ini")
        config.read(settings_path)

        backup_dir = config.get("BackupSettings", "BACKUP_DIR", fallback="./db_backup")
        frequency = config.get("BackupSettings", "FREQUENCY", fallback="DAILY")
        time = config.get("BackupSettings", "TIME", fallback="00:00")

        return render_template(
            "settings.html",
            backup_dir=backup_dir,
            frequency=frequency,
            time=time,
        )
    except Exception as e:
        flash(f"Error loading settings: {e}", "danger")
        return redirect(url_for("index"))



@app.route("/update_settings", methods=['POST'])
def update_settings():
    try:
        backup_dir = request.form.get("backup_dir", "./db_backup")
        frequency = request.form.get("frequency", "DAILY").upper()
        time = request.form.get("time", "00:00")

        print(f"Backup Directory: {backup_dir}")
        print(f"Frequency: {frequency}")
        print(f"Time: {time}")

        config = configparser.ConfigParser()
        settings_path = os.path.join(os.path.dirname(__file__), "settings.ini")
        config.read(settings_path)

        config["BackupSettings"]["BACKUP_DIR"] = backup_dir
        config["BackupSettings"]["FREQUENCY"] = frequency
        config["BackupSettings"]["TIME"] = time

        with open(settings_path, "w") as configfile:
            config.write(configfile)

        flash("Settings updated successfully.", "success")

        backup_setup.create_task(force=True)
        flash("Backup task recreated successfully.", "success")

    except Exception as e:
        flash(f"Error updating settings: {e}", "danger")

    return redirect(url_for("settings"))


backup_setup.create_task(force=False)
backup_script.backup_database()

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
