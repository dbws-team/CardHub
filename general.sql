CREATE TABLE USERS (
	UserId INT  AUTO_INCREMENT,
	Username TEXT,
	Email TEXT,
	Password TEXT,
	DateJoined TIMESTAMP,
	PRIMARY KEY(UserId)
);

CREATE TABLE PLAYERS(
    UserId INT,
    League TEXT,
    FOREIGN KEY(UserID)REFERENCES USERS(UserId)
);

CREATE TABLE CREATORS(
    UserId INT,
    FOREIGN KEY(UserID)REFERENCES USERS(UserId)
);

CREATE TABLE CARDS (
   	CardId INT  AUTO_INCREMENT,
    BackText TEXT,
	PRIMARY KEY(CardId)
);

CREATE TABLE PHOTO_CARDS (
   	CardId INT  AUTO_INCREMENT,
	FrontImage TEXT,
	BackText TEXT,
	FOREIGN KEY(CardId) REFERENCES CARDS(CardId)
);

CREATE TABLE TEXT_CARDS (
   	CardId INT  AUTO_INCREMENT,
	FrontText TEXT,
	BackText TEXT,
	FOREIGN KEY(CardId) REFERENCES CARDS(CardId)
);

CREATE TABLE LEADERBOARDS (
    LeaderboardId INT  AUTO_INCREMENT,
    CompetitionId INT,
    PRIMARY KEY (LeaderboardId)
);

CREATE TABLE COMPETITIONS (
	CompetitionId INT,
	LeaderboardId INT,
	CompetitionType TEXT,
	PRIMARY KEY(CompetitionId)
);

CREATE TABLE TIME_COMPETITIONS (
	CompetitionId INT,
	LeaderboardId INT,
    StartTime TIMESTAMP,
	FOREIGN KEY(CompetitionId) REFERENCES COMPETITIONS(CompetitionId),
    FOREIGN KEY(LeaderboardId) REFERENCES LEADERBOARDS(LeaderboardId)
);

CREATE TABLE SCORE_COMPETITIONS (
	CompetitionId INT,
	LeaderboardId INT,
	FOREIGN KEY(CompetitionId) REFERENCES COMPETITIONS(CompetitionId),
	FOREIGN KEY(LeaderboardId) REFERENCES LEADERBOARDS(LeaderboardId)
);

CREATE TABLE CARDSETS (
	CardsetId INT AUTO_INCREMENT PRIMARY KEY
);

CREATE TABLE CARDSETS_CARDS (
    CardsetId INT,
    CardId INT,
    FOREIGN KEY (CardsetId) REFERENCES CARDSETS(CardsetId),
    FOREIGN KEY (CardId) REFERENCES CARDS(CardId)
);

CREATE TABLE CARDSETS_USERS (
    CardsetId INT,
    UserId INT,
    FOREIGN KEY (CardsetId) REFERENCES CARDSETS(CardsetId),
    FOREIGN KEY (UserId) REFERENCES USERS(UserId)
);

CREATE TABLE SCORE_LEADERBOARDS (
LeaderboardId INT,
	UserId INT,
	Score INT,
	Place INT,
	FOREIGN KEY (UserId) REFERENCES USERS(UserId),
	FOREIGN KEY (LeaderboardId) REFERENCES LEADERBOARDS(LeaderboardId)

);

CREATE TABLE TIME_LEADERBOARDS (
	LeaderboardId INT,
	UserId INT,
	Time INT,
	Place INT,
	FOREIGN KEY (UserId) REFERENCES USERS(UserId),
	FOREIGN KEY (LeaderboardId) REFERENCES LEADERBOARDS(LeaderboardId)
);
CREATE TABLE USERS_COMPETITIONS(
    CompetitionId INT,
    UserId INT,
    FOREIGN KEY (CompetitionId) REFERENCES COMPETITIONS(CompetitionId),
    FOREIGN KEY (UserId) REFERENCES USERS(UserId)
);

INSERT INTO USERS (Username, Email, Password, DateJoined)
VALUES ('User1', 'user1@example.com', 'password1', NOW());
INSERT INTO USERS (Username, Email, Password, DateJoined)
VALUES ('User2', 'user2@example.com', 'password2', NOW());
INSERT INTO USERS (Username, Email, Password, DateJoined)
VALUES ('User3', 'user3@example.com', 'password3', NOW());

INSERT INTO CREATORS (UserId)
VALUES (3);

INSERT INTO PLAYERS (UserId, League)
VALUES (1, "a");
INSERT INTO PLAYERS (UserId, League)
VALUES (2, "b");

INSERT INTO CARDS (BackText)
VALUES ('Random Card 1 Back Text');
INSERT INTO CARDS (BackText)
VALUES ('Random Card 2 Back Text');
INSERT INTO CARDS (BackText)
VALUES ('Random Card 3 Back Text');
INSERT INTO CARDS (BackText)
VALUES ('Random Card 4 Back Text');
INSERT INTO CARDS (BackText)
VALUES ('Random Card 5 Back Text');

INSERT INTO TEXT_CARDS (CardId, FrontText, BackText)
VALUES (1, 'Front Text for Text Card 1', 'Back Text for Text Card 1');
INSERT INTO TEXT_CARDS (CardId, FrontText, BackText)
VALUES (2, 'Front Text for Text Card 2', 'Back Text for Text Card 2');
INSERT INTO TEXT_CARDS (CardId, FrontText, BackText)
VALUES (3, 'Front Text for Text Card 3', 'Back Text for Text Card 3');

