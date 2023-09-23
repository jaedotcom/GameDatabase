from games.adapters.repository import AbstractRepository
from functools import cmp_to_key
from games.domainmodel.model import Review


def get_game_by_id(game_id, repo: AbstractRepository):
    for game in repo:
        if game.game_id == game_id:
            return game
    return None

def get_number_of_games(repo: AbstractRepository):
    return repo.get_number_of_games()


def post_rating(user_name, game_id, rating, repo_instance: AbstractRepository):
    """
    Add a rating for a game associated with a user.

    :param user_name: The username of the user posting the rating.
    :param game_id: The ID of the game for which the rating is posted.
    :param rating: The user's rating for the game.
    :param repo_instance: The repository instance.
    """
    # Check if the user and game exist in the repository
    user = repo_instance.get_user(user_name)
    game = repo_instance.get_game_by_id(game_id)

    if user is None or game is None:
        raise ValueError("User or game not found")

    # Create a new Review object with the rating
    review = Review(user, game, rating, "")  # Note: You can provide an empty string as a comment if needed

    # Add the review to the game's reviews
    game.add_review(review)

    # Update the repository
    repo_instance.add_review(review)

def post_review(user_name: str, game_id: int, review_text: str, repo: AbstractRepository):
    """
    Add a review for a game associated with a user.

    :param user_name: The username of the user posting the review.
    :param game_id: The ID of the game for which the review is posted.
    :param review_text: The text of the review.
    :param repo: The repository instance.
    """
    # Check if the user and game exist in the repository
    user = repo.get_user(user_name)
    game = repo.get_game_by_id(game_id)

    if user is None or game is None:
        raise ValueError("User or game not found")

    # Create a new review object
    review = Review(user, game,0, review_text)

    # Add the review to the game's reviews
    game.add_review(review)

    # Update the repository
    repo.add_review(review)


def get_games(repo: AbstractRepository):
    games = repo.get_games()
    sorted_games = sorted(games, key=cmp_to_key(compare_games_by_title))
    game_dicts = []
    for game in sorted_games:
        game_genres = game.genres
        genre_names = []
        for i in game_genres:
            genre_names.append(i.genre_name)
        game_dict = {
            'game_id': game.game_id,
            'title': game.title,
            'game_release_date': game.release_date,
            'price': game.price,
            'description': game.description,
            'image_url': game.image_url,
            'genres': genre_names
        }
        game_dicts.append(game_dict)
    return game_dicts


def compare_games_by_title(game1, game2):
    return (game1.title > game2.title) - (game1.title < game2.title)


def compare_games_by_release_date(game1, game2):
    return (game1.release_date > game2.release_date) - (game1.release_date < game2.release_date)


def get_games_by_search_key(search_key: str, repo):
    games = repo.get_games()
    if not search_key or not isinstance(search_key, str):
        raise ValueError("Invalid search key")
    matching_games = []
    for game in games:
        if search_key.lower() in game.title.lower():
            matching_games.append(game)
    return matching_games

