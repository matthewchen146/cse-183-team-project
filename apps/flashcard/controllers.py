"""

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash

# views

# home page
@action("index")
@action.uses("index.html", auth)
def index():
    
    

    return dict(
        vue_root = './js/components/home.js'
    )

# decks page
@action("decks")
@action.uses("index.html", auth)
def index():
    
    return dict(
        vue_root = './js/components/test.js'
    )


# util
def process_deck(row):

    row['modified'] = row['modified'].isoformat()

    if auth.get_user() != {}:
        row['is_favorite'] = bool(db((db.favorite.deck_id == row.id) & (db.favorite.user_id == auth.user_id)).count())

    return row


# api

# return a list of decks with their meta information
@action("get_decks", method="GET")
@action.uses(db, auth)
def get_decks():

    max_decks = 10
    
    search_string = request.query.get('search')

    decks = []

    if search_string == None or len(search_string) == 0:
        for row in db(db.deck.public == True).iterselect():
            if len(decks) >= max_decks:
                break
            deck = process_deck(row)
            decks.append(deck)

    return dict(
        decks = decks
    )

@action("set_favorite", method="POST")
@action.uses(db, auth.user)
def set_favorite():

    data = request.json
    deck_id = data.get('deck_id')
    is_favorite = data.get('is_favorite')

    query = (db.favorite.user_id == auth.user_id) & (db.favorite.deck_id == deck_id)
    if is_favorite:
        if not db(query).count():
            db.favorite.insert(
                deck_id = deck_id,
                user_id = auth.user_id
            )
    else:
        db(query).delete()
    return dict(message = 'successfully set favorite', is_favorite = is_favorite)

    