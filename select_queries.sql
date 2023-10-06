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

