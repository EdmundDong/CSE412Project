import psycopg2
from passlib.hash import sha256_crypt
from datetime import datetime

class db():
    def __init__(self):
        self.connection = None
        try:
            self.connection = psycopg2.connect(host = "localhost", port = "8088", database = "GameDB")
            print("Database connection sucessful")
        except:
            print("Error connection with database, trying again")
            try:
                self.connection = psycopg2.connect(database = "gamedb")
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

        connection.commit()
        cursor.close()

        return user_id

    def user_authenticate(self, username, password):
        cursor = self.connection.cursor()

        sql = 'SELECT * FROM Client WHERE username = %s'
        data = [username]

        cursor.execute(sql, data)

        result = cursor.fetchone()
        cursor.close()
        if result == None:
            return (None, "Username not found")
        elif not sha256_crypt.verify(password, result[2]):
            return (None, "Wrong Password")
        else:
            return (result[0], "Success")

    def update_game_rating(self, game_name, rating):
        cursor = self.connection.cursor()

        sql = "UPDATE Game SET userRating = %s WHERE name = %s;";
        data = [rating, game_name]

        cursor.execute(sql, data)

        connection.commit()

        cursor.close()

        return

    def remove_user_like(self, game_id, user_id):
        cursor = self.connection.cursor()

        sql = "DELETE FROM Likes WHERE userId = %s AND gameId = %s";
        data = [user_id, game_id]

        cursor.execute(sql, data)

        connection.commit()

        cursor.close()

        return

    def add_user_like(self, game_id, user_id):
        cursor = self.connection.cursor()

        timestamp = datetime.now()

        sql = "INSERT INTO Likes VALUES(%s, %s, %s)";
        data = [user_id, game_id, timestamp]

        cursor.execute(sql, data)

        connection.commit()

        cursor.close()

        return

    def select_games_liked_by_user(self, user_id):
        cursor = self.connection.cursor()

        sql = """SELECT Game.* 
                FROM Client, Likes, Game 
                WHERE Client.userId = Likes.userId 
                    AND Likes.gameId = Game.gameId
                    AND Client.userId = %s"""
        data = [user_id]

        cursor.execute(sql,data)

        results = cursor.fetchall()

        cursor.close()

        return results

    def select_games_published_by_publisher(self, publisher_name):
        cursor = self.connection.cursor()

        sql = """SELECT Game.*
                 FROM Game, HasPublisher, Publisher
                 WHERE Game.gameId = HasPublisher.gameId
                    AND HasPublisher.pubId = Publisher.pubId
                    AND Publisher.name = %s
                 ORDER BY releaseDate DESC;"""
        data = [user_id]

        cursor.execute(sql,data)

        results = cursor.fetchall()

        cursor.close()

        return results

    def select_games_sort_release(self):
        cursor = self.connection.cursor()
        sql = 'SELECT * FROM Game ORDER BY releaseDate DESC;'

        cursor.execute(sql)

        results = cursor.fetchall()

        cursor.close()

        return results

    def select_games_sort_user_rating(self):
        cursor = self.connection.cursor()
        sql = 'SELECT * FROM Game ORDER BY userRating DESC;'

        cursor.execute(sql)

        results = cursor.fetchall()

        cursor.close()

        return results

    def select_games_sort_critic_rating(self):
        cursor = self.connection.cursor()
        sql = 'SELECT * FROM Game ORDER BY criticRating DESC;'

        cursor.execute(sql)

        results = cursor.fetchall()

        cursor.close()

        return results

    def select_games_sort_by_likes(self):
        cursor = self.connection.cursor()
        sql = """SELECT Game.*, T.likes_amount
                 FROM Game
                 LEFT JOIN (SELECT COUNT(userId) AS likes_amount, gameId
                            FROM Likes
                            GROUP BY gameId) AS T
                 ON Game.gameId = T.gameId
                 ORDER BY T.likes_amount DESC NULLS LAST;"""

        cursor.execute(sql)

        results = cursor.fetchall()

        cursor.close()

        return results

    def select_games_sort_by_likes_10(self):
        cursor = self.connection.cursor()
        sql = """SELECT Game.*, T.likes_amount
                 FROM Game
                 LEFT JOIN (SELECT COUNT(userId) AS likes_amount, gameId
                            FROM Likes
                            GROUP BY gameId) AS T
                 ON Game.gameId = T.gameId
                 ORDER BY T.likes_amount DESC NULLS LAST
                 LIMIT 10;"""

        cursor.execute(sql)

        results = cursor.fetchall()

        cursor.close()

        return results

    def select_games_sort_by_alph(self):
        cursor = self.connection.cursor()
        sql = 'SELECT * FROM Game ORDER BY name ASC;'

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

    def select_games_by_developer(self, developer_id):
        cursor = self.connection.cursor()
        sql = """SELECT Game.*
                    FROM Game, Developer, HasDeveloper
                    WHERE Game.gameId = HasDeveloper.gameId 
                            AND Developer.devId = HasDeveloper.devId 
                            AND Developer.devId = %s;
                    """
        data = [developer_id]
        cursor.execute(sql,data)

        results = cursor.fetchall()

        cursor.close()

        return results

    def select_games_by_query_string(self, query_string):
        cursor = self.connection.cursor()
        sql = """SELECT *
                    FROM Game
                    WHERE name LIKE %s;
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

    def __del__(self):
        if self.connection is not None:
            self.connection.close()




        