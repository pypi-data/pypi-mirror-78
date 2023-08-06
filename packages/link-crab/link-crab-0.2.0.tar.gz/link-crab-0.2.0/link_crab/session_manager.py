import requests
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options 
import logging

module_logger = logging.getLogger(__name__)

#FIXME: handle exception when webdriver is not present

def make_session(user=None):
    session = requests.session()
    if user:
        cookies = get_cookies_with_selenium(user)
        for cookie in cookies:
            cookie_obj = requests.cookies.create_cookie(domain=cookie['domain'],name=cookie['name'],value=cookie['value'])
            session.cookies.set_cookie(cookie_obj)
        module_logger.debug(session.cookies)
    return session

def get_cookies_with_selenium(user):
    login_url= user['login_url']
    email= user['email']
    email_locator_id = user['email_locator_id']
    password= user['password']
    password_locator_id = user['password_locator_id']

 

    chrome_options = Options()  
    chrome_options.add_argument("--headless")   

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(login_url)
    
    
    email_field = driver.find_element_by_id(email_locator_id)
    
    email_field.clear()
    email_field.send_keys(email)

    password_field = driver.find_element_by_id(password_locator_id)
    password_field.clear()
    password_field.send_keys(password)

    submit_button = driver.find_element_by_xpath('//input[@type="submit"]')

    submit_button.click()
    # time.sleep(1)
    cookies = driver.get_cookies()
    module_logger.debug(f"got cookie with selenium: {cookies}")
    driver.close()
    return cookies


    