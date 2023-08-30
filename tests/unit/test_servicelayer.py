import pytest
import os
from games.domainmodel.model import Publisher, Genre, Game, Review, User, Wishlist
from games.adapters.datareader.csvdatareader import GameFileCSVReader


def test_publisher_init():
    publisher1 = Publisher("Publisher A")
    assert repr(publisher1) == "<Publisher Publisher A>"
    assert publisher1.publisher_name == "Publisher A"

    publisher2 = Publisher("")
    assert publisher2.publisher_name is None

    publisher3 = Publisher(123)
    assert publisher3.publisher_name is None

    publisher4 = Publisher(" Wild Rooster   ")
    assert publisher4.publisher_name == "Wild Rooster"

    publisher4.publisher_name = "Century Game"
    assert repr(publisher4) == "<Publisher Century Game>"

