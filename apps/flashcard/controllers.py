from py4web import action, abort, redirect, request, URL
from yatl.helpers import A
from .common import auth, db, session


#
# GLOBALS
#


MAX_DECKS = 10


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
@action.uses("index.html", auth, auth.user)
def decks():
    return dict(
        vue_root='./js/components/test.js'
    )


#
# HELPER / UTILITY
#


def process_deck(row):
    # Reformat the 'modified' entry.
    row['modified'] = row['modified'].isoformat()

    # Get the number of cards associated with a deck.
    row['num_cards'] = db(
        db.card.deck_id == row.id
    ).count()

    # Get the tags associated with a deck.
    tags = db(db.tag.deck_id == row.id).select(db.tag.tag).as_list()
    if len(tags) > 0:
        row['tags'] = [r["tag"] for r in tags]
    else:
        row['tags'] = []

    # If signed in, display deck's favorited status by current user.
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
    # Get search parameters from GET request.
    # The 'search_string' is the search query; if blank, ignore.
    # The 'search_mode' determines whether the user is searching
    # for deck titles or deck authors.
    search_string = request.query.get('search')
    search_mode = request.query.get('mode')
    decks = []

    # The query that will be sent to the DAL.
    # Get all public decks that match the current search string.
    query = (
        (db.deck.public == True)
        if (search_string is None or len(search_string) == 0) else
        (db.deck.public == True) & (
            (db.deck.title.contains(search_string))
            if (search_mode == "title") else
            (db.deck.author.contains(search_string))
        )
    )

    # Iterate through queried decks.
    for row in db(query).iterselect(orderby=~db.deck.modified):
        if len(decks) >= MAX_DECKS:
            break
        decks.append(process_deck(row))

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
