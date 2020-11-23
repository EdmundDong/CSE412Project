from app import flaskapp
from flask import request, render_template


@flaskapp.route('/')
@flaskapp.route('/index')
def index():
    return "Hello World!"

@flaskapp.route('/login', methods=["GET"])
def login():
    return render_template()