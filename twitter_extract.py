import os
import pandas as pd
import requests
import datetime as dt
from pathlib import Path
import time

TODAY = dt.datetime.today().isoformat(timespec = 'seconds') + 'Z'
ONE_DAY_AGO = (dt.datetime.today() - dt.timedelta(days = 1)).isoformat(timespec = 'seconds') + 'Z'

def singleton(cls):    
    instance = [None]
    def wrapper(*args, **kwargs):
        if instance[0] is None:
            instance[0] = cls(*args, **kwargs)
        return instance[0]
    return wrapper

@singleton
class request_counter:
    def __init__(self) -> None:
        self.count = 0

    def add_count(self):
        self.count += 1

    def reset_count(self):
        self.count = 0

    def check_limit(self):
        if self.count == 449: 
            print("Waiting 15 mins to the restart of requests limit")
            self.sleep()
            self.reset_count()

    def sleep(self):
        time.sleep(60 * 15)

def create_headers():
    bearer_token = os.environ.get('TWITTER_BEARER_TOKEN')
    return {'Authorization': f'Bearer {bearer_token}'}

def create_params(hashtag):
    params = {
        'query': f'{hashtag} -is:retweet',
        'start_time' : ONE_DAY_AGO,
        'end_time' : TODAY,
        'max_results': 100,
        'tweet.fields': 'author_id,conversation_id,created_at'
        }
    return params

def get_search_request(headers, params):
    url = 'https://api.twitter.com/2/tweets/search/recent'
    response = requests.request("GET", url, params = params, headers = headers)
    if response.status_code != 200: return {'meta' : {'next_token' : None}, 'data' : []}
    return response.json()

def pagination(first_response, headers, params):
    response = first_response
    tweets = []
    tweets += first_response.get('data')
    request_count = request_counter()
    request_count.add_count()
    request_count.check_limit()
    while response['meta'].get('next_token'):
        print(f"Total scrapped tweets: {len(tweets)}")
        params['pagination_token'] = response['meta']['next_token']
        response = get_search_request(headers, params)
        tweets += response['data']
        request_count.add_count()
        request_count.check_limit()
    return tweets

def main(hashtags):
    total_tweets_df = pd.DataFrame()
    headers = create_headers()
    for hashtag in hashtags:
        print(f'Scrapping hashtag: {hashtag}')
        params = create_params(hashtag = hashtag)
        response = get_search_request(headers = headers, params = params)
        if not response.get('data'): continue
        tweets = pagination(first_response = response, headers = headers, params = params)
        tweets_df = pd.DataFrame(tweets)
        tweets_df['search_hashtag'] = hashtag
        total_tweets_df = pd.concat([total_tweets_df, tweets_df])
    total_tweets_df["text"] = total_tweets_df .text.str.replace('\n', ' ')
    return total_tweets_df

def save_dataframe(df, name):
    path = Path('data') / name
    with open(path, 'w', encoding ='utf-8', newline = '') as f:
        df.to_csv(f, index = False)

if __name__ == '__main__':
    hashtags = ['AprueboFeliz', 'Apruebo', 'NuevaConstitucion', 'Plebiscito', 'NuevaConstitucion', 
        'RutaConstituyente', 'ConvencionConstituyente', 'PlebiscitoConstitucional', 'PlebiscitoDeSalida',
        'RechazoDeSalida', 'AprueboCrece', 'Constitucion', 'Rechazo', 'RechazoTransversal', 'YoRechazo']
    total_tweets_df = main(hashtags)
    save_dataframe(total_tweets_df, 'tweets.csv')