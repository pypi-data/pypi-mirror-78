import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pytest
from link_crab.session_manager import make_session

@pytest.fixture(scope='session')
def test_session():
    session = make_session()
    return session
