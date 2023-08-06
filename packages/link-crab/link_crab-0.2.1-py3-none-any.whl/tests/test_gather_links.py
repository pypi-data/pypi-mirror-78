import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from link_crab.session_manager import make_session
from link_crab.gather_links import get_all_website_links, crawl, gather_links
import pytest
from tests.test_helpers import test_session
from tests.test_app import mock_app
import logging

def test_url_gathering(test_session):
    links = set()
    assert len(get_all_website_links(test_session,'http://127.0.0.1:5000', links)) == 8

def test_crawl_url_already_visited_not_collected(test_session, caplog):
    caplog.set_level(logging.DEBUG)
    links = set()
    url='http://www.example.com/xmpl'
    links.add(url)
    crawl(test_session,url,links,'www.example.com') # first run to collect url in crawled_links
    assert crawl(test_session,url,links,'www.example.com') == None
    captured = caplog.text
    assert "already visited" in captured

def test_crawl_url_out_of_domain_not_collected(test_session, caplog):
    caplog.set_level(logging.DEBUG)
    links = set()
    url='http://www.example.com/xmpl2'
    assert crawl(test_session,url,links,'www.not_correct_domain.com') == None
    captured = caplog.text
    assert "out of domain" in captured

def test_gather_links_hp(test_session):
    links = set()
    url='http://127.0.0.1:5000'
    links.add(url)

    outcome_links = {'http://127.0.0.1:5000', 'http://127.0.0.1:5000/', 'http://127.0.0.1:5000/admin', 'http://127.0.0.1:5000/members', 'http://127.0.0.1:5000/missing', 'http://127.0.0.1:5000/user/forgot-password', 'http://127.0.0.1:5000/user/missing', 'http://127.0.0.1:5000/user/register', 'http://127.0.0.1:5000/user/sign-in', 'http://127.0.0.1:5000/user/sign-out', 'http://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css'}
    assert  gather_links(test_session,links,'127.0.0.1:5000') == outcome_links