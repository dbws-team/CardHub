import os
from flask import Flask, render_template, request, Request
from typing import List, Optional, Tuple, Callable, Dict
from modules.Database import *

app = Flask(__name__)
db = Database(host=os.environ.get('DBWS_HOST'), user=os.environ.get('DBWS_USER'), password=os.environ.get('DBWS_PASSWORD'), database='Group-7')

ENTITIES = ["photo_card", "text_card", "player", "creator", "cardset", "time_competition", "score_competition", "score_leaderboard", "time_leaderboard"]

ENTITIES_FIELDS = {"photo_card": ["url", "back_text"],
                   "text_card": ["front_text", "back_text"],
                   "player": ["username", "email", "password", "date_joined", "league"],
                   "creator": ["username", "email", "password", "date_joined"],
                   "cardset": [],
                   "time_competition": ["start_time", "leaderboard_id"],
                   "score_competition": ["leaderboard_id"],
                   "score_leaderboard": [],
                   "time_leaderboard": []
                   }

ENTITIES_INSERT_FUNCTION = {'photo_card': db.create_photo_card,
                            'text_card': db.create_text_card,
                            'player': db.create_player,
                            'creator': db.create_creator,
                            'cardset': db.create_cardset,
                            'time_competition': db.create_time_competition,
                            'score_competition': db.create_score_competition,
                            'time_leaderboard': db.create_time_leaderboard,
                            'score_leaderboard': db.create_score_leaderboard
                            }

RELATION_FIELDS = {"photo_card": ["cardset_id"],
                   "text_card": ["cardset_id"],
                   "player": [],
                   "creator": [],
                   "cardset": ["creator_id"],
                   "time_competition": ["player_id"],
                   "score_competition": ["player_id"],
                   "score_leaderboard": ["competition_id"],
                   "time_leaderboard": ["competition_id"]
                   }


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/disclaimer')
def disclaimer():
    return render_template('disclaimer.html')


@app.route('/form_submit', methods=['POST'])
def print_submitted():
    d = dict(request.form)
    return d


@app.route('/maintenance')
def maintenance_page():
    return render_template("maintenance.html", entities=ENTITIES, search_queries=SEARCH_QUERIES_NAME)


@app.route('/maintenance/photo_card')
def get_photo_card_input():
    cardsets = {'cardset_id': list(map(lambda x: Cardset(*x).id, db.select_cardsets()))}
    return render_template("entity.html", fields=ENTITIES_FIELDS['photo_card'],
                           entity_name='photo_card',
                           select_fields=RELATION_FIELDS['photo_card'],
                           existed_relations=cardsets)

@app.route('/maintenance/text_card')
def get_text_card_input():
    cardsets = {'cardset_id': list(map(lambda x: Cardset(*x).id, db.select_cardsets()))}
    return render_template("entity.html", fields=ENTITIES_FIELDS['text_card'],
                           entity_name='text_card',
                           select_fields=RELATION_FIELDS['text_card'],
                           existed_relations=cardsets)

@app.route('/maintenance/player')
def get_player_input():
    return render_template("entity.html", fields=ENTITIES_FIELDS['player'], entity_name='player')

@app.route('/maintenance/creator')
def get_creator_input():
    return render_template("entity.html", fields=ENTITIES_FIELDS['creator'], entity_name='creator')

@app.route('/maintenance/cardset')
def get_cardset_input():
    print(db.select_creators())
    creators = {'creator_id': list(map(lambda x: Creator(*x).id, db.select_creators()))}
    return render_template("entity.html", fields=ENTITIES_FIELDS['cardset'],
                           entity_name='cardset',
                           select_fields=RELATION_FIELDS['cardset'],
                           existed_relations=creators)

@app.route('/maintenance/time_competition')
def get_time_competition_input():
    players = {'player_id': list(map(lambda x: Player(*x).id, db.select_players()))}
    return render_template("entity.html", fields=ENTITIES_FIELDS['time_competition'], entity_name='time_competition',
                           select_fields=RELATION_FIELDS['time_competition'],
                           existed_relations=players)

@app.route('/maintenance/score_competition')
def get_score_competition_input():
    players = {'player_id': list(map(lambda x: Player(*x).id, db.select_players()))}
    return render_template("entity.html", fields=ENTITIES_FIELDS['score_competition'], entity_name='score_competition',
                           select_fields=RELATION_FIELDS['score_competition'],
                           existed_relations=players)

@app.route('/maintenance/score_leaderboard')
def get_score_leaderboard_input():
    competitions = {'competition_id': list(map(lambda x: x[0], db.select_competitions()))}
    return render_template("entity.html", fields=ENTITIES_FIELDS['score_leaderboard'], entity_name='score_leaderboard',
                           select_fields=RELATION_FIELDS['score_leaderboard'],
                           existed_relations=competitions)

@app.route('/maintenance/time_leaderboard')
def get_time_leaderboard_input():
    competitions = {'competition_id': list(map(lambda x: x[0], db.select_competitions()))}
    return render_template("entity.html", fields=ENTITIES_FIELDS['time_leaderboard'], entity_name='time_leaderboard',
                           select_fields=RELATION_FIELDS['time_leaderboard'],
                           existed_relations=competitions)


