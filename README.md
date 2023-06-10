# Flashcard - CSE 183 Team Project

[Project Repository](https://github.com/matthewchen146/cse-183-team-project)  

[Design Sketches](https://docs.google.com/document/d/1bG1MpbpZuVgnCje2CVgHCXiv5YPz7i0XJo8IA7Ov3ak/edit?usp=sharing)

Matthew Chen ([mchen146@ucsc.edu](mchen146@ucsc.edu))  
Jonathan Alvarez ([jalva100@ucsc.edu](jalva100@ucsc.edu))  
Nicholas Wong ([nwong17@ucsc.edu](nwong17@ucsc.edu))  
Michael Tan ([mtan42@ucsc.edu](mtan42@ucsc.edu))  
Benjamin Quang ([bquang@ucsc.edu](bquang@ucsc.edu))  

## About

### Description

**Flashcard** is a flashcard application where users create and view decks of flashcards, much like Quizlet.
In Flashcard, a user can create their own deck with their own cards for studying, or use the search to find, view, and favorite other user-created decks.
Cards have a front side and a back side, facilitating easy studying by flipping between the two sides.

### Features

This application comes with the following features:

- User-created decks
  - Users can create new decks with their own individual cards.
  - Users can modify and delete their own pre-existing decks and any individual card in the deck.
  - Users can set whether their spefific deck is public or private.
  - Users can view a deck and navigate and flip through its individual cards.
- Flexible search
  - Users can search for public decks based on the deck title, the author's username, or a specific tag applied to decks.
- Favoriting
  - Users can favorite decks for easier access to them.

## Technical Explanation

### Idea

As a team, we came up with and tried to followed these [design sketches](https://docs.google.com/document/d/1bG1MpbpZuVgnCje2CVgHCXiv5YPz7i0XJo8IA7Ov3ak/edit?usp=sharing).
They served as a good starting point for inspiration when we actually began to start implementing various features of our application.

### User Stories

The following user stories describe the features we aimed to implement:

- "As a user, I want to create a deck of flashcards to help me study a specific topic."
  - A user can create their own deck.
  - A user can add cards to their deck.
  - A user can add content to the front and back of a card.
  - A user can edit the deck title and description as well as the content of any card in the deck.
- "As a user, I want to search for decks created by other users to help me study."
  - A user can search for decks based on author username.
  - A user can search for decks based on a specific tag applied to a deck.
  - A user can search for decks based on deck title.
  - A user can combine different modes of search at once.
  - A user can view a deck and navigate through its cards.
- "As a user, I want to favorite specific decks so that I can return to them easily later."
  - A user can favorite and unfavorite decks.
- "As a user, I want to help others study as well by allowing my created deck to be findable in the search."
  - A user can set their decks to be either public (viewable to others) or private (viewable only to him or her).

### Models

The following database models were defined and used in ``models.py``:

- ``deck``
  - A table used to hold information regarding an individual deck of  cards.
  - Contains fields for the user ID of the author, the username of the author, the deck title, the deck description, whether or not the deck is "public" (visible to others when searching), a creation timestamp, and a last modified timestamp.
- ``card``
  - A table used to hold information regarding an individual card that belongs to a deck.
  - Contains fields for the deck ID that the card belongs in, the positional index of the card in the deck, the content on the front of the card, and the content on the back of the card.
- ``tag``
  - A many-to-one table used to hold user-defined tags for a deck.
  - Contains fields for the deck ID that the tag applies to and the tag itself.
- ``favorite``
  - A many-to-many table used to hold users' favorited decks.
  - Contains fields for a deck ID and the user ID of the user that favorited the deck.

### Controllers

``controllers.py`` is internally divided into three components: views, helper/utility, and API.

- In the view functions, these lead to Vue.js-styled templates with an associated ``vue_root`` to load the correct JavaScript file (see the next section **Templates** for more on this).
- Helper/utility functions are more-or-less self-explanatory; they are used by API calls (like fetchings tags for a specific deck) for cleaner, more organized code.
- API functions are used mainly for fetching/modifying things (like getting decks and cards, or editing tags) in the database via the database abstraction layer and form processing.

### Templates

Portions of this applicatation (like retrieving decks from the backend and viewing a specific deck) lean heavily into a [Vue.js-styled application](https://vuejs.org/guide/essentials/application.html).
These Vue-styled templates and associated JavaScript implementations are found in ``<root>/static/js/components``.
In these templates, JavaScript is used extensively to process a web page for the user's viewing, allowing for things like custom components (for instance, ``<deck-item>`` in ``home-template.html``) in the HTML.

Other portions of this application (like adding/editing cards and tags) follow the more traditional PY4WEB way of doing things, with controllers and templates working together to display the web page to the user and process the user's form data.

## Notes

- To ensure that there are not any application bugs caused by your browser loading something incorrectly, please open this application in an entirely new browser window. If you are encountering errors in the console and/or a web page appears broken, there is a possibility that your browser isn't loading something correctly (peer-reviewing student submissions in Crowdgrader was a good example of this, as the browser would sometimes load a different JavaScript file than what was provided in the student's submission).
