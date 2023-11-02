import os
from flask import Flask, render_template, request, Request
from typing import List, Optional, Tuple
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
                   "score_leaderboard": ["user_id", "score"],
                   "time_leaderboard": ["user_id", "time"]
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
    return render_template("maintenance.html", entities=ENTITIES)


@app.route('/maintenance/photo_card')
def get_photo_card_input():
    cardsets = {'cardset_ids': list(map(lambda x: Cardset(x).id, db.select_cardsets()))}
    return render_template("entity.html", fields=ENTITIES_FIELDS['photo_card'],
                           entity_name='photo_card',
                           select_fields=RELATION_FIELDS['photo_card'],
                           existed_relations=cardsets)

@app.route('/maintenance/text_card')
def get_text_card_input():
    cardsets = {'cardset_ids': list(map(lambda x: Cardset(x).id, db.select_cardsets()))}
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
    creators = {'creator_ids': list(map(lambda x: Creator(*x).id, db.select_creators()))}
    return render_template("entity.html", fields=ENTITIES_FIELDS['cardset'],
                           entity_name='cardset',
                           select_fields=RELATION_FIELDS['cardset'],
                           existed_relations=creators)

@app.route('/maintenance/time_competition')
def get_time_competition_input():
    players = {'player_ids': list(map(lambda x: Player(*x).id, db.select_players()))}
    return render_template("entity.html", fields=ENTITIES_FIELDS['time_competition'], entity_name='time_competition',
                           select_fields=RELATION_FIELDS['time_competition'],
                           existed_relations=players)

@app.route('/maintenance/score_competition')
def get_score_competition_input():
    players = {'player_ids': list(map(lambda x: Player(*x).id, db.select_players()))}
    return render_template("entity.html", fields=ENTITIES_FIELDS['score_competition'], entity_name='score_competition',
                           select_fields=RELATION_FIELDS['score_competition'],
                           existed_relations=players)

@app.route('/maintenance/score_leaderboard')
def get_score_leaderboard_input():
    competitions = {'competition_ids': list(map(lambda x: x[0], db.select_competitions()))}
    return render_template("entity.html", fields=ENTITIES_FIELDS['score_leaderboard'], entity_name='score_leaderboard',
                           select_fields=RELATION_FIELDS['score_leaderboard'],
                           existed_relations=competitions)

@app.route('/maintenance/time_leaderboard')
def get_time_leaderboard_input():
    competitions = {'competition_ids': list(map(lambda x: x[0], db.select_competitions()))}
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
