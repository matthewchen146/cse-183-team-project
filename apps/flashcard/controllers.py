from py4web import action, abort, redirect, request, URL
from yatl.helpers import A
from py4web.utils.form import Form, FormStyleBulma
from .common import auth, db, session


#
# GLOBALS
#


MAX_DECKS = 10


#
# VIEWS
#


# The home (index) page.
@action("index")
@action.uses("generic.html", auth)
def index():
    return dict(
        
        vue_root='./static/js/components/home.js'
    )


# The page to view an individual deck.
@action("deck/<deck_id:int>")
@action.uses("generic.html", auth)
def deck(deck_id):
    return dict(
        deckId=deck_id,
        vue_root='./static/js/components/view-deck.js',
        
    )


# The decks page
@action("decks")
@action.uses("generic.html", auth, auth.user)
def decks():
    return dict(
        vue_root='./static/js/components/test.js'
    )


#
# HELPER / UTILITY
#


def get_decks_from_tag(tag):
    # Gets decks tagged with a specific tag.
    decks = db(db.tag.tag == tag).select(db.tag.deck_id).as_list()
    if len(decks) > 0:
        return [deck["deck_id"] for deck in decks]
    return []


def get_tags_from_deck(row):
    # Gets tags associated with a deck.
    tags = db(db.tag.deck_id == row.id).select(db.tag.tag).as_list()
    if len(tags) > 0:
        return [tag["tag"] for tag in tags]
    return []


def process_deck(row):
    # Reformat the 'modified' entry.
    row['modified'] = row['modified'].isoformat()

    # Get the number of cards associated with a deck.
    row['num_cards'] = db(
        db.card.deck_id == row.id
    ).count()

    # Get the tags associated with a deck.
    row['tags'] = get_tags_from_deck(row)

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
    search_mode = request.query.get('mode').split("+")
    decks = []

    # The query that will be sent to the DAL.
    # Get all decks that match the current search mode(s).
    query_modes = []
    if search_string is not None and len(search_string) > 0:
        if "title" in search_mode:
            query_modes.append(
                (db.deck.title.contains(search_string))
            )
        if "author" in search_mode:
            query_modes.append(
                (db.deck.author.contains(search_string))
            )
        if "tag" in search_mode:
            query_modes.append(
                (db.deck.id.belongs(get_decks_from_tag(search_string)))
            )

    # Construct the mode portion of the query.
    query_mode = None
    for q in query_modes:
        if query_mode is None:
            query_mode = q
            continue
        query_mode |= q

    # Construct the entire query.
    # This is done to establish higher order so that public decks
    # are prioritized. In other words, all of this does the following:
    # ``query & (query_mode_1 | query_mode_2 | ...)``
    if query_mode is not None:
        query = (db.deck.public == True) & (query_mode)
    else:
        query = (db.deck.public == True)

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

# Get cards to display.
@action("get_cards", method="GET")
@action.uses(auth, db)
def get_cards(deck_id=None):
    deck_id= request.query.get('deck_id')
    print("fetching a deck with the ID ",deck_id)
    # Make sure a valid deck ID is provided
    

    # Query the database for cards associated with the deck ID
    cards = db(db.card.deck_id == deck_id).select().as_list()
    for card in cards:
        card['isFront'] = True
    
    

    # Return the cards as a dictionary
    return dict(cards=cards)

@action("get_deck", method="GET")
@action.uses(auth, db)
def get_deck(deck_id=None):
    deck_id = request.query.get('deck_id')
    print("fetching a deck with the ID", deck_id)

    # Make sure a valid deck ID is provided

    # Query the database for the deck
    deck = db(db.deck.id == deck_id).select().first()

    if deck:
        # Check if the deck is favorited by the user
        is_favorited = bool(
            db(
                (db.favorite.deck_id == deck.id) &
                (db.favorite.user_id == auth.user_id)
            ).count()
        )
        deck["is_favorited"] = is_favorited

    

    # Return the deck as a dictionary
    return dict(deck=deck)

# Edit the selected deck's title, description and public toggle
# Also updates Save Status
@action("edit/<deck_id:int>", method=['GET', 'POST'])
@action.uses(db, session, auth.user, "edit.html")
def edit_deck(deck_id=None):
    assert deck_id is not None
    d = db.deck[deck_id]
    if d is None:
        redirect(URL("index"))
    status = "N/A"
    form = Form(db.deck, record=d, deletable=False, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        status = "Saved"
    rows = db(db.card.deck_id == deck_id).select()
    tag_rows = db(db.tag.deck_id == deck_id).select()
    return dict(form=form, rows=rows, deck_id=deck_id, tag_rows=tag_rows, status=status)

# Edit the selected tag
@action("edit_tag/<deck_id:int>/<tag_id:int>", method=['GET', 'POST'])
@action.uses(db, session, auth.user, "edit_tag.html")
def edit_tag(deck_id=None, tag_id=None):
    assert deck_id is not None
    assert tag_id is not None
    t = db.tag[tag_id]
    tag_form = Form(db.tag, record=t, deletable=False, csrf_session=session, formstyle=FormStyleBulma)
    if tag_form.accepted:
        redirect(URL("edit", deck_id))
    return dict(tag_form=tag_form)

# Delete the selected tag
@action('delete_tag/<deck_id:int>/<tag_id:int>')
@action.uses(db, 'delete_tag.html', auth.user)
def delete_tag(deck_id=None, tag_id=None):
    assert deck_id is not None
    assert tag_id is not None
    db(db.tag.id == tag_id).delete()
    redirect(URL('edit', deck_id))

# Edit the selected card's front and back
@action('edit_card/<deck_id:int>/<card_id:int>')
@action.uses(db, 'edit_card.html', auth.user)
def edit_card(deck_id=None, card_id=None):
    assert deck_id is not None
    assert card_id is not None
    c = db.card[card_id]
    form = Form(db.card, record=c, deletable=False, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL("edit", deck_id))
    return dict(form=form)

#Add a tag
@action('add_tag/<deck_id:int>', method=["GET", "POST"])
@action.uses(db, 'add_tag.html', auth.user)
def add_phone(deck_id=None):
    assert deck_id is not None
    d = db.tag[deck_id]
    form = Form(db.tag, record=d, deletable=False, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        db.card.insert(tag=form.vars['tag'], deck_id=deck_id)
        redirect(URL("edit", deck_id))
    return dict(form=form)

# Delete the selected card
@action('delete_card/<deck_id:int>/<card_id:int>')
@action.uses(db, 'delete_card.html', auth.user)
def delete_card(deck_id=None, card_id=None):
    assert deck_id is not None
    assert card_id is not None
    db(db.card.id == card_id).delete()
    redirect(URL('edit', deck_id))

# Add a card
@action('add_card/<deck_id:int>', method=["GET", "POST"])
@action.uses(db, 'add_card.html', auth.user)
def add_phone(deck_id=None):
    assert deck_id is not None
    d = db.card[deck_id]
    form = Form(db.card, record=d, deletable=False, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        db.card.insert(front=form.vars['front'], back=form.vars['back'], deck_id=deck_id)
        redirect(URL("edit", deck_id))
    return dict(form=form)





