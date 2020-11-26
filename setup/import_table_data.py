import csv
import logging
import psycopg2 as pg

if __name__ == "__main__":
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    db_name = "gamedb"  # TODO load from environment
    db_user = ""  # Add as keyword argument to pg.connect() if applicable
    db_password = ""  # Add as keyword argument to pg.connect() if applicable

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
    conn = pg.connect(dbname=db_name)

    # open a cursor to perform db operations
    cur = conn.cursor()

    # insert rows from Game table
    game_argslist = []
    for row in game_rows[1:]:
        game_argslist.append([int(row[0]), 
                              "\"{}\"".format(row[1]),
                              "\"{}\"".format(row[2]),
                              float(row[3]),
                              float(row[4]),
                              "\"{}\"".format(row[5]),
                              "\"{}\"".format(row[6]),
                              "\"{}\"".format(row[7])])
    pg.extras.execute_values(cur, '''INSERT INTO Game (gameId, name, releaseDate, userRating, criticRating, description, imageLink, lastUpdate) VALUES %s''', game_argslist)
    conn.commit()

    # insert rows from Developer
    dev_argslist = []
    for row in dev_rows:
        dev_argslist.append([int(row[0]),
                             "\"{}\"".format(row[1]),
                             "\"{}\"".format(row[2])])
    pg.extras.execute_values(cur, '''INSERT INTO Developer (devId, name, lastUpdate) VALUES %s''', dev_argslist)
    conn.commit()

    # insert rows from Publisher
    pub_argslist = []
    for row in pub_rows:
        pub_argslist.append([int(row[0]),
                             "\"{}\"".format(row[1]),
                             "\"{}\"".format(row[2])])
    pg.extras.execute_values(cur, '''INSERT INTO Publisher (pubId, name, lastUpdate) VALUES %s''', pub_argslist)
    conn.commit()

    # insert rows from Platform
    platform_argslist = []
    for row in platform_rows:
        platform_argslist.append([int(row[0]),
                                  "\"{}\"".format(row[1]),
                                  "\"{}\"".format(row[2])])
    pg.extras.execute_values(cur, '''INSERT INTO Platform (platformId, name, lastUpdate) VALUES %s''', platform_argslist)
    conn.commit()

    # insert rows from Genre
    genre_argslist = []
    for row in genre_rows:
        genre_argslist.append([int(row[0]),
                               "\"{}\"".format(row[1]),
                               "\"{}\"".format(row[2])])
    pg.extras.execute_values(cur, '''INSERT INTO Genre (genreId, name, lastUpdate) VALUES %s''', genre_argslist)
    conn.commit()

    # insert rows from HasDeveloper
    hasdev_argslist = []
    for row in hasdev_rows:
        hasdev_argslist.append([int(row[0]),
                                int(row[1]),
                                "\"{}\"".format(row[2])])
    pg.extras.execute_values(cur, '''INSERT INTO HasDeveloper (gameId, devId, lastUpdate) VALUES %s''', hasdev_argslist)
    conn.commit()

    # insert rows from HasPublisher
    haspub_argslist = []
    for row in haspub_rows:
        haspub_argslist.append([int(row[0]),
                                int(row[1]),
                                "\"{}\"".format(row[2])])
    pg.extras.execute_values(cur, '''INSERT INTO HasPublisher (gameId, pubId, lastUpdate) VALUES %s''', haspub_argslist)
    conn.commit()

    # insert rows from HasPlatform
    hasplatform_argslist = []
    for row in hasplatform_rows:
        hasplatform_argslist.append([int(row[0]),
                                     int(row[1]),
                                     "\"{}\"".format(row[2])])
    pg.extras.execute_values(cur, '''INSERT INTO HasPlatform (gameId, platformId, lastUpdate) VALUES %s''', hasplatform_argslist)
    conn.commit()

    # insert rows from HasGenre
    hasgenre_argslist = []
    for row in hasgenre_rows:
        hasgenre_argslist.append([int(row[0]),
                                  int(row[1]),
                                  "\"{}\"".format(row[2])])
    pg.extras.execute_values(cur, '''INSERT INTO HasGenre (gameId, genreId, lastUpdate) VALUES %s''', hasgenre_argslist)
    conn.commit()

    # insert rows from Client
    client_argslist = []
    for row in client_rows:
        client_argslist.append([int(row[0]),
                                "\"{}\"".format(row[1]),
                                "\"{}\"".format(row[2]),
                                "\"{}\"".format(row[3])])
    pg.extras.execute_values(cur, '''INSERT INTO Client (userId, username, hashedPass, lastUpdate) VALUES %s''', client_argslist)
    conn.commit()

    # insert rows from Likes
    likes_argslist = []
    for row in likes_rows:
        likes_argslist.append([int(row[0]),
                               int(row[1]),
                               "\"{}\"".format(row[2])])
    pg.extras.execute_values(cur, '''INSERT INTO Likes (userId, gameId, lastUpdate) VALUES %s''', likes_argslist)
    conn.commit()

    # end communciation with the database
    cur.close()
    conn.close()
