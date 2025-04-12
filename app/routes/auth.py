from flask import Blueprint, request, redirect, render_template, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import get_db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        phone_number = request.form.get("phone_number")
        wilaya = request.form.get("wilaya")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmed_password = request.form.get("confirmed_password")

        # Error checking
        if not name:
            return render_template('error.html', error_message="Missing name.")
        if not last_name:
            return render_template('error.html', error_message="Missing last name.")
        if not email:
            return render_template('error.html', error_message="Missing email.")
        if not phone_number:
            return render_template('error.html', error_message="Missing phone number.")
        if not wilaya:
            return render_template('error.html', error_message="Missing wilaya.")
        if not password:
            return render_template('error.html', error_message="Missing password.")
        if not confirmed_password:
            return render_template('error.html', error_message="Missing re-typed password.")
        if len(password) < 8 or len(confirmed_password) < 8:
            return render_template('error.html', error_message="Password must be at least 8 characters.")
        if password != confirmed_password:
            return render_template('error.html', error_message="Passwords don't match.")

        db = get_db()
        cr = db.cursor()

        # Check if username or phone number already exists
        cr.execute("SELECT wilaya, phone_number FROM users WHERE wilaya = ? OR phone_number = ?", (wilaya, phone_number))
        existing_user = cr.fetchone()

        if existing_user:
            if existing_user["username"] == username:
                return render_template('error.html', error_message="Username already taken.")
            if existing_user["phone_number"] == phone_number:
                return render_template('error.html', error_message="Phone number already exists.")

        # Insert new user
        cr.execute(
            "INSERT INTO users (name, last_name, email, phone_number, wilaya, password_hash) VALUES (?, ?, ?, ?, ?, ?)",
            (name, last_name, email, phone_number, username, generate_password_hash(password))
        )
        db.commit()

        # Retrieve user ID
        cr.execute("SELECT id FROM users WHERE username = ?", (username,))
        user_id = cr.fetchone()
        db.close()

        session["user_id"] = user_id[0]
        return redirect("/")

    return render_template("user/signup.html")

@auth_bp.route('/userLogin', methods=['GET', 'POST'])
def login():
    if "user_id" in session:
        return redirect("/")
    session.pop("admin_id", None)

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return render_template('error.html', error_message="Must provide username.")
        if not password:
            return render_template('error.html', error_message="Must provide password.")

        db = get_db()
        cr = db.cursor()
        cr.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cr.fetchone()
        db.close()

        if not user or not check_password_hash(user["password_hash"], password):
            return render_template('error.html', error_message="Invalid username and/or password.")

        session["user_id"] = user["id"]
        session.permanent = True

        return redirect("/")

    return render_template("user/login.html")

@auth_bp.route('/adminLogin', methods=['GET', 'POST'])
def admin_login():
    if "admin_id" in session:
        return redirect("/admin/dashboard")

    session.pop("user_id", None)

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return render_template('error.html', error_message="Must provide username and password.")

        db = get_db()
        cr = db.cursor()
        cr.execute("SELECT * FROM admin WHERE username = ?", (username,))
        admin = cr.fetchone()
        db.close()

        if not admin or not check_password_hash(admin["password_hash"], password):
            return render_template('error.html', error_message="Invalid admin username and/or password.")

        session["admin_id"] = admin["id"]
        session.permanent = True

        return redirect("/admin/dashboard")

    return render_template("admin/login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")
