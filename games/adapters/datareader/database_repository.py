from abc import ABC
from typing import List, Any

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Publisher, Genre, User, Review


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository, ABC):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    # region Game_data
    def get_games(self) -> List[Game]:
        games = self._session_cm.session.query(Game).order_by(Game._Game__game_id).all()
        return games

    def get_game(self, game_id: int) -> Game:
        game = None
        try:
            game = self._session_cm.session.query(
                Game).filter(Game._Game__game_id == game_id).one()
        except NoResultFound:
            print(f'Game {game_id} was not found')

        return game

    def add_game(self, game: Game):
        with self._session_cm as scm:
            scm.session.merge(game)
            scm.commit()

    def add_multiple_games(self, games: List[Game]):
        with self._session_cm as scm:
            for game in games:
                scm.session.merge(game)
            scm.commit()

    def get_number_of_games(self):
        total_games = self._session_cm.session.query(Game).count()
        return total_games

    # endregion

    # region Publisher data
    def get_publishers(self) -> List[Publisher]:
        publishers = self._session_cm.session.query(Publisher).all()
        return publishers

    def add_publisher(self, publisher: Publisher):
        with self._session_cm as scm:
            scm.session.merge(publisher)
            scm.commit()

    def add_multiple_publishers(self, publishers: List[Publisher]):
        with self._session_cm as scm:
            for publisher in publishers:
                scm.session.merge(publisher)
            scm.commit()

    def get_number_of_publishers(self) -> int:
        total_publishers = self._session_cm.session.query(Publisher).count()
        return total_publishers

    # endregion

    # region Genre_data
    def get_genres(self) -> List[Genre]:
        genres = self._session_cm.session.query(Genre).all()
        return genres

    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.merge(genre)
            scm.commit()

    def add_multiple_genres(self, genres: List[Genre]):
        with self._session_cm as scm:
            for genre in genres:
                scm.session.merge(genre)
            scm.commit()

    # endregion
    def search_games_by_title(self, title_string: str) -> List[Game]:
        games = self._session_cm.session.query(Game).filter(Game._Game__game_title.contains(title_string)).all()
        return games

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.merge(user)
            scm.commit()

    def add_review(self, review: Review) -> Review:
        with self._session_cm as scm:
            scm.session.merge(review)
            scm.commit()
        return review

    def get_first_review(self) -> Review | None:
        try:
            review = self._session_cm.session.query(Review).first()
            return review
        except NoResultFound:
            return None

    def get_game_by_id(self, game_id) -> Game | None:
        game = None
        try:
            game = self._session_cm.session.query(Game).filter(Game._Game__game_id == game_id).one()
        except NoResultFound:
            return None
        return game

    def get_games_by_genre(self, genre_name: str) -> List[Game]:
        games = self._session_cm.session.query(Game).join(Genre).filter(Genre._Genre__genre_name == genre_name).all()
        return games

    def get_last_review(self) -> Review | None:
        try:
            review = self._session_cm.session.query(Review).first()
            return review
        except NoResultFound:
            return None

    def get_reviews_by_game_id(self, game_id) -> List[Review]:
        reviews = self._session_cm.session.query(Review).filter(Game._Game__game_id == game_id).all()
        return reviews


    def get_user(self, user_name) -> Any | None:
        try:
            user = self._session_cm.session.query(User).filter(User._User__username == user_name).one()
            return user
        except NoResultFound:
            return None

    def update_user(self, user: User):
        with self._session_cm as scm:
            scm.session.merge(user)
            scm.commit()


