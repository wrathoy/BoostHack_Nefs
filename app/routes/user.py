from flask import Blueprint, request, redirect, render_template, session, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import get_db
from app.helpers import apology

user_bp = Blueprint('user', __name__)

@user_bp.route("/")
def homepage():
    return render_template("user/home.html")


@user_bp.route("/articles")
def services():
    return render_template("user/articles.html")

@user_bp.route("/aboutUs")
def aboutus():
    return render_template("user/about.html")
@user_bp.route("/faq")
def faq():
    return render_template("user/faq.html")

