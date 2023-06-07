"""
This file defines the database models
"""
import random

from datetime import datetime, timedelta

from .common import auth, db, Field
from py4web.utils.populate import FIRST_NAMES, LAST_NAMES, IUP
from pydal.validators import *


def add_test_user_and_data():
    """
    A testing function that adds a user and test data.
    """
    # Only add this test user if he doesn't exist yet.
    test_user_firstname = random.choice(FIRST_NAMES)
    test_user_lastname = random.choice(LAST_NAMES)
    test_user_username = "_" + test_user_firstname + "_" + test_user_lastname
    exists = db(db.auth_user.username == test_user_username).count()

    if exists:
        return

    print(f"Adding test user {test_user_username} w/ test data.")
    user = dict(
        username=test_user_username,
        email=test_user_username + "@example.com",
        first_name=test_user_firstname,
        last_name=test_user_lastname,
        password=test_user_username
    )
    user_id = auth.register(user)

    # Generate between 1 and 5 decks.
    ts = datetime.utcnow()
    for _ in range(random.randint(1, 5)):
        # Taken from the Assignment 5 starter code.
        ts -= timedelta(seconds=random.uniform(60, 1000))

        # Add this deck into the database.
        test_deck = dict(
            title=" ".join(random.choices(list(IUP.keys()), k=3)),
            description=" ".join(random.choices(list(IUP.keys()), k=20)),
            public=True,
            user_id=user_id,
            author=test_user_username,
            created=ts,
            modified=ts
        )
        deck_id = db.deck.insert(**test_deck)

        # Generate a random amount of cards for the deck.
        for j in range(random.randint(1, 10)):
            db.card.insert(
                deck_id=deck_id,
                index=j,
                front=" ".join(random.choices(list(IUP.keys()), k=2)),
                back=" ".join(random.choices(list(IUP.keys()), k=11)),
            )

        # Generate a few tags for the deck.
        for j in range(random.randint(0, 5)):
            db.tag.insert(
                deck_id=deck_id,
                tag=" ".join(random.choices(list(IUP.keys()), k=1))
            )

    db.commit()
    return


# A deck, with a title and description.
db.define_table(
    "deck",
    Field("user_id", "reference auth_user"),  # User ID.
    Field("author", "string"),                # Author username.
    Field("title", "string"),                 # The name of the deck.
    Field("description", "string"),           # A description of the deck.
    Field("public", "boolean"),               # Whether the deck is public.
    Field("created", "datetime", default=lambda: datetime.utcnow()),
    Field("modified", "datetime", default=lambda: datetime.utcnow())
)

db.deck.user_id.writable = db.deck.user_id.readable = False
db.deck.id.writable = db.deck.id.readable = False
db.deck.author.writable = db.deck.author.readable = False
db.deck.created.writable = db.deck.created.readable = False
db.deck.modified.writable = db.deck.modified.readable = False

# An individual card, with a front and back side.
# Multiple cards make up a deck (many-to-one table).
db.define_table(
    "card",
    Field("deck_id", "reference deck"),  # The associated deck.
    Field("index", "integer"),           # The card's place in the deck.
    Field("front", "string"),            # The content on the card's front.
    Field("back", "string"),             # The content on the card's back.
)

db.card.index.writable = db.card.index.readable = False
db.card.id.writable = db.card.id.readable = False
db.card.deck_id.writable = db.card.deck_id.readable = False

# Users can mark cards with difficulties.
db.define_table(
    "difficulty",
    Field("user_id", "reference auth_user"),
    Field("deck_id", "reference deck"),
    Field("card_id", "reference card"),
    Field("difficulty", "string")             # The difficulty of the card.
)

# Decks can have tags.
db.define_table(
    "tag",
    Field("deck_id", "reference deck"),
    Field("tag", "string")
)

db.tag.deck_id.writable = db.tag.deck_id.readable = False
db.tag.id.writable = db.tag.id.readable = False

# A user's favorite decks (many-to-many table).
db.define_table(
    "favorite",
    Field("deck_id", "reference deck"),
    Field("user_id", "reference auth_user")
)

db.commit()

db(db.auth_user.username.startswith("_")).delete()
# db(db.card).delete()
# db(db.deck).delete()

for _ in range(10):
    # This adds a test user and data.
    # Uncomment if necessary.
    add_test_user_and_data()
