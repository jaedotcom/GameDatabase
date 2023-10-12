import pytest

from games import SqlAlchemyRepository
from games.domainmodel.model import User


def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Dave', '123456789')
    repo.add_user(user)

    repo.add_user(User('Martin', '123456789'))

    user2 = repo.get_user('Dave')

    assert user2 == user and user2 is user


def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')

def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('prince')
    assert user is None


def test_repository_can_add_review(session_factory):
    pass

def test_repository_can_retrieve_review(session_factory):
    pass


def test_repository_can_retrieve_reviews_of_game(session_factory):
    pass

def test_repository_does_not_retrieve_a_review_when_there_are_no_reviews_for_a_given_game(session_factory):
    pass

def test_repository_can_retrieve_genres(session_factory):
    pass

def test_repository_can_get_first_review(session_factory):
    pass

def test_repository_can_get_last_review(session_factory):
    pass
def test_repository_can_get_review_by_ids(session_factory):
    pass
def test_repository_does_not_retrieve_review_for_non_existent_id(session_factory):
    pass



def test_repository_returns_none_when_there_are_no_previous_reviews(session_factory):
    pass




def test_repository_can_add_a_favourite(session_factory):
    pass


def test_repository_can_add_a_review(session_factory):
    pass


def test_repository_does_not_add_a_review_without_a_user(session_factory):
    pass

def test_repository_can_retrieve_reviews(session_factory):
    pass


def make_review():
    pass



