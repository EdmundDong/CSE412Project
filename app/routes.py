from app import flaskapp
from flask import request, render_template

from app import database


db_instance = database.db()


@flaskapp.route('/')
def popular():
    #not tested
    top_10_games = db_instance.select_games_sort_by_likes_10()

    #top_10_games = [(1, "Skyrim", "Temp", 1.0, 1.0, "Temp")]

    return render_template("main.html", page = "home", games=top_10_games)

@flaskapp.route('/search/')
def search():

    search_type = None
    query =  None
    games = None

    display_data = True
    if "type" in request.args:    
        search_type = request.args.get("type")

    if "query" in requrest.args:
        query = request.args.get("query")

    if search_type == None:
        display_data = False

    elif search_type == "word" and query not None:
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
def game(game_id):
    return "Profile page"

@flaskapp.route('/game/<int:game_id>/')
def game_with_id(game_id):
    return "Page for game #" + str(game_id)
