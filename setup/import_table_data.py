import csv
import logging
import os
import psycopg2 as pg
import psycopg2.extras as pgex

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    db_name = os.getenv("DATABASE")
    db_host =  os.getenv("HOST")
    db_port = os.getenv("PORT")
    db_user = os.getenv("USER")
    db_pass = os.getenv("PASS")

    game_path = "table_data/Game.csv"
    dev_path = "table_data/Developer.csv"
    pub_path = "table_data/Publisher.csv"
    platform_path = "table_data/Platform.csv"
    genre_path = "table_data/Genre.csv"
    hasdev_path = "table_data/HasDeveloper.csv"
    haspub_path = "table_data/HasPublisher.csv"
    hasplatform_path = "table_data/HasPlatform.csv"
    hasgenre_path = "table_data/HasGenre.csv"
    client_path = "table_data/Client.csv"
    likes_path = "table_data/Likes.csv"

    game_rows = []
    dev_rows = []
    pub_rows = []
    platform_rows = []
    genre_rows = []
    hasdev_rows = []
    haspub_rows = []
    hasplatform_rows = []
    hasgenre_rows = []
    client_rows = []
    likes_rows = []

    logger.debug("Loading Game csv from {}...".format(game_path))
    with open(game_path, "r", newline="") as csv_file:
        reader = csv.reader(csv_file, delimiter="|")
        for row in reader:
            game_rows.append(row)
    logger.debug("Loaded Game csv.")

    logger.debug("Loading Developer csv from {}...".format(dev_path))
    with open(dev_path, "r", newline="") as csv_file:
        reader = csv.reader(csv_file, delimiter="|")
        for row in reader:
            dev_rows.append(row)
    logger.debug("Loaded Developer csv.")

    logger.debug("Loading Publisher csv from {}...".format(pub_path))
    with open(pub_path, "r", newline="") as csv_file:
        reader = csv.reader(csv_file, delimiter="|")
        for row in reader:
            pub_rows.append(row)
    logger.debug("Loaded Publisher csv.")

    logger.debug("Loading Platform csv from {}...".format(platform_path))
    with open(platform_path, "r", newline="") as csv_file:
        reader = csv.reader(csv_file, delimiter="|")
        for row in reader:
            platform_rows.append(row)
    logger.debug("Loaded Platform csv.")

    logger.debug("Loading Genre csv from {}...".format(genre_path))
    with open(genre_path, "r", newline="") as csv_file:
        reader = csv.reader(csv_file, delimiter="|")
        for row in reader:
            genre_rows.append(row)
    logger.debug("Loaded Genre csv.")

    logger.debug("Loading HasDeveloper csv from {}...".format(hasdev_path))
    with open(hasdev_path, "r", newline="") as csv_file:
        reader = csv.reader(csv_file, delimiter="|")
        for row in reader:
            hasdev_rows.append(row)
    logger.debug("Loaded HasDeveloper csv.")

    logger.debug("Loading HasPublisher csv from {}...".format(haspub_path))
    with open(haspub_path, "r", newline="") as csv_file:
        reader = csv.reader(csv_file, delimiter="|")
        for row in reader:
            haspub_rows.append(row)
    logger.debug("Loaded HasPublisher csv.")

    logger.debug("Loading HasPlatform csv from {}...".format(hasplatform_path))
    with open(hasplatform_path, "r", newline="") as csv_file:
        reader = csv.reader(csv_file, delimiter="|")
        for row in reader:
            hasplatform_rows.append(row)
    logger.debug("Loaded HasPlatform csv.")

    logger.debug("Loading HasGenre csv from {}...".format(hasgenre_path))
    with open(hasgenre_path, "r", newline="") as csv_file:
        reader = csv.reader(csv_file, delimiter="|")
        for row in reader:
            hasgenre_rows.append(row)
    logger.debug("Loaded HasGenre csv.")

    logger.debug("Loading Client csv from {}...".format(client_path))
    with open(client_path, "r", newline="") as csv_file:
        reader = csv.reader(csv_file, delimiter="|")
        for row in reader:
            client_rows.append(row)
    logger.debug("Loaded Client csv.")

    logger.debug("Loading Likes csv from {}...".format(likes_path))
    with open(likes_path, "r", newline="") as csv_file:
        reader = csv.reader(csv_file, delimiter="|")
        for row in reader:
            likes_rows.append(row)
    logger.debug("Loaded Likes csv.")

    # connect to database
    conn = None
    logger.debug("Attempting connection to database. Credentials:\n\tHost: {}\n\tPort: {}\n\tDatabase: {}\n\tUser: {}\n\tPassword: {}".format(db_host, db_port, db_name, db_user, db_pass))
    try:
        conn = pg.connect(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_pass)
        logger.debug("Database connection sucessful")
    except:
        print("Error connection with database credentials, trying again without them")
        try:
            conn = pg.connect(dbname=db_name)
            logger.debug("Database connection sucessful")
        except:
            logger.debug("Error connection with database")
            exit(0)

    # open a cursor to perform db operations
    cur = conn.cursor()

    # insert rows from Game table
    game_argslist = []
    for row in game_rows[1:]:
        game_argslist.append((int(row[0]), 
                              row[1][2:len(row[1])-1],
                              row[2][2:len(row[2])-1],
                              float(row[3]),
                              float(row[4]),
                              row[5][2:len(row[5])-1],
                              row[6][2:len(row[6])-1],
                              row[7][2:len(row[7])-1]))
    pgex.execute_values(cur, "INSERT INTO Game (gameId, name, releaseDate, userRating, criticRating, description, imageLink, lastUpdate) VALUES %s;", game_argslist, template="(%s, %s, %s, %s, %s, %s, %s, %s)")
    conn.commit()

    # insert rows from Developer
    dev_argslist = []
    for row in dev_rows[1:]:
        dev_argslist.append((int(row[0]),
                             row[1][2:len(row[1])-1],
                             row[2][2:len(row[2])-1]))
    pgex.execute_values(cur, "INSERT INTO Developer (devId, name, lastUpdate) VALUES %s", dev_argslist)
    conn.commit()

    # insert rows from Publisher
    pub_argslist = []
    for row in pub_rows[1:]:
        pub_argslist.append((int(row[0]),
                             row[1][2:len(row[1])-1],
                             row[2][2:len(row[2])-1]))
    pgex.execute_values(cur, "INSERT INTO Publisher (pubId, name, lastUpdate) VALUES %s", pub_argslist)
    conn.commit()

    # insert rows from Platform
    platform_argslist = []
    for row in platform_rows[1:]:
        platform_argslist.append((int(row[0]),
                                  row[1][2:len(row[1])-1],
                                  row[2][2:len(row[2])-1]))
    pgex.execute_values(cur, "INSERT INTO Platform (platformId, name, lastUpdate) VALUES %s", platform_argslist)
    conn.commit()

    # insert rows from Genre
    genre_argslist = []
    for row in genre_rows[1:]:
        genre_argslist.append((int(row[0]),
                               row[1][2:len(row[1])-1],
                               row[2][2:len(row[2])-1]))
    pgex.execute_values(cur, "INSERT INTO Genre (genreId, name, lastUpdate) VALUES %s", genre_argslist)
    conn.commit()

    # insert rows from HasDeveloper
    hasdev_argslist = []
    for row in hasdev_rows[1:]:
        hasdev_argslist.append((int(row[0]),
                                int(row[1]),
                                row[2][2:len(row[2])-1]))
    pgex.execute_values(cur, "INSERT INTO HasDeveloper (gameId, devId, lastUpdate) VALUES %s", hasdev_argslist)
    conn.commit()

    # insert rows from HasPublisher
    haspub_argslist = []
    for row in haspub_rows[1:]:
        haspub_argslist.append((int(row[0]),
                                int(row[1]),
                                row[2][2:len(row[2])-1]))
    pgex.execute_values(cur, "INSERT INTO HasPublisher (gameId, pubId, lastUpdate) VALUES %s", haspub_argslist)
    conn.commit()

    # insert rows from HasPlatform
    hasplatform_argslist = []
    for row in hasplatform_rows[1:]:
        hasplatform_argslist.append((int(row[0]),
                                     int(row[1]),
                                     row[2][2:len(row[2])-1]))
    pgex.execute_values(cur, "INSERT INTO HasPlatform (gameId, platformId, lastUpdate) VALUES %s", hasplatform_argslist)
    conn.commit()

    # insert rows from HasGenre
    hasgenre_argslist = []
    for row in hasgenre_rows[1:]:
        hasgenre_argslist.append((int(row[0]),
                                  int(row[1]),
                                  row[2][2:len(row[2])-1]))
    pgex.execute_values(cur, "INSERT INTO HasGenre (gameId, genreId, lastUpdate) VALUES %s", hasgenre_argslist)
    conn.commit()

    # insert rows from Client
    client_argslist = []
    for row in client_rows[1:]:
        client_argslist.append((int(row[0]),
                                row[1][2:len(row[1])-1],
                                row[2][2:len(row[2])-1],
                                row[3][2:len(row[3])-1]))
    pgex.execute_values(cur, "INSERT INTO Client (userId, username, hashedPass, lastUpdate) VALUES %s", client_argslist)
    conn.commit()

    # insert rows from Likes
    likes_argslist = []
    for row in likes_rows[1:]:
        likes_argslist.append((int(row[0]),
                               int(row[1]),
                               row[2][2:len(row[2])-1]))
    pgex.execute_values(cur, "INSERT INTO Likes (userId, gameId, lastUpdate) VALUES %s", likes_argslist)
    conn.commit()

    # end communciation with the database
    cur.close()
    conn.close()
