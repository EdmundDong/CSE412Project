from app import flaskapp
from flask import request, render_template, jsonify
import os
from dotenv import load_dotenv
load_dotenv()

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
    page = 1

    display_data = True
    if "type" in request.args:    
        search_type = request.args.get("type")

    if "page" in request.args:
        page = int(request.args.get("page"))

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
    
    output_games = []
    
    max_page = False
    if games is not None:
        index = (page - 1) * 10
        if index >= len(games):
            index = 0
            page = 1
            
        limit = min(index+10, len(games))
        while index < limit:
            output_games.append(games[index])
            index += 1

        if index+10 >= len(games):
            max_page = True
    
    print(output_games)
    return render_template("main.html",
                            page = "search", 
                            display_data = display_data, 
                            games = output_games, 
                            page_num = page,
                            max_page = max_page)

@flaskapp.route("/register/", methods=["GET"])
def register_page():
    return render_template("main.html", 
                            page = "register")

@flaskapp.route("/api/register/", methods = ["POST"])
def register():
    body = request.get_json()
    
    found = db_instance.find_user(body["username"])

    if not found:
        user_id = db_instance.create_user(body["username"], body["password"])
        return jsonify({"user_id": user_id, "username": body["username"]})
    return jsonify({"error": "something went wrong"})

@flaskapp.route("/login/", methods=["GET"])
def login_page():
    return render_template("main.html",
                            page = "login")

@flaskapp.route("/api/login/", methods=["POST"])
def login():
    body = request.get_json()
    
    authenticate = db_instance.user_authenticate(body["username"], body["password"])

    if authenticate[0] is None:
        return jsonify({"error": authenticate[1]})
   
    return jsonify({"user_id": authenticate[0], "username": body["username"]})
        

@flaskapp.route('/profile/', methods=["GET"])
def profile():
    return render_template("main.html", page = "profile", profile = profile)

@flaskapp.route("/api/profile/<int:user_id>", methods=["GET"])
def profile_info(user_id):
    games = db_instance.select_games_liked_by_user(user_id)
    return jsonify({"games": games})

@flaskapp.route('/game/<int:game_id>/')
def game(game_id):
    games = db_instance.select_gamepage_by_gameid(game_id)
    return render_template("main.html", page = "game", games = games)

@flaskapp.route('/api/game/<int:game_id>/<int:user_id>', methods=["GET"])
def user_likes_game(game_id, user_id):
    games = db_instance.select_games_liked_by_user(user_id)

    like = False
    for game in games:
        if game[0] == game_id:
            like = True
            break
    
    return jsonify({"like": like})

@flaskapp.route("/api/game/likes/<int:game_id>/<int:user_id>", methods=["GET"])
def user_update_likes(game_id, user_id):
    games = db_instance.select_games_liked_by_user(user_id)

    like = False
    for game in games:
        if game[0] == game_id:
            like = True
            break
    
    if like:
        db_instance.remove_user_like(game_id, user_id)
    else:
        db_instance.add_user_like(game_id, user_id)

    return jsonify({"msg": "done"})