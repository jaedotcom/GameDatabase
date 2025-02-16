from werkzeug.security import generate_password_hash, check_password_hash
from games.adapters.repository import AbstractRepository
from games.domainmodel.model import User


class NameNotUniqueException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass


def add_user(username: str, password: str, repo: AbstractRepository):
    # Encrypt password
    password_hash = generate_password_hash(password)
    # Create new User
    new_user = User(username, password_hash)
    # check username is not taken
    repo.add_user(new_user)


# def get_current_user(username: str, repo: AbstractRepository):
#     current_user = repo.get_user(username)

def get_user_details(username: str, repo: AbstractRepository):
    user = repo.get_user(username)

    # TO DO: handle
    if user is None:
        raise UnknownUserException

    return user_to_dict(user)


def get_current_user(username: str, repo: AbstractRepository):
    user = repo.get_user(username)
    return user


def authenticate_user(username: str, password: str, repo: AbstractRepository):
    #authenticated = False

    user = repo.get_user(username)
    if user is not None:
        authenticated = check_password_hash(user.password, password)
        if not authenticated:
            raise AuthenticationException("Authentication failed")

    return user


# ============================================
# Functions to convert model entities to dicts
# ============================================

def user_to_dict(user: User):
    user_dict = {
        'username': user.username,
        'password': user.password
    }

    return user_dict