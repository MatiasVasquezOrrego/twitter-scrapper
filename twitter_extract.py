#%%
import os
import pandas
import requests
import datetime as dt

#AprueboFeliz 
#Apruebo 
#NuevaConstitucion
#Plebiscito 
#NuevaConstitucion
#RutaConstituyente
#ConvencionConstituyente
#PlebiscitoConstitucional
#PlebiscitoDeSalida 
#RechazoDeSalida 
#AprueboCrece
#Constitucion
#Rechazo 
#RechazoTransversal
#YoRechazo
#'b26v89c19zqg8o3fpz2mvagplwk78esg5c7tohp79ilj1'
TODAY = dt.datetime.today().isoformat(timespec='seconds') + 'Z'
ONE_WEEK_AGO = (dt.datetime.today() - dt.timedelta(days = 6)).isoformat(timespec='seconds') + 'Z'

def create_headers():
    bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")
    return {"Authorization": f"Bearer {bearer_token}"}

def create_params(hashtag):
    params = {
        'query': f'{hashtag} -is:retweet',
        'start_time' : ONE_WEEK_AGO,
        'end_time' : TODAY,
        'max_results': 100,
        'tweet.fields': 'author_id,conversation_id,created_at'
        }
    return params

def get_search_request(headers, params):
    url = "https://api.twitter.com/2/tweets/search/recent"
    return requests.request("GET", url, params = params, headers = headers).json()

def pagination(first_response, headers, params):
    response = first_response
    tweets = first_response['data']
    while response['meta']['next_token']:
        print(f"Total scrapped tweets: {len(tweets)}")
        params['pagination_token'] = response['meta']['next_token']
        response = get_search_request(headers, params)
        tweets += response['data']
    return tweets

def main():
    headers = create_headers()
    params = create_params(hashtag = "Apruebo")
    response = get_search_request(headers, params)
    tweets = pagination(response, headers, params)
    return tweets

if __name__ == "__main__":
    a = main()








# %%
