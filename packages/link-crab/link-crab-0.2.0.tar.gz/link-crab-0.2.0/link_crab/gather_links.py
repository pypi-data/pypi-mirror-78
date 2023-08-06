try:
    import reporting as reporting
except:
    pass
try:
    import link_crab.reporting as reporting
except:
    pass

import requests
from bs4 import BeautifulSoup
from urllib.request import urljoin, urlparse
import logging

crawled_links = set()
links_to_crawl = set()
total_urls_visited = 0

module_logger = logging.getLogger(__name__)

# FIXME: hangs if he first link is "out of domain" or unreachable?
def gather_links(session, links, checked_domain):
    for link in links:
        links_to_crawl.add(link)
    while len(links_to_crawl) > 0:
        module_logger.info(f"PROGRESS: {len(links)} links found, {len(crawled_links)} already crawled, {len(links_to_crawl)} left to crawl.")
        for link in links_to_crawl:
            crawl(session, link, links, checked_domain)
        reporting.save_links(links, checked_domain)

    return links



def crawl(session,url, links, checked_domain):
    global total_urls_visited
    global crawled_links
    global links_to_crawl
    module_logger.debug (f'{total_urls_visited} - currently checked page: {url}')

    if  url in crawled_links :
        module_logger.debug(f'    skip: already visited: {url}')
        return
    crawled_links.add(url)

    parsed = urlparse(url)
    if not (parsed.netloc == checked_domain):
        module_logger.debug(f'    skip: out of domain: {parsed.netloc}')
        return

    total_urls_visited += 1
    links = get_all_website_links(session, url, links)
    links_to_crawl= links-crawled_links


def get_all_website_links(session, url, links):
    """
    Returns URLs that is found on `url` in which belongs to the website
    """

    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc

    try:
        soup = BeautifulSoup(session.get(url).content, "html.parser")

        for a_tag in soup.findAll():
            href = a_tag.attrs.get("href")
            if href == "" or href is None:
                continue

            href = urljoin(url, href)
            parsed_href = urlparse(href)

            # remove URL GET parameters, URL fragments, etc.
            href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        
            if href in links:
               # print(f"[ ] link already gathered: {href}") # implement module_logger and logging level
               pass
            else:
                links.add(href)
               # print(f"[+] link found: {href}")
    except:
        module_logger.error(f"An exception occurred in getting website links from {url}")
    return links