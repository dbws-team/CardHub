import os
import random

from flask import Flask, render_template, request, Request
from typing import List, Optional, Tuple
# from modules.Database import SqlException, Database

app = Flask(__name__)
# db = Database(host=os.environ.get('DBWS_HOST'), user=os.environ.get('DBWS_USER'), password=os.environ.get('DBWS_PASSWORD'))

ENTITIES = ["photo_card", "text_card", "player", "creator", "cardset", "time_competition", "score_competition", "score_leaderboard", "time_leaderboard"]

ENTITIES_FIELDS = {"photo_card": ["url", "back_text"],
                   "text_card": ["front_text", "back_text"],
                   "player": ["username", "email", "password", "date_joined", "league"],
                   "creator": ["username", "email", "password", "date_joined"],
                   "cardset": ["name"],
                   "time_competition": ["start_time"],
                   "score_competition": [],
                   "score_leaderboard": ["leaderboard_id", "user_id", "score"],
                   "time_leaderboard": ["leaderboard_id", "user_id", "time"]
                   }

# ENTITIES_INSERT_FUNCTION = {'photo_card': db.insert_photo_card,
#                             'text_card': db.insert_text_card,
#                             'player': db.insert_player,
#                             'creator': db.insert_creator,
#                             'cardset': db.insert_cardset,
#                             'time_competition': db.insert_time_competition,
#                             'score_competition': db.insert_score_competition,
#                             'time_leaderboard': db.insert_time_leaderboard,
#                             'score_leaderboard': db.insert_score_leaderboard
#                             }

RELATION_FIELDS = {"photo_card": ["cardsets_name"], "text_card": ["cardsets_name"]}


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
    cardsets = {'cardset_name': []} # list(map(lambda x: x.name, db.select_cardsets()))}
    return render_template("entity.html", fields=ENTITIES_FIELDS['photo_card'],
                           entity_name='photo_card',
                           select_fields=RELATION_FIELDS['photo_card'],
                           existed_relations=cardsets)

@app.route('/maintenance/text_card')
def get_text_card_input():
    cardsets = {'cardset_name': []} # list(map(lambda x: x.name, db.select_cardsets()))}
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
    return render_template("entity.html", fields=ENTITIES_FIELDS['cardset'], entity_name='cardset')

@app.route('/maintenance/time_competition')
def get_time_competition_input():
    return render_template("entity.html", fields=ENTITIES_FIELDS['time_competition'], entity_name='time_competition')

@app.route('/maintenance/score_competition')
def get_score_competition_input():
    return render_template("entity.html", fields=ENTITIES_FIELDS['score_competition'], entity_name='score_competition')

@app.route('/maintenance/score_leaderboard')
def get_score_leaderboard_input():
    return render_template("entity.html", fields=ENTITIES_FIELDS['score_leaderboard'], entity_name='score_leaderboard')

@app.route('/maintenance/time_leaderboard')
def get_time_leaderboard_input():
    return render_template("entity.html", fields=ENTITIES_FIELDS['time_leaderboard'], entity_name='time_leaderboard')


def ensure_field_exists(entity: str, r: Request) -> Optional[Tuple[str, int]]:
    print(entity)
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
        assert(random.choice([1, 2, 3, 4, 5]) != 1)
        # ENTITIES_INSERT_FUNCTION[entity](**request.form)
    except AssertionError as e:
        return render_template('result.html', result=f'Failed: {e}')
    else:
        return render_template('result.html', result='Success')
