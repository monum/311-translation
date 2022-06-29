# Import Modules

from time import time
import requests
import time
import pandas as pd

# Global Variables

WAITING_TIME = 10 # seconds
PAGE_SIZE = 200
NUM_PAGES = 10
BASE_URL = "https://mayors24.cityofboston.gov/open311/v2/requests.json" + "?page_size=" + str(PAGE_SIZE)

# First Page

data = requests.get(BASE_URL).json()
service_ids = [issue['service_request_id'] for issue in data if 'description' in issue]
grievances = [issue['description'] for issue in data if 'description' in issue]

# Subsequent Pages so that NUM_PAGES is the number of pages to be scraped

for i in range(NUM_PAGES):
    time.sleep(WAITING_TIME)
    new_url = BASE_URL + "&page_increment=" + str(i)
    additional_data = requests.get(new_url).json()
    for issue in additional_data:
        if 'description' in issue.keys(): # if the issue has no description, this is when it is only an image
            service_ids.append(issue['service_request_id'])
            grievances.append(issue['description'])
        else:
            pass

# Storing the data in a CSV format

df = pd.DataFrame(list(zip(service_ids, grievances)), columns=['service_request_id', 'grievance'])
df.to_csv('../../data/grievances.csv')