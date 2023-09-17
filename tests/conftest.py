import pytest

from games import MemoryRepository, create_app


class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def login(self, username='thorke', password='cLQ^C#oFXloS'):
        return self.__client.post(
            'authentication/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self.__client.get('/authentication/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)


@pytest.fixture
def in_memory_repo(memory_repository=None, TEST_DATA_PATH=None):
    repo = MemoryRepository()
    memory_repository.populate(TEST_DATA_PATH, repo)
    return repo


@pytest.fixture
def client(TEST_DATA_PATH=None):
    my_app = create_app({
        'TESTING': True,
        'TEST_DATA_PATH': TEST_DATA_PATH,
        'WTF_CSRF_ENABLED': False
    })

    return my_app.test_client()
