import csv
from pathlib import Path
from datetime import date, datetime
from typing import List


from games.adapters.repository import Repository
from games.domainmodel import Game, Genre, User, Publisher, Review, Wishlist

# Abstract Repository - need to add more

class Repository:

    def fetch_game(self, game):
        pass

    def store_game(self, game):
        pass

    def manipulating_delete_game(self, game):
        pass

    def manipulating_add_game(self, game):
        pass

