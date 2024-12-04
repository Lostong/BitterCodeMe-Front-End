import requests

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    session,
    flash,
)
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    current_user,
)

from dotenv import load_dotenv

from os import getenv

from frontend.forms.check import check_role

from .. import app

load_dotenv(".env.example")
BASE = getenv("URL_BASE")

tasks = {
    "1": {
        "title": "Task 1",
        "description": "Description for task 1",
        "unit_tests": "assert func(2) == 4",
    },
    "2": {
        "title": "Task 2",
        "description": "Description for task 2",
        "unit_tests": "assert func(3) == 9",
    },
}


@app.route("/submit_task", methods=["POST"])
@login_required
def submit_task():
    data = request.get_json()
    task_description = data.get("description")
    unit_tests = data.get("tests")
    code_prototype = data.get("code_prototype")

    print(f"Task Description: {task_description}")
    print(f"Unit Tests: {unit_tests}")
    print(f"Code Prototype: {code_prototype}")

    return jsonify({"message": "Task successfully submitted!"})


@app.route("/create_task", methods=["POST", "GET"])
@login_required
def create_task():
    email = session.get("email")
    check = check_role(email=email)

    if check == "employer":
        if request.method == "POST":
            name = request.form.get("taskName")
            description = request.form.get("taskDescription")
            tests = request.form.get("unitTests")
            complexity = request.form.get("complexity")
            email = session.get("email")

            print(name, description, tests, complexity, email)

            user_response = requests.get(url=f"{BASE}/user/email/{email}")

            if user_response.status_code == 200:
                user = user_response.json()
                user_id = user["id"]
                data = {
                    "name": name,
                    "description": description,
                    "employer_id": user_id,
                    "unit_tests": tests,
                    "complexity_id": complexity,
                }
                response = requests.post(url=f"{BASE}/tasks/create", json=data)
                if response.status_code == 200:
                    return redirect(url_for("home"))
                else:
                    return "error"

        return render_template("task.html")
    elif check == "candidate":
        return redirect(url_for("home"))


@app.route("/task/solve/<task_id>", methods=["GET", "POST"])
@login_required
def solve_task(task_id):
    response = requests.get(url=f"{BASE}/tasks/{task_id}")
    if response.status_code != 200:
        return "Error fetching task information", response.status_code

    task = response.json()
    title = task.get("title", "No Title")
    description = task.get("description", "No Description")
    unit_tests = task.get("unit_tests", "")

    return render_template(
        "task.html",
        task_title=title,
        task_description=description,
        unit_tests=unit_tests,
        task_id=task_id,
    )


@app.route("/execute_task/<int:task_id>", methods=["POST", "GET"])
@login_required
def execute_task(task_id: int):
    if request.method == "GET":
        task_response = requests.get(url=f"{BASE}/tasks/{task_id}")
        if task_response.status_code != 200:
            return "", task_response.status_code

        task_data = task_response.json()
        task_title = task_data.get("title")
        task_description = task_data.get("description")
        unit_tests = task_data.get("unit_tests")

        return render_template(
            "execute_task.html",
            task_title=task_title,
            task_description=task_description,
            unit_tests=unit_tests,
            task_id=task_id,
        )

    if request.method == "POST":
        user_code = request.form.get("userCode")
        email = session.get("email")

        user_response = requests.get(url=f"{BASE}/user/email/{email}")
        if user_response.status_code != 200:
            return "User not found", 404

        user = user_response.json()
        user_id = user["id"]
        data = {"code": user_code, "task_id": task_id, "user_id": user_id}
        print(data)

        response = requests.post(url=f"{BASE}/execute_task", params=data)
        if response.status_code == 200:
            return redirect(url_for("home"))
        else:
            return "Error executing the task", 500
