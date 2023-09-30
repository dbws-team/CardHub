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
