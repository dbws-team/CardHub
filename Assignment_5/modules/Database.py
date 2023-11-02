import mysql.connector
from mysql.connector import errorcode
from dataclasses import dataclass
import datetime

VERBOSE = True


class SqlException(Exception):
    def __init__(self, error: mysql.connector.Error, context: str):
        super().__init__(f'MYSQL EXCEPTION: f{str(error)}')
        self.error = error
        self.context = context

@dataclass
class Player:
    id: int
    league: str

@dataclass
class Creator:
    id: int

@dataclass
class TextCard:
    id: int
    front_text: str
    back_text: str

@dataclass
class PhotoCard:
    id: int
    back_text: str
    front_photo_url: str

@dataclass
class Cardset:
    id: int

@dataclass
class TimeCompetition:
    id: int
    start_time: datetime.datetime

@dataclass
class ScoreCompetition:
    id: int

@dataclass
class TimeLeaderboard:
    id: int
    user_id: int
    time: datetime.datetime

@dataclass
class ScoreLeaderboard:
    id: int
    user_id: int
    score: int

class Database:
    def __init__(self, user: str, password: str, host: str = 'localhost', port: int = 3306, database='dbws'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.users = 0
        self.leaderboards = 0
        self.competitions = 0
        self.cards = 0
        self.cardsets = 0

    def execute_query(self, _query: str, context: str, flag: bool):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password, autocommit=True, database=self.database)
            cursor = connection.cursor()

            _query = f'{_query}'
            cursor.execute(_query)
            if flag:
                res = cursor.fetchall()
                cursor.close()
                connection.close()
                return res
            else:
                cursor.close()
                connection.close()
        except mysql.connector.Error as err:
            raise SqlException(error=err, context=context)

    def insert_text_card(self, card_id, front_text, back_text):
        return f"INSERT INTO TEXT_CARDS (CardId, FrontText, BackText) VALUES ('{card_id}', '{front_text}', '{back_text}');"

    def insert_photo_card(self, card_id, front_photo_url, back_text):
        return f"INSERT INTO PHOTO_CARDS (CardId, FrontText, BackText) VALUES ('{card_id}', '{front_photo_url}', '{back_text}');"

    def insert_player(self, user_id, league):
        return f"INSERT INTO PLAYERS (UserId, League) VALUES ('{user_id}', '{league}');"

    def insert_creator(self, user_id):
        return f"INSERT INTO CREATORS (UserId) VALUES ('{user_id}');"

    def insert_cardset(self):
        return f"INSERT INTO CARDSETS () VALUES ();"

    def insert_score_competitions(self, competition_id, leaderboard_id):
        return f"INSERT INTO SCORE_COMPETITIONS (CompetitionId, LeaderboardId) VALUES ('{competition_id}', '{leaderboard_id}');"

    def insert_time_competitions(self, competition_id, leaderboard_id, start_time):
        return f"INSERT INTO TIME_COMPETITIONS (CompetitionId, LeaderboardId, StartTime) VALUES ('{competition_id}', '{leaderboard_id}', '{start_time}');"

    def insert_score_leaderboards(self, leaderboard_id, user_id, score, place):
        return f"INSERT INTO SCORE_LEADERBOARDS (LeaderboardId, UserId, Score, Place) VALUES ('{leaderboard_id}', '{user_id}', '{score}', '{place}');"

    def insert_time_leaderboards(self, leaderboard_id, user_id, time, place):
        return f"INSERT INTO TIME_LEADERBOARDS (LeaderboardId, UserId, Time, Place) VALUES ('{leaderboard_id}', '{user_id}', '{time}', '{place}');"

    def insert_card(self, back_text):
        return f"INSERT INTO CARDS (BackText) VALUES ('{back_text}');"

    def insert_user(self, username, email, password, date_joined):
        return f"INSERT INTO USERS (Username, Email, Password, DateJoined) VALUES ('{username}', '{email}', '{password}', '{date_joined}');"

    def insert_leaderboard(self, competition_id):
        return f"INSERT INTO LEADERBOARDS (CompetitionId) VALUES ('{competition_id}');"

    def insert_competiton(self, leaderboard_id, competition_type):
        return f"INSERT INTO COMPETITIONS(LeaderboardId, CompetitionType) VALUES('{leaderboard_id}', '{competition_type}');"

    def create_photo_card(self, front_photo_url, back_text, cardset_id):
        self.execute_query(self.insert_card(back_text), 'Insert card', False)
        self.cards += 1
        self.execute_query(self.insert_photo_card(self.cards, front_photo_url, back_text), 'Insert PhotoCard', False)
        self.execute_query(f"INSERT INTO CARDSETS_CARDS (CardsetId, CardId) VALUES ('{cardset_id}', '{self.cards}');",
                           "Add cardset", False)

    def create_text_card(self, front_text, back_text, cardset_id):
        self.execute_query(self.insert_card(back_text), 'Insert card', False)
        self.cards += 1
        self.execute_query(self.insert_text_card(self.cards, front_text, back_text), 'Insert TextCard', False)
        self.execute_query(f"INSERT INTO CARDSETS_CARDS (CardsetId, CardId) VALUES ('{cardset_id}', '{self.cards}');",
                           "Add cardset", False)
    def create_player(self, username, email, password, date_joined, league):
        self.execute_query(self.insert_user(username, email, password, date_joined), 'Insert User', False)
        self.users += 1
        self.execute_query(self.insert_player(self.users, league), 'Insert Player', False)

    def create_creator(self, username, email, password, date_joined):
        self.execute_query(self.insert_user(username, email, password, date_joined), 'Insert User', False)
        self.users += 1
        self.execute_query(self.insert_creator(self.users), 'Insert Creator', False)

    def create_cardset(self, creator_id):
        self.execute_query(self.insert_cardset(), 'Insert Cardset', False)
        self.cardsets += 1
        self.execute_query(f"INSERT INTO CARDSETS_USERS (CardsetId, UserId) VALUES ('{self.cardsets}', '{creator_id}');", "Add creator", False)

    def create_score_leaderboard(self, competition_id):
        self.execute_query(self.insert_leaderboard(competition_id), 'Insert Leaderboard', False)
        self.leaderboards += 1

    def create_time_leaderboard(self, competition_id):
        self.execute_query(self.insert_leaderboard(competition_id), 'Insert Leaderboard', False)
        self.leaderboards += 1

    def create_time_competition(self, leaderboard_id, start_time, player_id):
        self.execute_query(self.insert_competiton(leaderboard_id, 'TIME'), 'Insert Competition', False)
        self.competitions += 1
        self.execute_query(self.insert_time_competitions(self.competitions, leaderboard_id, start_time), 'Insert TimeCompetition', False)
        self.execute_query(f"INSERT INTO USERS_COMPETITIONS (CompetitionId, UserId) VALUES ({self.competitions}, {player_id});", "", False)

    def create_score_competition(self, leaderboard_id, player_id):
        self.execute_query(self.insert_competiton(leaderboard_id, 'SCORE'), 'Insert Competition', False)
        self.competitions += 1
        self.execute_query(self.insert_score_competitions(self.competitions, leaderboard_id), 'Insert ScoreCompetition', False)
        self.execute_query(f"INSERT INTO USERS_COMPETITIONS (CompetitionId, UserId) VALUES ({self.competitions}, {player_id});", "", False)

    def select_cardsets(self):
        return self.execute_query("select * from CARDSETS", "Selecting cardsets", True)

    def select_creators(self):
        return self.execute_query("select * from CREATORS", "Selecting creators", True)

    def select_players(self):
        return self.execute_query("select * from PLAYERS", "Selecting players", True)

    def select_competitions(self):
        return self.execute_query("select * from COMPETITIONS", "Selecting competitions", True)