def ensure_field_exists(entity: str, r: Request) -> Optional[Tuple[str, int]]:
    for field in ENTITIES_FIELDS[entity]:
        if field not in r.form:
            return f"Can't find field {field} in form", 400

    for field in RELATION_FIELDS[entity]:
        if field not in r.form:
            return f"Can't find field {field} in form", 400
    if ENTITIES_FIELDS[entity] + RELATION_FIELDS[entity] != list(r.form.keys()):
        return "Not only fields", 400
    return None


@app.route('/maintenance/<entity>/submit', methods=["POST"])
def submit(entity):
    if entity not in ENTITIES:
        return "unknown entity", 400
    verify_result = ensure_field_exists(entity, request)
    if verify_result is not None:
        return verify_result

    try:
        ENTITIES_INSERT_FUNCTION[entity](**request.form)
    except SqlException as e:
        return render_template('result.html', result=f'Failed: {e}')
    else:
        return render_template('result.html', result='Success')

@dataclass
class Parameter:
    name: str
    desc: str


@dataclass
class SearchQuery:
    name: str
    description: str
    params: List[Parameter]
    exec_func: Callable
    details_id: str
    object_name: str

def get_all_cards(cardset_id):
    return list(map(lambda x: Card(*x), db.select_cards(int(cardset_id))))

def get_creator(cardset_id):
    return list(map(lambda x: Creator(*x), db.select_creator(int(cardset_id))))

def get_competitions(player_id):
    return list(map(lambda x: Competition(*x), db.select_competitions_for_player(int(player_id))))

def get_users_from_all_competitions():
    return list(map(lambda x: UserAndCompetitions(*x), db.select_users_from_all_competitions()))

SEARCH_QUERIES: Dict[str, SearchQuery] = {
    'cards_from_cardset':
        SearchQuery(name='cards_from_cardset',
                    description='Select list of cards in cardset',
                    params=[Parameter(name='cardset_id',
                                      desc='CardsetId')],
                    exec_func=get_all_cards,
                    details_id='id',
                    object_name='card'
                    ),
    'creator_from_cardset':
        SearchQuery(name='creator_from_cardset',
                    description='Select creator of cardset',
                    params=[Parameter(name='cardset_id',
                                      desc='CardsetId')],
                    exec_func=get_creator,
                    details_id='id',
                    object_name='creator'
                    ),
    'competitions_from_player':
        SearchQuery(name='competitions_from_player',
                    description='Select all competitions for user',
                    params=[Parameter(name='player_id',
                                      desc='PlayerId')],
                    exec_func=get_competitions,
                    details_id='id',
                    object_name='competitions'
                    ),
    'users_from_all_competitions':
        SearchQuery(name='users_from_all_competitions',
                    description='Find the users who have participated in all competitions.',
                    params=[],
                    exec_func=get_users_from_all_competitions,
                    details_id='id',
                    object_name='users'
                    ),
}
SEARCH_QUERIES_NAME: List[str] = list(SEARCH_QUERIES.keys())
ORDER_HEADERS: Dict[str, List[str]] = {
    'cards_from_cardset': ["id"],
    'creator_from_cardset': ["id"],
    'competitions_from_player': ["id"],
    'users_from_all_competitions': ["id", "username", "number"]
}
RESULT_HEADERS = {
    'cards_from_cardset': ["card id"],
    'creator_from_cardset': ["user id"],
    'competitions_from_player': ["competition id"],
    'users_from_all_competitions': ["user id", "username", "number of competitions"]
}


def ensure_search_field_exists(query: str, r: Request) -> Optional[Tuple[str, int]]:
    for param in SEARCH_QUERIES[query].params:
        if param.name not in r.form:
            return f"Can't find field {param.name} in form", 400
    if len(SEARCH_QUERIES[query].params) != len(list(r.form.keys())):
        return "Not only fields", 400
    return None


def get_rows(name: str, result):
    return [[row.__dict__[param] for param in ORDER_HEADERS[name]] for row in result]


@app.route('/maintenance/search/<query>/submit', methods=['POST'])
def show_search_result(query):
    if query not in SEARCH_QUERIES_NAME:
        return 'Unknown query', 400

    res = ensure_search_field_exists(query, request)
    if res is not None:
        return res
    try:
        print(SEARCH_QUERIES[query].exec_func(**request.form))
        return render_template("search_result.html",
                               headers=RESULT_HEADERS[query],
                               query=SEARCH_QUERIES[query],
                               order=ORDER_HEADERS[query],
                               result=SEARCH_QUERIES[query].exec_func(**request.form))
    except SqlException as e:
        return render_template("insert_result.html", result=e)


@app.route('/maintenance/search/<query>')
def search_query(query):
    if query not in SEARCH_QUERIES_NAME:
        return 'Unknown query', 400

    return render_template("search_query.html", query=SEARCH_QUERIES[query])