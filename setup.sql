CREATE TABLE Platform(
platformId SERIAL,
name TEXT,
lastUpdate TIMESTAMP,
PRIMARY KEY(platformId)
);

CREATE TABLE Developer(
devId SERIAL,
name TEXT,
lastUpdate TIMESTAMP,
PRIMARY KEY(devId)
);

CREATE TABLE Publisher(
pubId SERIAL,
name TEXT,
lastUpdate TIMESTAMP,
PRIMARY KEY(pubId)
);

CREATE TABLE Genre(
genreId SERIAL,
name TEXT,
lastUpdate TIMESTAMP,
PRIMARY KEY(genreId)
);

CREATE TABLE Client(
userId SERIAL,
username CHAR(40) UNIQUE,
hashedPass CHAR(256),
lastUpdate TIMESTAMP,
PRIMARY KEY(userId)
);

CREATE TABLE Game(
gameId SERIAL,
name TEXT,
releaseDate DATE,
userRating DOUBLE PRECISION,
criticRating DOUBLE PRECISION,
description TEXT,
imageLink TEXT,
lastUpdate TIMESTAMP,
PRIMARY KEY(gameId)
);

CREATE TABLE HasPlatform(
gameId INT,
platformId INT,
lastUpdate TIMESTAMP,
PRIMARY KEY(gameId, platformId),
FOREIGN KEY(gameId) REFERENCES Game(gameId) ON DELETE CASCADE,
FOREIGN KEY(platformId) REFERENCES Platform(platformId) ON DELETE CASCADE
);

CREATE TABLE HasDeveloper(
gameId INT,
devId INT,
lastUpdate TIMESTAMP,
PRIMARY KEY(gameId, devId),
FOREIGN KEY(gameId) REFERENCES Game(gameId) ON DELETE CASCADE,
FOREIGN KEY(devId) REFERENCES Developer(devId) ON DELETE CASCADE
);

CREATE TABLE HasPublisher(
gameId INT,
pubId INT,
lastUpdate TIMESTAMP,
PRIMARY KEY(gameId, pubId),
FOREIGN KEY(gameId) REFERENCES Game(gameId) ON DELETE CASCADE,
FOREIGN KEY(pubId) REFERENCES Publisher(pubId) ON DELETE CASCADE
);

CREATE TABLE HasGenre(
gameId INT,
genreId INT,
lastUpdate TIMESTAMP,
PRIMARY KEY(gameId, genreId),
FOREIGN KEY(gameId) REFERENCES Game(gameId) ON DELETE CASCADE,
FOREIGN KEY(genreId) REFERENCES Genre(genreId) ON DELETE CASCADE
);

CREATE TABLE Likes(
userId INT,
gameId INT,
lastUpdate TIMESTAMP,
PRIMARY KEY(userId, gameId),
FOREIGN KEY(gameId) REFERENCES Game(gameId) ON DELETE CASCADE,
FOREIGN KEY(userId) REFERENCES Client(userId) ON DELETE CASCADE
);

SELECT setval('client_userid_seq', 100, true);