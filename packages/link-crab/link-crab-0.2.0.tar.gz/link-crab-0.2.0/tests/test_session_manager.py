import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from link_crab.session_manager import make_session
from link_crab.exercise_url import exercise_url
from tests.test_app import app
import pytest
from tests.test_app import mock_app

@pytest.fixture(scope='session')
def test_session_mock():
    member_mockuser = {
        'login_url': 'http://127.0.0.1:5000/user/sign-in',
        'email': 'member@example.com',
        'password': 'Password1',
        'password_locator_id': 'password',
        'email_locator_id': 'email'
    }
    session = make_session(member_mockuser)
    return session

# These tests are highly dependent on the testapp.py
def test_access(test_session_mock):
    assert exercise_url(test_session_mock,'http://127.0.0.1:5000/members')[3] == True