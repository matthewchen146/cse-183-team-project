from py4web import action, abort, redirect, request, URL
from yatl.helpers import A
from .common import auth, db, session


#
# VIEWS
#


# The home page.
@action("index")
@action.uses("index.html", auth)
def index():
    return dict(
        vue_root='./js/components/home.js'
    )


# The decks page
@action("decks")
@action.uses("index.html", auth)
def decks():
    return dict(
        vue_root='./js/components/test.js'
    )


#
# HELPER / UTILITY
#


def process_deck(row):
    row['modified'] = row['modified'].isoformat()
    if auth.get_user() != {}:
        row['is_favorite'] = bool(
            db(
                (db.favorite.deck_id == row.id) &
                (db.favorite.user_id == auth.user_id)
            ).count()
        )

    return row


#
# API
#


# Get decks to display.
@action("get_decks", method="GET")
@action.uses(auth, db)
def get_decks():

    max_decks = 10
    search_string = request.query.get('search')

    decks = []

    if search_string is None or len(search_string) == 0:
        for row in db(db.deck.public == True).iterselect():
            if len(decks) >= max_decks:
                break
            deck = process_deck(row)
            decks.append(deck)

    return dict(
        decks=decks
    )


# Toggle deck favorite status of the current user.
@action("set_favorite", method="POST")
@action.uses(auth.user, db)
def set_favorite():
    # Get the following variables from the POST request.
    deck_id = request.json.get('deck_id')
    is_favorite = request.json.get('is_favorite')

    # The query that will be sent to the DAL.
    # Get all favorited decks by the current user.
    query = (
        (db.favorite.user_id == auth.user_id) &
        (db.favorite.deck_id == deck_id)
    )

    # Toggles deck favoriting; if not favorited, favorite it.
    # Otherwise, remove the favorite from the database.
    if is_favorite:
        if not db(query).count():
            db.favorite.insert(
                deck_id=deck_id,
                user_id=auth.user_id
            )
    else:
        db(query).delete()

    return dict(
        message='successfully toggled favorite',
        is_favorite=is_favorite
    )
