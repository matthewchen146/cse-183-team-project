"""
This file defines the database models
"""

from datetime import datetime

from .common import auth, db, Field
from pydal.validators import *


def add_test_user_and_data():
    """
    A testing function that adds a user "_test_user_1"
    and his deck of Spanish cards.
    """
    # Only add this test user if he doesn't exist yet.
    test_user_username = "_test_user_1"
    test_user_firstname = "Test"
    test_user_lastname = "User"
    exists = db(db.auth_user.username == test_user_username).count()
    if not exists:
        print("Adding test user w/ test data.")
        user = dict(
            username=test_user_username,
            email=test_user_username + "@example.com",
            first_name=test_user_firstname,
            last_name=test_user_lastname,
            password=test_user_username
        )
        auth.register(user)

        # Get this test user's ID.
        user_id = (
            db(
                db.auth_user.username == test_user_username
            ).select(
                db.auth_user.id
            ).as_list()[0]["id"]
        )

        # Add this user's Spanish deck.
        test_deck = dict(
            title="Spanish terms",
            description="A list of Spanish terms for me to memorize.",
            public=True,
            author=user_id
        )
        db.deck.insert(**test_deck)

        # Add three Spanish cards.
        deck_id = db(
            db.deck.author == user_id
        ).select(
            db.deck.id
        ).as_list()[0]["id"]
        test_card_1 = dict(
            deck_id=deck_id,
            index=1,
            front="hola",
            back="hello",
        )
        test_card_2 = dict(
            deck_id=deck_id,
            index=2,
            front="good morning",
            back="buenos dias",
        )
        test_card_3 = dict(
            deck_id=deck_id,
            index=3,
            front="Donde está el baño?",
            back="Where is the bathroom?",
        )
        db.card.insert(**test_card_1)
        db.card.insert(**test_card_2)
        db.card.insert(**test_card_3)
    db.commit()
    return


# A deck, with a title and description.
db.define_table(
    "deck",
    Field("author", "reference auth_user"),  # User ID.
    Field("title", "string"),                # The name of the deck.
    Field("description", "string"),          # A description of the deck.
    Field("public", "boolean"),              # Whether the deck is public.
    Field("created", "datetime", default=lambda: datetime.utcnow()),
    Field("modified", "datetime", default=lambda: datetime.utcnow())
)

# An individual card, with a front and back side.
# Multiple cards make up a deck (many-to-one table).
db.define_table(
    "card",
    Field("deck_id", "reference deck"),  # The associated deck.
    Field("index", "integer"),           # The card's place in the deck.
    Field("front", "string"),            # The content on the card's front.
    Field("back", "string"),             # The content on the card's back.
)

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

# A user's favorite decks (many-to-many table).
db.define_table(
    "favorite",
    Field("deck_id", "reference deck"),
    Field("user_id", "reference auth_user")
)

# This adds a test user and data.
# Uncomment if necessary.
add_test_user_and_data()

db.commit()
