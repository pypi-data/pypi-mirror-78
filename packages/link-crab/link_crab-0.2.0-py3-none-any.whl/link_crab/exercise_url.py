import requests
from urllib.request import urljoin, urlparse
import logging

module_logger = logging.getLogger(__name__)

def exercise_url(session, url):
    '''
    Excersize url and gives back the following array:
    [0] visited url
    [1] status code
    [2] response time
    [3] accessible (bool)
    [4] returned url (after all redirects)
    args: 
        session: the session made by session_manager.py
        url: the url to be exercised
    '''
    if not check_url_validity(url):
        module_logger.warning(f"invalid link: {url}")
        return False
    try:
        resp = session.get(url) # maybe we should just use  allow_redirects=False for accessibility 
        accessible = resp.ok and resp.url == url
        outcome=[url,resp.status_code, int(resp.elapsed.total_seconds()*1000), accessible, resp.url] #should we change this to a dict? (depends on memory usage)
        module_logger.debug(f"[*] {outcome[0]} - {outcome[1]} - {outcome[4]} - {outcome[2]} ms - accessible: {outcome[3]}")

    except:
        outcome=[url, 'err', 'err', False, 'err']
    return outcome


def check_url_validity(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


