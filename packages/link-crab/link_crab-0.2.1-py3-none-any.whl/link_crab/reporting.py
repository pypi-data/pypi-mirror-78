from datetime import datetime

import os
delimiter=','
#TODO: some test-reports folder would be nice tbh, The -t argument should be used
def save_linkdb_to_csv(link_db, domain_name, starting_time):
    if not os.path.exists(f'reports/{domain_name}'):
        os.makedirs(f'reports/{domain_name}')
    with open(f"reports/{domain_name}/{domain_name}_{starting_time}_exercised_links.csv", "w") as f:
        print(f"url{delimiter}status_code{delimiter}resp_url(after_redirects){delimiter}response_time(ms){delimiter}accessible?", file=f)
        for link in link_db:
            print(f"{link[0]}{delimiter}{link[1]}{delimiter}{link[4]}{delimiter}{link[2]}{delimiter}{link[3]}", file=f)

def save_permdb_to_csv(perm_db, domain_name, user_email,starting_time):
    if not os.path.exists(f'reports/{domain_name}'):
        os.makedirs(f'reports/{domain_name}')
    with open(f"reports/{domain_name}/{domain_name}_{starting_time}_{user_email}_permission_check_result.csv", "w") as f:
        print(f"url{delimiter}status_code{delimiter}response_time(ms){delimiter}accessible?{delimiter}should_be_accessible?{delimiter}assert_accessibility", file=f)
        for link in perm_db:
            print(f"{link[0]}{delimiter}{link[1]}{delimiter}{link[4]}{delimiter}{link[3]}{delimiter}{link[5]}{delimiter}{link[6]}", file=f)

def save_links(links, domain_name):
    if not os.path.exists(f'reports/{domain_name}'):
        os.makedirs(f'reports/{domain_name}')
    with open(f"reports/{domain_name}/{domain_name}_links.txt", "w") as f:
        for link in links:
            print(f"{link}", file=f)