# The Link Crab

[![PyPI version](https://badge.fury.io/py/link-crab.svg)](https://badge.fury.io/py/link-crab)
![Run Pytest](https://github.com/klucsik/link-crab/workflows/Run%20Pytest/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/klucsik/link-crab/badge.svg?branch=master)](https://coveralls.io/github/klucsik/link-crab?branch=master)

A simple CLI tool which can crawl through your website and catch broken links, and can check user permissions to specific pages on your website.

## Workmode - Link gathering:
In this mode, you provide a starting url, and the Link Crab will crawl through the starting page, and all the page which is accessible thorugh links from that page and is in the same domain as the starting apge.
The program export the gathered links in a txt file, then exercise them, gathering response time and status code, and exporting these in a csv file.

 ## Workmode - Link access permission checking:
In this mode you provide a csv file with links to check, and wether those links should be accessible. The Link Crab will check every link in the list, determines if its accessible or not, and then assert the expected accessibilty to the actual accessibility. 
A link is considered accessible if the http response for a get request on the link has a status code under 400, and after all redirects, the url is equals of the starting url. 
(Most of the websites either give you a 404 or redirect to the sign-in page.)
*Maybe following the redirects is unnecessary, but I considered it safer*

## Session management:
In both workmode, you can provide login informations. The Link Crab opens up a Chrome browser with Selenium webdriver, and goes to the provided login page. On the login page, it will find the email and password fields, based on the html ids you provided, and fills it with your credentials. Then it will click on the submit button, thus logs in to the page. Then the Link Crab aquires the cookies, and closes the browser. It will use this auth cookies through the testing.

If you are in Permission checking mode, and want to check the logout page, be sure you will not need the session in the next checked pages after the logout.

## Generated reports:

The Link Crab will make the following reports:

**[domain_name]_links.txt:**
This report is generated in the link gathering mode, through the gathering phase. It will be updated as the gatherer crawls through the pages.

Example from the mock app:

    http://127.0.0.1:5000/user/sign-in
    http://127.0.0.1:5000/user/forgot-password
    http://127.0.0.1:5000/members
    http://127.0.0.1:5000/user/edit_user_profile
    http://127.0.0.1:5000/missing
    http://127.0.0.1:5000/user/change-password
    http://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css
    http://127.0.0.1:5000/user/missing
    http://127.0.0.1:5000/user/register
    http://127.0.0.1:5000/user/sign-out
    http://127.0.0.1:5000/
    http://127.0.0.1:5000/missing_member_only
    http://127.0.0.1:5000/admin

**[domain_name]_[datetime]_exercised_links.csv:**
This report is generated at the end of the exercising phase in the link gathering mode. Example from the mock app:


| url                                                                  | status_code | resp_url(after_redirects)                                            | response_time(ms) | accessible? |
|----------------------------------------------------------------------|-------------|----------------------------------------------------------------------|-------------------|-------------|
| http://127.0.0.1:5000/user/sign-in                                   | 200         | http://127.0.0.1:5000/                                               | 10                | False       |
| http://127.0.0.1:5000/user/forgot-password                           | 200         | http://127.0.0.1:5000/user/forgot-password                           | 6                 | True        |
| http://127.0.0.1:5000/members                                        | 200         | http://127.0.0.1:5000/members                                        | 10                | True        |
| http://127.0.0.1:5000/user/edit_user_profile                         | 200         | http://127.0.0.1:5000/user/edit_user_profile                         | 6                 | True        |
| http://127.0.0.1:5000/missing                                        | 404         | http://127.0.0.1:5000/missing                                        | 3                 | False       |
| http://127.0.0.1:5000/user/change-password                           | 200         | http://127.0.0.1:5000/user/change-password                           | 13                | True        |
| http://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css | 200         | http://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css | 94                | True        |
| http://127.0.0.1:5000/user/missing                                   | 404         | http://127.0.0.1:5000/user/missing                                   | 2                 | False       |
| http://127.0.0.1:5000/user/register                                  | 200         | http://127.0.0.1:5000/user/register                                  | 7                 | True        |
| http://127.0.0.1:5000/user/sign-out                                  | 200         | http://127.0.0.1:5000/                                               | 8                 | False       |
| http://127.0.0.1:5000/                                               | 200         | http://127.0.0.1:5000/                                               | 8                 | True        |
| http://127.0.0.1:5000/missing_member_only                            | 404         | http://127.0.0.1:5000/missing_member_only                            | 3                 | False       |
| http://127.0.0.1:5000/admin                                          | 200         | http://127.0.0.1:5000/user/sign-in?next=/admin                       | 9                 | False       |


**[domain_name]_[datetime]_[user_email]_permission_check_result.csv:**
This report is generated at the end of the permission checking mode. Example from the mock app:

| url                                          | status_code | resp_url(after_redirects)                                     | accessible? | should_be_accessible? | assert_accessibility |
|----------------------------------------------|-------------|---------------------------------------------------------------|-------------|-----------------------|----------------------|
| http://127.0.0.1:5000/                       | 200         | http://127.0.0.1:5000/                                        | True        | True                  | PASSED               |
| http://127.0.0.1:5000/user/register          | 200         | http://127.0.0.1:5000/user/register                           | True        | True                  | PASSED               |
| http://127.0.0.1:5000/members                | 200         | http://127.0.0.1:5000/members                                 | True        | True                  | PASSED               |
| http://127.0.0.1:5000/user/forgot-password   | 200         | http://127.0.0.1:5000/user/forgot-password                    | True        | True                  | PASSED               |
| http://127.0.0.1:5000/user/edit_user_profile | 200         | http://127.0.0.1:5000/user/edit_user_profile                  | True        | True                  | PASSED               |
| http://127.0.0.1:5000/admin                  | 200         | http://127.0.0.1:5000/                                        | False       | False                 | PASSED               |
| http://127.0.0.1:5000/user/sign-in           | 200         | http://127.0.0.1:5000/                                        | False       | True                  | FAILED               |
| http://127.0.0.1:5000/user/sign-out          | 200         | http://127.0.0.1:5000/                                        | False       | True                  | FAILED               |
| http://127.0.0.1:5000/user/change-password   | 200         | http://127.0.0.1:5000/user/sign-in?next=/user/change-password | False       | True                  | FAILED               |


All reports are saved in the reports folder under a folder named by the domain name. For example, when you test  `example.com`, the reports will be in `reports/example.com/` relative to where you called the command.
The link-crab also saves runtime logs in the created report folder.

The configuration is done through a yaml config files.

## Installation

Install with `pip install link-crab`

Dependencies: [chromedriver](https://chromedriver.chromium.org/downloads) for logging in to the tested site.

## Usage:
Simply use the command `python -m link_crab path/to/your/config.yaml` in the PYthon envrionment which has the link-crab installed. All the configuration is done in the config file, which is expanded bellow.
If you want to use the sample flask mock app for testing, provide the `-t` flag.
If you want to have verbose output, provide the `-t` flag.

For additional help run:  `python -m link-crab -h`

A good usage pattern would be to run the Link Crab first in link gathering mode, and from the generated links.txt select the links for the permission checking mode.

### Configuration:
**starting_url**

    starting_url: http://127.0.0.1:5000

Gather the reachable links in the starting_url's page and all of its subpages.
After collecting all the links, the link exerciser load every in-domain url with a GET request, and measures 
status code, response time, response url after all redirects, and accessibility based on status code and response url

**path_to_link_perms**

    path_to_link_perms: testapp_member_access.csv

Test accessibility of provided links. The csv should have a link and a should-access column. 
asserts the link accessibility equals to provided should-access.
A link is accessible if the response status code<400, and after redirets the respone url equals the starting url
(some framework give a 404 for unaccessible pages or redriects to sign_in page)

 Sample link_perms csv:

| link                                         | should-access |
|----------------------------------------------|---------------|
| http://127.0.0.1:5000/                       | TRUE          |
| http://127.0.0.1:5000/user/register          | TRUE          |
| http://127.0.0.1:5000/members                | TRUE          |
| http://127.0.0.1:5000/admin                  | FALSE         |


**User**

    user:
        email: member@example.com
        email_locator_id: email
        login_url: http://127.0.0.1:5000/user/sign-in
        password: Password1
        password_locator_id: password
    
Login with the help of selenium webdriver (chromedriver). You need to provide the url of the login form, 
   and the id's of the email (or username) and password fields.