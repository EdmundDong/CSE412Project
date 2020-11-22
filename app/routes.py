from app import flaskapp

@flaskapp.route('/')
@flaskapp.route('/index')
def index():
    return "Hello World!"