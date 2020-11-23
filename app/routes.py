from app import flaskapp
from flask import request, render_template

from app import database


db_instance = database.db()


@flaskapp.route('/')
def popular():
    #temp test data
    #top_10_games = [(1, "Skyrim", "Temp", 1.0, 1.0, "Temp")]
    top_10_games = db_instance.select_games_sort_by_likes_10()
    return render_template("main.html", page = "home", games=top_10_games)

@flaskapp.route('/search/')
def search():

    search_type = None
    query =  None
    games = None

    display_data = True
    if "type" in request.args:    
        search_type = request.args.get("type")

    if "query" in request.args:
        query = request.args.get("query")

    if search_type == None:
        display_data = False

    elif search_type == "word" and query is not None:
        games = db_instance.select_games_by_query_string(query)

    elif search_type == "likes_desc":
        games = db_instance.select_games_sort_by_likes()

    elif search_type == "name_asc":
        games = db_instance.select_games_sort_by_alph()
    else:
        display_data = False


    return render_template("main.html",
                            page = "search", 
                            display_data = display_data, 
                            games = games)

@flaskapp.route('/profile/')
def profile():
    return "Profile page"

@flaskapp.route('/login/')
def login():
    return render_template("main.html", page = "login")

@flaskapp.route('/game/<int:game_id>/')
def game(game_id):
    games = db_instance.select_game_by_gameid(game_id)
    return render_template("main.html", page = "game", games = games)
