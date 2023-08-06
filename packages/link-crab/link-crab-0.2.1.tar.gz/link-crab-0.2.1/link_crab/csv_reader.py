import csv
import logging

module_logger = logging.getLogger(__name__)

def read_link_perms(path_to_csv):
    with open(path_to_csv, 'r') as file:
        link_perms=[]
        csv_file = csv.DictReader(file)
        for row in csv_file:
            if row['should-access'] != '':
                should_access=None
                if row['should-access'].lower() in ('true', '1', 'yes'):
                    should_access=True
                elif row['should-access'].lower() in ('false','no', '0'):
                    should_access=False
                else:
                    raise 'invalid should-access value in perm-set! use true/false'
                link_perms.append([row['link'],should_access])
    module_logger.debug(link_perms)
    return link_perms