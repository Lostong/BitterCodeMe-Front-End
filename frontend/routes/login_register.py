import requests

from flask import render_template, request, redirect, url_for, flash, session

from flask_login import (
    login_user,
    logout_user,
)

from dotenv import load_dotenv

from os import getenv

from frontend.forms.login_register import Login, Registration

from frontend.routes.session import User_log

from frontend import app
from frontend.routes.session import load_user

load_dotenv(".env.example")
BASE = getenv("URL_BASE")


@app.route("/register", methods=["POST", "GET"])
def register():
    form = Registration()
    form.submit.label.text = "Registration"
    if request.method == "POST":
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            role_id = int(form.role.data)

            data = {"email": email, "password": password, "role_id": role_id}

            response = requests.post(url=f"{BASE}/register", json=data)
            print(data)

            if response.status_code == 200:
                user_response = requests.get(url=f"{BASE}/user/email/{form.email.data}")

                if user_response.status_code == 200:
                    user_data = user_response.json()
                    user = User_log(
                        id=user_data["id"], email=user_data["email"], active=True
                    )
                    login_user(user=user)
                    load_user(user.email)
                    session["email"] = user.email
                    return redirect(url_for("home"))

            elif response.status_code == 400:
                flash("User with this email already exists")
                return render_template(
                    "login_registration_form.html", form=form, action="/register"
                )

        return render_template(
            "login_registration_form.html", form=form, action="/register"
        )
    return render_template(
        "login_registration_form.html", form=form, action="/register"
    )


@app.route("/login", methods=["POST", "GET"])
def login():
    form = Login()
    if request.method == "POST":
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            data = {"email": email, "password": password, "role_id": 1}
            print(data)
            response = requests.post(url=f"{BASE}/login", json=data)

            if response.status_code == 200:
                user_response = requests.get(url=f"{BASE}/user/email/{email}")
                if user_response.status_code == 200:
                    user_data = user_response.json()
                    user = User_log(
                        id=user_data["id"], email=user_data["email"], active=True
                    )
                    login_user(user=user)
                    load_user(user.email)
                    session["email"] = user.email
                    return redirect(url_for("home"))

            elif response.status_code == 401:
                flash("Wrong password")
                redirect(url_for("login"))
            elif response.status_code == 404:
                flash("User not found")
                redirect(url_for("login"))
            elif response.status_code == 422:
                redirect(url_for("register"))

        return render_template(
            "login_registration_form.html", form_login=form, action="/login"
        )
    return render_template(
        "login_registration_form.html", form_login=form, action="/login"
    )


@app.route("/logout")
def log_out():
    logout_user()
    flash("You are logged out")
    return redirect(url_for("login"))
