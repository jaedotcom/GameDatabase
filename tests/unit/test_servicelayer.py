import pytest
from games.domainmodel.model import Publisher, Genre, Game, Review, User, Wishlist
from datetime import datetime

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

def test_game_init():
    genre = Genre("Action")
    game = Game(1010, "Game Title")
    game.add_genre(genre)
    assert repr(game) == "<Game 1010, Game Title>"
    assert game.title == "Game Title"
    assert repr(game.genres[0]) == '<Genre Action>'

def test_game_title_validation():
    publisher = Publisher("Publisher A")
    genre = Genre("Action")

    with pytest.raises(ValueError):
        game = Game('', "")

    with pytest.raises(ValueError):
        game = Game('', genre)

    with pytest.raises(ValueError):
        game = Game('', publisher)

    with pytest.raises(ValueError):
        game = Game(-10, 0)

    with pytest.raises(ValueError):
        game = Game(publisher, genre)

def test_game_release_date_validation():
    game = Game(12345678, "God I hate writing tests, Amen")

    with pytest.raises(ValueError):
        game.release_date = "Dec 44, 0000"

    game.release_date = "Oct 21, 2008"

    expected_date = datetime.strptime("Oct 21, 2008", "%b %d, %Y")
    assert str(game.release_date) == 'Oct 21, 2008'




