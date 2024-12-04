from flask import render_template, session, redirect, url_for
from flask_login import (
    current_user,
    login_required,
)

from dotenv import load_dotenv
from os import getenv

import requests

from frontend.forms.check import check_role

from .. import app

load_dotenv('.env.example')
BASE = getenv('URL_BASE')

@app.route("/", methods=['POST', 'GET'])
@login_required
def home():
    email = session.get('email')
    data = check_role(email=email)


    if data == 'candidate':
        user_tasks = requests.get(url=f'{BASE}/tasks/not_executor_tasks/{email}')

        if user_tasks.status_code == 200:
            tasks = user_tasks.json()
            task_list = []

            for task_id, task_name in zip(tasks['task_ids'], tasks['task_names']):
                task_list.append({
                    'id': task_id, 
                    'name': task_name
                            })
        elif user_tasks.status_code == 404:
            return 'Error 404'

        return render_template('show_task.html', tasks=task_list)
    
    elif data == 'employer':
        tasks_response = requests.get(url=f'{BASE}/tasks/get_employer_tasks/', params={'email':email})

        if tasks_response.status_code == 200:
            tasks = tasks_response.json()

            task_list = []

            for task in tasks:
                task_list.append({
                    'name':task.get('name'),
                    'id':task.get('id')
                })

            return render_template('show_task.html', tasks=task_list)

        elif tasks_response.status_code == 404:
            return 'Error 404'
    else:
        return redirect(url_for('register'))
            



@app.route("/dashboard")
@login_required
def dashboard():
    return "Ласкаво просимо на панель управління!"