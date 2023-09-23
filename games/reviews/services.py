from typing import List, Iterable

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Review, make_review


class NonExistentReviewException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_review(game_id: int, comment_text: str, user_name: str, rating: int, repo: AbstractRepository):
    game = repo.get_game_by_id(game_id)

    if game is None:
        raise NonExistentReviewException

    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException

    review = make_review(user, game, rating, comment_text)

    repo.add_review(review)


def get_reviews(game_id: int, repo: AbstractRepository):
    reviews = repo.get_reviews_by_game_id(game_id)

    if reviews is None:
        raise NonExistentReviewException

    return reviews_to_dict(reviews)


def get_first_article(repo: AbstractRepository):
    review = repo.get_first_review()
    return review_to_dict(review)


def get_last_review(repo: AbstractRepository):
    review = repo.get_last_review()
    return review_to_dict(review)


def get_reviews_for_game(game_id, repo: AbstractRepository):
    reviews = repo.get_reviews_by_game_id(game_id)
    if reviews is None:
        raise NonExistentReviewException
    return reviews_to_dict(reviews)


# ============================================
# Functions to convert model entities to dicts
# ============================================

def review_to_dict(review: Review):
    review_dict = {
        'user': review.user,
        'game': review.game,
        'rating': review.rating,
        'comments': review.comment,
    }
    return review_dict


def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]


# ============================================
# Functions to convert dicts to model entities
# ============================================

def dict_to_review(dict):
    review = Review(dict.user, dict.game, dict.rating, dict.comment)
    return review