INSERT INTO PHOTO_CARDS (CardId, FrontImage, BackText)
VALUES (4, 'FrontImage1.jpg', 'Back Text for Photo Card 4');
INSERT INTO PHOTO_CARDS (CardId, FrontImage, BackText)
VALUES (5, 'FrontImage2.jpg', 'Back Text for Photo Card 5');

INSERT INTO LEADERBOARDS (CompetitionId)
VALUES (1);
INSERT INTO LEADERBOARDS (CompetitionId)
VALUES (2);

INSERT INTO TIME_LEADERBOARDS (LeaderboardId, UserId, Time, Place)
VALUES (2, 1, 5, 2);
INSERT INTO TIME_LEADERBOARDS (LeaderboardId, UserId, Time, Place)
VALUES (2, 2, 4, 1);

INSERT INTO SCORE_LEADERBOARDS (LeaderboardId, UserId, Score, Place)
VALUES (1, 1, 5, 1);
INSERT INTO SCORE_LEADERBOARDS (LeaderboardId, UserId, Score, Place)
VALUES (1, 2, 4, 2);

INSERT INTO COMPETITIONS (LeaderboardId, CompetitionType)
VALUES (1, 'SCORE');
INSERT INTO COMPETITIONS (LeaderboardId, CompetitionType)
VALUES (2, 'TIME');

INSERT INTO SCORE_COMPETITIONS (CompetitionId, LeaderboardId)
VALUES (1, 1);

INSERT INTO TIME_COMPETITIONS (CompetitionId, LeaderboardId, StartTime)
VALUES (2, 2, '2023-10-06 12:00:00');

INSERT INTO CARDSETS (CardsetId)
VALUES (1);

INSERT INTO CARDSETS_USERS (CardsetId, UserId)
VALUES (1, 3);

INSERT INTO CARDSETS_CARDS (CardsetId, CardId)
VALUES (1, 1);
INSERT INTO CARDSETS_CARDS (CardsetId, CardId)
VALUES (1, 2);
INSERT INTO CARDSETS_CARDS (CardsetId, CardId)
VALUES (1, 3);
INSERT INTO CARDSETS_CARDS (CardsetId, CardId)
VALUES (1, 4);
INSERT INTO CARDSETS_CARDS (CardsetId, CardId)
VALUES (1, 5);

INSERT INTO USERS_COMPETITIONS (CompetitionId, UserId)
VALUES (1, 1);
INSERT INTO USERS_COMPETITIONS (CompetitionId, UserId)
VALUES (1, 2);
INSERT INTO USERS_COMPETITIONS (CompetitionId, UserId)
VALUES (2, 1);
INSERT INTO USERS_COMPETITIONS (CompetitionId, UserId)
VALUES (2, 2);

-- Query 1: Find the top 10 users with the highest scores in a specific competition.

SELECT U.Username, SL.Score
FROM SCORE_LEADERBOARDS SL
JOIN USERS U ON SL.UserId = U.UserId
WHERE SL.LeaderboardId = @LeaderboardId
ORDER BY SL.Score DESC
LIMIT 10;

-- Query 2: Calculate the average score for all users in a specific competition.

SELECT AVG(SL.Score) AS AverageScore
FROM SCORE_LEADERBOARDS SL
WHERE SL.LeaderboardId = @LeaderboardId;

-- Query 3: Find creator of cardset

SELECT DISTINCT CU.UserId
FROM CARDSETS_USERS CU
WHERE CU.CardsetId = @CardsetId;

-- Query 4: Find the total number of players in each league.

SELECT P.League, COUNT(*) AS PlayerCount
FROM PLAYERS P
GROUP BY P.League;

-- Query 5: Select all competitions for user

SELECT UC.CompetitionId
FROM USERS_COMPETITIONS UC
WHERE UC.UserId = @UserId;

-- Query 6: Select list of cards in cardset

SELECT CC.CardId
FROM CARDSETS_CARDS CC
WHERE CC.CardsetId = @CardsetId;

-- Query 7: List the card sets that have the most cards in them.


SELECT CS.CardsetId, COUNT(*) AS CardCount
FROM CARDSETS_CARDS CS
GROUP BY CS.CardsetId
ORDER BY CardCount DESC
LIMIT 1;


-- Query 8: Calculate the average time taken by users in time-based competitions.

SELECT AVG(TL.Time) AS AverageTime
FROM TIME_LEADERBOARDS TL
JOIN USERS U ON TL.UserId = U.UserId
WHERE TL.LeaderboardId = @LeaderboardId;

-- Query 9: Show cardsets id which creators have created.

SELECT CREATORS.UserId AS CreatorID, CARDSETS_USERS.CardSetID
FROM CREATORS
JOIN CARDSETS_USERS ON CREATORS.UserId = CARDSETS_USERS.UserID;

-- Query 10: List top 5 biggest competitions

SELECT C.CompetitionId, C.CompetitionType, COUNT(UC.UserId) AS ParticipantCount
FROM COMPETITIONS C
JOIN USERS_COMPETITIONS UC ON C.CompetitionId = UC.CompetitionId
GROUP BY C.CompetitionId, C.CompetitionType
ORDER BY ParticipantCount DESC
LIMIT 5;

-- Query 11: Calculate the total number of cards created by each user.

SELECT U.UserId, U.Username, COUNT(*) AS TotalCardsCreated
FROM CREATORS C
JOIN USERS U ON C.UserId = U.UserId
GROUP BY U.UserId, U.Username;

-- Query 12: Find the users who have participated in all competitions.

SELECT U.UserId, U.Username, COUNT(UC.CompetitionId) AS NumberOfCompetitions
FROM USERS U
LEFT JOIN USERS_COMPETITIONS UC ON U.UserId = UC.UserId
GROUP BY U.UserId, U.Username;
