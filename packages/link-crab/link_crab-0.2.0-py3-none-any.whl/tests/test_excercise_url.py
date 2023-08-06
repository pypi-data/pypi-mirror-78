import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from link_crab.session_manager import make_session
from link_crab.exercise_url import exercise_url
import pytest
from tests.test_app import mock_app
from tests.test_helpers import test_session

# These tests are highly dependent on the testapp.py
def test_url_validations(test_session):
    assert exercise_url(test_session,'Á://127.0.0.1:5000') == False
    assert exercise_url(test_session,'http://127.0.0.1:5000') != False

def test_url_status_codes(test_session):
    assert exercise_url(test_session,'http://127.0.0.1:5000')[1] == 200
    assert exercise_url(test_session,'http://127.0.0.1:5000/missing')[1] == 404

def test_accessibility(test_session):
    assert exercise_url(test_session,'http://127.0.0.1:5000/')[3] == True
    assert exercise_url(test_session,'http://127.0.0.1:5000/missing')[3] == False # Inaccessible because of status code is not ok
    assert exercise_url(test_session,'http://127.0.0.1:5000/member')[3] == False # Inaccessible because of permission