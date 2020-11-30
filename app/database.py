import psycopg2
from passlib.hash import sha256_crypt
from datetime import datetime
import os

DATABASE = os.getenv("DATABASE")
HOST =  os.getenv("HOST")
PORT = os.getenv("PORT")

class db():
    def __init__(self):
        self.connection = None
        print("HOST: "+(HOST,"None")[HOST is None]+", PORT: "+(PORT,"None")[PORT is None]+", DATABASE: "+(DATABASE,"None")[DATABASE is None])
        try:
            self.connection = psycopg2.connect(host=HOST, port=PORT, dbname=DATABASE)
            print("Database connection sucessful")
        except:
            print("Error connection with database credentials, trying again without them")
            try:
                self.connection = psycopg2.connect(dbname=DATABASE)
                print("Database connection sucessful")
            except:
                print("Error connection with database")
                exit(0)

    #find if user exists
    def find_user(self, username):
        cursor = self.connection.cursor()

        sql = 'SELECT COUNT(*) FROM Client WHERE username = %s;'
        data = [username]
        cursor.execute(sql, data)

        result = cursor.fetchone()

        count = result[0]

        cursor.close()
        if count != 0:
            return True
        return False

    def create_user(self, username, password):
        cursor = self.connection.cursor()

        hashedpass = sha256_crypt.hash(password)
        timestamp = datetime.now()

        sql = 'INSERT INTO Client(username, hashedPass, lastUpdate) VALUES(%s, %s, %s) RETURNING userId;'
        data = [username, hashedpass, timestamp]

        cursor.execute(sql, data)

        result = cursor.fetchone()

        user_id = result[0]

        self.connection.commit()
        cursor.close()

        return user_id

    def user_authenticate(self, username, password):
        cursor = self.connection.cursor()

        sql = 'SELECT * FROM Client WHERE username = %s'
        data = [username]

        cursor.execute(sql, data)

        result = cursor.fetchone()
        cursor.close()
        print(password)
        print(result)
        print(sha256_crypt.verify(password, result[2].strip()))
        if result == None:
            return (None, "Username not found")
        elif not sha256_crypt.verify(password, result[2].strip()):
            return (None, "Wrong Password")
        else:
            return (result[0], "Success")

    def update_game_rating(self, game_name, rating):
        cursor = self.connection.cursor()

        sql = "UPDATE Game SET userRating = %s WHERE name = %s;";
        data = [rating, game_name]

        cursor.execute(sql, data)

        self.connection.commit()

        cursor.close()

        return

    def remove_user_like(self, game_id, user_id):
        cursor = self.connection.cursor()

        sql = "DELETE FROM Likes WHERE userId = %s AND gameId = %s";
        data = [user_id, game_id]

        cursor.execute(sql, data)

        self.connection.commit()

        cursor.close()

        return

    def add_user_like(self, game_id, user_id):
        cursor = self.connection.cursor()

        timestamp = datetime.now()

        sql = "INSERT INTO Likes VALUES(%s, %s, %s)";
        data = [user_id, game_id, timestamp]

        cursor.execute(sql, data)

        self.connection.commit()

        cursor.close()

        return

    def select_games_liked_by_user(self, user_id):
        cursor = self.connection.cursor()

        sql = """SELECT Game.*, T.likes_amount, Genre.name as Genre
                FROM Client, Likes, Genre, HasGenre, Game 
                        LEFT JOIN (SELECT COUNT(userId) AS likes_amount, gameId
                        FROM Likes
                        GROUP BY gameId) AS T
                ON Game.gameId = T.gameId
                WHERE Game.gameid = HasGenre.gameid
                AND HasGenre.genreid = Genre.genreid
                AND Client.userId = Likes.userId
                AND Likes.gameId = Game.gameId
                AND Client.userId = 1
                ORDER BY Game.name DESC NULLS LAST;"""
        data = [user_id]

        cursor.execute(sql,data)

        results = cursor.fetchall()

        cursor.close()

        return results
    
    def get_publisher_name(self, platform_id):
        cursor = self.connection.cursor()
        sql = """SELECT name
                FROM Publisher
                WHERE pubid = %s;"""
        data = [platform_id]
        cursor.execute(sql,data)

        results = cursor.fetchall()

        cursor.close()

        return results
    
    def get_developer_name(self, developer_id):
        cursor = self.connection.cursor()
        sql = """SELECT name
                FROM Developer
                WHERE devid = %s;"""
        data = [developer_id]
        cursor.execute(sql,data)

        results = cursor.fetchall()

        cursor.close()

        return results
    
    def select_games_published_by_publisher(self, publisherid):
        cursor = self.connection.cursor()

        sql = """SELECT Game.*, T.likes_amount, Genre.name as Genre, Publisher.name as Publisher
                    FROM HasPublisher, Publisher, Genre, HasGenre, Game 
                        LEFT JOIN (SELECT COUNT(userId) AS likes_amount, gameId
                        FROM Likes
                        GROUP BY gameId) AS T
                    ON Game.gameId = T.gameId
                    WHERE Game.gameid = HasGenre.gameid
                    AND HasGenre.genreid = Genre.genreid
                    AND Game.gameId = HasPublisher.gameId
                    AND HasPublisher.pubId = Publisher.pubId
                    AND Publisher.pubid = %s
                    ORDER BY releaseDate DESC;"""
        data = [publisherid]

        cursor.execute(sql,data)

        results = cursor.fetchall()

        cursor.close()

        return results
    
    def select_games_developed_by_developer(self, developerid):
        cursor = self.connection.cursor()

        sql = """SELECT Game.*, T.likes_amount, Genre.name as Genre, Developer.name as Developer
                    FROM HasPublisher, Developer, Genre, HasGenre, Game 
                        LEFT JOIN (SELECT COUNT(userId) AS likes_amount, gameId
                        FROM Likes
                        GROUP BY gameId) AS T
                    ON Game.gameId = T.gameId
                    WHERE Game.gameid = HasGenre.gameid
                    AND HasGenre.genreid = Genre.genreid
                    AND Game.gameId = HasPublisher.gameId
                    AND HasPublisher.pubId = Developer.devId
                    AND Developer.devid = %s
                    ORDER BY releaseDate DESC;"""
        data = [developerid]

        cursor.execute(sql,data)

        results = cursor.fetchall()

        cursor.close()

        return results

    def select_games_sort_release(self):
        cursor = self.connection.cursor()
        sql = """SELECT Game.*, T.likes_amount, Genre.name as Genre
                 FROM Genre, HasGenre, Game
                 LEFT JOIN (SELECT COUNT(userId) AS likes_amount, gameId
                            FROM Likes
                            GROUP BY gameId) AS T
                 ON Game.gameId = T.gameId
                 WHERE Game.gameid = HasGenre.gameid
                 AND HasGenre.genreid = Genre.genreid
                 ORDER BY Game.releaseDate DESC NULLS LAST;"""

        cursor.execute(sql)

        results = cursor.fetchall()

        cursor.close()

        return results

    def select_games_sort_user_rating(self):
        cursor = self.connection.cursor()
        sql = """SELECT Game.*, T.likes_amount, Genre.name as Genre
                 FROM Genre, HasGenre, Game
                 LEFT JOIN (SELECT COUNT(userId) AS likes_amount, gameId
                            FROM Likes
                            GROUP BY gameId) AS T
                 ON Game.gameId = T.gameId
                 WHERE Game.gameid = HasGenre.gameid
                 AND HasGenre.genreid = Genre.genreid
                 ORDER BY Game.userRating DESC NULLS LAST;"""

        cursor.execute(sql)

        results = cursor.fetchall()

        cursor.close()

        return results

    def select_games_sort_critic_rating(self):
        cursor = self.connection.cursor()
        sql = """SELECT Game.*, T.likes_amount, Genre.name as Genre
                 FROM Genre, HasGenre, Game
                 LEFT JOIN (SELECT COUNT(userId) AS likes_amount, gameId
                            FROM Likes
                            GROUP BY gameId) AS T
                 ON Game.gameId = T.gameId
                 WHERE Game.gameid = HasGenre.gameid
                 AND HasGenre.genreid = Genre.genreid
                 ORDER BY Game.criticRating DESC NULLS LAST;"""

        cursor.execute(sql)

        results = cursor.fetchall()

        cursor.close()

        return results

    def select_games_sort_by_likes(self):
        cursor = self.connection.cursor()
        sql = """SELECT Game.*, T.likes_amount, Genre.name as Genre
                 FROM Genre, HasGenre, Game
                 LEFT JOIN (SELECT COUNT(userId) AS likes_amount, gameId
                            FROM Likes
                            GROUP BY gameId) AS T
                 ON Game.gameId = T.gameId
                 WHERE Game.gameid = HasGenre.gameid
                 AND HasGenre.genreid = Genre.genreid
                 ORDER BY T.likes_amount DESC NULLS LAST;"""

        cursor.execute(sql)

        results = cursor.fetchall()

        cursor.close()

        return results

    def select_games_sort_by_alph(self):
        cursor = self.connection.cursor()
        sql = """SELECT Game.*, T.likes_amount, Genre.name as Genre
                FROM Genre, HasGenre, Game 
                        LEFT JOIN (SELECT COUNT(userId) AS likes_amount, gameId
                        FROM Likes
                        GROUP BY gameId) AS T
                ON Game.gameId = T.gameId
                WHERE Game.gameid = HasGenre.gameid
                AND HasGenre.genreid = Genre.genreid
                ORDER BY Game.name ASC NULLS LAST;"""

        cursor.execute(sql)

        results = cursor.fetchall()

        cursor.close()

        return results

    def select_games_sort_by_likes_10(self):
        cursor = self.connection.cursor()
        sql = """SELECT Game.*, T.likes_amount, Genre.name as Genre
                FROM Genre, HasGenre, Game 
                        LEFT JOIN (SELECT COUNT(userId) AS likes_amount, gameId
                        FROM Likes
                        GROUP BY gameId) AS T
                ON Game.gameId = T.gameId
                WHERE Game.gameid = HasGenre.gameid
                AND HasGenre.genreid = Genre.genreid
                ORDER BY T.likes_amount DESC NULLS LAST
                LIMIT 10;"""

        cursor.execute(sql)

        results = cursor.fetchall()

        cursor.close()

        return results

    def get_number_likes_for_game(self, game_id):
        cursor = self.connection.cursor()
        sql = """SELECT COUNT(userId)
                FROM (Likes
                    NATURAL JOIN Game)
                WHERE gameId = selectedGameId;"""

        cursor.execute(sql)

        results = cursor.fetchall()

        cursor.close()

        return results

    def select_games_user_likes(self, username):
        cursor = self.connection.cursor()
        sql = """SELECT Game.*
                    FROM Client, Likes, Game
                    WHERE Client.userId = Likes.userId AND Likes.gameId = Game.gameId AND Client.username = %s;
                    """
        data = [username]
        cursor.execute(sql,data)

        results = cursor.fetchall()

        cursor.close()

        return results
    
    def select_games_by_platform(self, platform_id):
        cursor = self.connection.cursor()
        sql = """SELECT Game.*
                FROM Game, Platform, HasPlatform
                WHERE Game.gameId = HasPlatform.GameId 
                    AND Platform.platformId = HasPlatform.platformId 
                    AND Platform.platformId = %s;"""
        data = [platform_id]
        cursor.execute(sql,data)

        results = cursor.fetchall()

        cursor.close()

        return results

    def select_games_by_query_string(self, query_string):
        cursor = self.connection.cursor()
        sql = """SELECT Game.*, T.likes_amount, Genre.name as Genre
                    FROM Genre, HasGenre, Game 
                            LEFT JOIN (SELECT COUNT(userId) AS likes_amount, gameId
                            FROM Likes
                            GROUP BY gameId) AS T
                    ON Game.gameId = T.gameId
                    WHERE Game.gameid = HasGenre.gameid
                    AND HasGenre.genreid = Genre.genreid
                    AND Game.name LIKE %s
                    ORDER BY T.likes_amount DESC NULLS LAST;
                    """
        data = ["%"+query_string+"%"]
        cursor.execute(sql,data)

        results = cursor.fetchall()

        cursor.close()

        return results
        
    def select_game_by_gameid(self, gameid):
        cursor = self.connection.cursor()
        sql = """SELECT *
                    FROM Game
                    WHERE gameid = %s;
                    """
        data = [gameid]
        cursor.execute(sql,data)

        results = cursor.fetchall()

        cursor.close()

        return results

    def select_gamepage_by_gameid(self, gameid):
        cursor = self.connection.cursor()
        sql = """SELECT Game.*, T.likes_amount, Platform.name as Platform, Developer.devid as DeveloperId, Developer.name as Developer, Publisher.pubid as PublisherId, Publisher.name as Publisher, Genre.name as Genre
                    FROM Platform, HasPlatform, Developer, HasDeveloper, Publisher, HasPublisher, Genre, HasGenre, Game 
                        LEFT JOIN (SELECT COUNT(userId) AS likes_amount, gameId
                        FROM Likes
                        GROUP BY gameId) AS T
                    ON Game.gameId = T.gameId
                    WHERE Game.gameid = HasGenre.gameid
                    AND HasGenre.genreid = Genre.genreid
                    AND Game.gameid = HasPlatform.gameid
                    AND HasPlatform.platformid = Platform.platformid
                    AND Game.gameid = HasDeveloper.gameid
                    AND HasDeveloper.devid = Developer.devid
                    AND Game.gameid = HasPublisher.gameid
                    AND HasPublisher.pubid = Publisher.pubid
                    AND Game.gameid = %s;
                    """
        data = [gameid]
        cursor.execute(sql,data)

        results = cursor.fetchall()

        cursor.close()

        return results
        
    def select_recommended_games(self, userid):
        cursor = self.connection.cursor()
        sql = """SELECT V.*, T.likes_amount, Genre.name as Genre
                    FROM Genre, HasGenre, (SELECT Game.*
                    FROM Game, HasGenre, 


                    (SELECT B.genreId 
                    FROM (SELECT MAX(T.counts) AS maxcounts
                    FROM (SELECT COUNT(HasGenre.gameId) AS counts, Genre.genreId
                        FROM Genre, Likes, HasGenre
                        WHERE Likes.userId = %s
                        AND Likes.gameId = HasGenre.gameId
                        AND Genre.genreId = HasGenre.genreId
                        GROUP BY Genre.genreId) AS T) AS U,

                    (SELECT COUNT(HasGenre.gameId) AS counts, Genre.genreId
                        FROM Genre, Likes, HasGenre
                        WHERE Likes.userId = %s
                        AND Likes.gameId = HasGenre.gameId
                        AND Genre.genreId = HasGenre.genreId
                        GROUP BY Genre.genreId) AS B



                    WHERE U.maxcounts = B.counts ) AS C
                    WHERE HasGenre.genreId = C.genreId
                    AND Game.gameId = HasGenre.gameId) As V
                    LEFT JOIN (SELECT COUNT(userId) AS likes_amount, gameId
                                                FROM Likes
                                                GROUP BY gameId) AS T
                    ON V.gameId = T.gameId
                    WHERE V.gameid = HasGenre.gameid
                    AND HasGenre.genreid = Genre.genreid
                    ORDER BY T.likes_amount DESC NULLS LAST;
                    """
        data = [userid, userid]
        cursor.execute(sql,data)

        results = cursor.fetchall()

        cursor.close()

        return results
    
    def __del__(self):
        if self.connection is not None:
            self.connection.close()