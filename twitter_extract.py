import os
import pandas as pd
import requests
import datetime as dt
from pathlib import Path

TODAY = dt.datetime.today().isoformat(timespec = 'seconds') + 'Z'
ONE_DAY_AGO = (dt.datetime.today() - dt.timedelta(days = 1)).isoformat(timespec = 'seconds') + 'Z'

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
    tweets = first_response['data']
    while response['meta'].get('next_token'):
        print(f"Total scrapped tweets: {len(tweets)}")
        params['pagination_token'] = response['meta']['next_token']
        response = get_search_request(headers, params)
        tweets += response['data']
    return tweets

def main():
    hashtags = ['AprueboFeliz', 'Apruebo', 'NuevaConstitucion', 'Plebiscito', 'NuevaConstitucion', 
        'RutaConstituyente', 'ConvencionConstituyente', 'PlebiscitoConstitucional', 'PlebiscitoDeSalida',
        'RechazoDeSalida', 'AprueboCrece', 'Constitucion', 'Rechazo', 'RechazoTransversal', 'YoRechazo']
    total_tweets_df = pd.DataFrame()
    for hashtag in hashtags:
        print(f'Scrapping hashtag: {hashtag}')
        headers = create_headers()
        params = create_params(hashtag = hashtag)
        response = get_search_request(headers = headers, params = params)
        tweets = pagination(first_response = response, headers = headers, params = params)
        tweets_df = pd.DataFrame(tweets)
        tweets_df['search_hashtag'] = hashtag
        total_tweets_df = pd.concat([total_tweets_df, tweets_df])
    return total_tweets_df

def save_dataframe(df, name):
    path = Path('data') / name
    with open(path, 'w', newline = '') as f:
        df.to_csv(f, index = False)

if __name__ == '__main__':
    total_tweets_df = main()
    save_dataframe(total_tweets_df, 'tweets.csv')