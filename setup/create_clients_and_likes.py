import csv
import datetime as dt
import hashlib as hl
import random

game_id_range = (1, 4027)
num_likes_range = (25, 50)

user_count = 40

def make_pg_string(string):
    return "'{}'".format(string)

user_ids = list(range(1, user_count + 1))
usernames = ["theshiningant",
             "muttonsurfing",
             "owlcowglove",
             "bagelthekid",
             "pathsofglory",
             "jadeitestone",
             "hamryefishing",
             "piscesaries",
             "floralpasta",
             "standbymepls",
             "spiderotter",
             "webcokeant",
             "omeganebula",
             "triangulum",
             "lettuceweb",
             "soybeansand",
             "polarboots",
             "footballman",
             "icecreambear",
             "findingemo",
             "tenniscake",
             "marsexpress",
             "sandwichire",
             "waterfallian",
             "lambchopwatermelon",
             "trumpetstyx",
             "ryemeadownet",
             "dogsavannah",
             "galileoleo",
             "quasarfirefly",
             "leafybat",
             "generalchickenegg",
             "gallantbeans",
             "theviolatempo",
             "lizardatsea",
             "pandanet",
             "thelegend27",
             "singingrice",
             "colonelhamburger",
             "crispychaos"]

passwords = ["password{}".format(x) for x in range(0, user_count)]
likes = []

for user_id in user_ids:
    likes.append(random.sample(list(range(game_id_range[0], game_id_range[1] + 1)), random.randint(num_likes_range[0], num_likes_range[1])))
    

client_header = ["userId", "username", "hashedPass", "lastUpdate"]
likes_header = ["userId", "gameId", "lastUpdate"]
unhashed_header = ["username", "password"]

client_path = "table_data/Client.csv"
likes_path = "table_data/Likes.csv"
unhashed_path = "table_data/unhashed.csv"

def get_hash(string):
    return hl.sha256(str.encode("{}".format(string))).hexdigest()

with open(client_path, "w", newline="") as client_csv:
    writer = csv.writer(client_csv, delimiter="|")
    writer.writerow(client_header)
    for index in range(0, len(user_ids)):
        user_id = user_ids[index]
        username = usernames[index]
        hashed_pass = get_hash(passwords[index])
        last_update = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        current_row = [user_id, make_pg_string(username), make_pg_string(hashed_pass), make_pg_string(last_update)]

        writer.writerow(current_row)

with open(likes_path, "w", newline="") as likes_csv:
    writer = csv.writer(likes_csv, delimiter="|")
    writer.writerow(likes_header)
    for index in range(0, len(user_ids)):
        user_id = user_ids[index]
        for game_id in likes[index]:
            last_update = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            current_row = [user_id, game_id, make_pg_string(last_update)]

            writer.writerow(current_row)

with open(unhashed_path, "w", newline="") as unhashed_csv:
    writer = csv.writer(unhashed_csv, delimiter="|")
    writer.writerow(unhashed_header)
    for index in range(0, len(usernames)):
        username = usernames[index]
        password = passwords[index]
        writer.writerow([username, password])