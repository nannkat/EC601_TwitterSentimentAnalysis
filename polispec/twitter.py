
import requests
import yaml
import json
import re
from datetime import datetime, timedelta

def get_twitter_credentials():
    with open("/Users/Nanna/Desktop/EC601/twitter_sentiment_analysis/creds.yaml") as file:
        return yaml.safe_load(file)

def create_headers():
    credentials = get_twitter_credentials()
    bearer_token = credentials['twitter_api']['bearer_token']
    headers = {}
    headers["Authorization"] = "Bearer {}".format(bearer_token)
    return headers

def querify_name(name):
    name_list = name.split()
    query = ''
    for n in name_list:
        query += n+'%20'
    return query

def create_url(name, additional_query_params = ''):
    base_url = 'https://api.twitter.com/2/tweets/search/recent?query='
    name_url = querify_name(name)
    set_query_params = 'lang%3Aen%20-is%3Aretweet%20-is%3Areply'
    return base_url + name_url + set_query_params + additional_query_params

def get_dates(hour_count):
    now = datetime.today()
    to_gmt = timedelta(4/24-(1/60)/24)
    now = now + to_gmt
    past = timedelta(hour_count/24)
    new_date = now - past
    return (now.strftime('%Y-%m-%dT%H:%M:%S.000Z'), new_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))

def create_params(max_results = 10, start_time = {}, end_time = {}):
    parameters = {
            'start_time': start_time,
            'end_time': end_time,
            'max_results' : max_results,
            'tweet.fields': 'created_at,public_metrics',
        }
    return parameters

def connect_to_endpoint_twitter(url, headers, params = None, next_token = {}):
    params['next_token'] = next_token
    response = requests.request("GET", url, headers = headers, params = params)
    #print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def get_next_token(api_response):
    return api_response['meta']['next_token']

def print_tweet_dump(api_response):
    print(json.dumps(api_response['data'], indent= 4, sort_keys=True))
    

class Tweet:
    def __init__(self, json_tweet):
        self.date = json_tweet['created_at'][0:10]
        self.time = json_tweet['created_at'][11:16]
        self.text = json_tweet['text']
        self.like_count = json_tweet['public_metrics']['like_count']
        self.retweet_count = json_tweet['public_metrics']['retweet_count']
    
    def get_date(self):
        return self.time + '-' + self.date


    def get_likes(self):
        return self.like_count

    def clean_tweet(self):
        '''Clean up the text of the tweet. Get rid of https links at the end. And, make time logic format dd-mm-yyyy'''
        self.text = re.sub(r"http\S+", "", self.text)
        self.date = self.date[8:10] + '-' + self.date[5:7] + '-' + self.date[0:4]
    
    def __str__(self):
        ret_str = "{}\n".format(self.text)
        ret_str += "Likes: {} Retweets:{}\n".format(str(self.like_count), str(self.retweet_count))
        ret_str += "Date: {} Time: {}\n".format(self.date, self.time)
        return ret_str