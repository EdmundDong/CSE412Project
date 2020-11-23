from app import flaskapp

@flaskapp.route('/')
@flaskapp.route('/index/')
def index():
    return "Hello World!"

@flaskapp.route('/popular/')
def popular():
    return "List of top games"

@flaskapp.route('/search/')
def search():
    return "Search for games here"

@flaskapp.route('/profile/')
def game(game_id):
    return "Profile page"

@flaskapp.route('/game/<int:game_id>/')
def game(game_id):
    return "Page for game #" + str(game_id)