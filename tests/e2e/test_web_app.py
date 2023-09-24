import pytest
from flask import session


def test_comment(client, auth):
    auth.login()

    response = client.get('/comment_review?something')

    response = client.post(
        '/comment_review',
        data={'comment': 'This game sucks', 'game_id': 1}
    )
    assert response.headers['Location'] == 'httpL//localhost/gameviewreviews'  # to do


def test_login_required_to_post_review(client):
    response = client.post('/comment')
    assert response.headers['Location'] == 'http://localhost/authentication/login'  # Check this is right later


def test_register(client):
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    response = client.post(
        '/authentication/register',
        data={'username': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == 'http://localhost/authentication/login'


@pytest.mark.parametrize(('username', 'password', 'message'), (
        (",", b'Your username is required'),
        ('cj', '', b'Your username is too short' ), # ask about "
        ('test', "", b'Your password is required' ), # ask about "
        ('test', 'test',
         b'Your password must be at least 8 characters, and contain an upper case letter, a lower case letter and a '
         b'digit'),
        ('fmercury', 'Test#6^0', b'Your username is already taken - please try again'),
))
def test_register_with_invalid_input(client, username, password, message):
    response = client.post(
        '/authentication/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_index(client):  # Checking to see the root of the page
    response = client.get('/')
    assert response.status_code == 200
    assert b'Access Games Instantly' in response.data


def test_games_with_review(client):  # to do
    response = client.get('/')
    assert response.status_code == 200
    assert b'Access Games Instantly' in response.data
    assert b'Access Games Instantly' in response.data

def test_login(client, auth):
    # Check we retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check successful login redirects to the homepage
    response = auth.login()
    assert response.headers["Location"] == "/"

    # Check a session has been created for the user
    with client:
        client.get('/')
        assert session["username"] == "test_user"

def test_logout(client, auth):
    # Login
    auth.login()

    # Log out
    with client:
        auth.logout()
        assert "username" not in session
