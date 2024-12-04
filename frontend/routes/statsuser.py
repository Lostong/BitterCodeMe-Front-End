from flask import Flask, render_template
from .. import app


@app.route('/status')
def status():
    user_data = {
        'name': 'Імя',
        'email': 'Пошта',
        'address': 'вул, регіон',
        'phone': '+380 00 00 000'
    }
    return render_template('stats_user.html', user=user_data)


