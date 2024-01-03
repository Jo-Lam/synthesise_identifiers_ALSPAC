import pandas as pd
import requests
import csv
import time
from requests.exceptions import ReadTimeout

class RateLimiter:
    def __init__(self, rate_limit, time_interval):
        self.rate_limit = rate_limit
        self.time_interval = time_interval
        self.tokens = rate_limit
        self.last_request_time = time.monotonic()

    def get_token(self):
        current_time = time.monotonic()
        time_elapsed = current_time - self.last_request_time
        self.tokens += time_elapsed * (self.rate_limit / self.time_interval)
        if self.tokens > self.rate_limit:
            self.tokens = self.rate_limit
        if self.tokens < 1:
            time.sleep(1 - self.tokens)
            self.tokens = 1
        self.last_request_time = current_time
        self.tokens -= 1

limiter = RateLimiter(rate_limit=30, time_interval=60)

def extract_ethnicity_likelihood(api_output):
    ethnicity_likelihood_pairs = api_output.split()
    ethnicity_likelihood_dict = {}
    for pair in ethnicity_likelihood_pairs:
        ethnicity, likelihood = pair.split(',')
        ethnicity_likelihood_dict[ethnicity] = likelihood
    return ethnicity_likelihood_dict

# Input file paths
names_csv_file = "name.csv" # change path/name to male list/female list from step 0

# Output file paths
output_csv_file = "male_output_nameprism.csv" # female_output_nameprism

# Read the list of names from the CSV file
names_df = pd.read_csv(names_csv_file)
names_list = names_df["Name"].tolist()
api_token = " " # insert your api

with open('output.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Hispanic', 'API', 'Black', 'AIAN', 'White'])
    for name in names_list:
        limiter.get_token()
        url = f"https://www.name-prism.com/api_token/eth/csv/{api_token}/{name}"
        try:
            response = requests.get(url, timeout = 3)
            if response.status_code == 200:
                ethnicity_likelihood_dict = extract_ethnicity_likelihood(response.text)
                row = [name] + [ethnicity_likelihood_dict.get(ethnicity, '') for ethnicity in ['Hispanic', 'API', 'Black', 'AIAN', 'White']]
                writer.writerow(row)
            else:
                print(f"API call for {name} failed with status code {response.status_code}")
        except ReadTimeout:
            print(f"API call for {name} timed out, pause for 5 minutes and move to the next request")
            time.sleep(30)
            continue
