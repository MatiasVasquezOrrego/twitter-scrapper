#%%
import os
import pandas
import requests

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

def create_headers():
    bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")
    return {"Authorization": f"Bearer {bearer_token}"}

def create_params(hashtag):
    params = {'query': f'{hashtag} -is:retweet',
        'max_results': 100,
        'tweet.fields': 'author_id,conversation_id,created_at',
        'next_token': {}}
    return params

def get_search_request(headers, params):
    url = "https://api.twitter.com/2/tweets/search/recent"
    return requests.request("GET", url, params = params, headers = headers).json()

def pagination():
    pass

def main():
    headers = create_headers()
    params = create_params("Apruebo")
    response = get_search_request(headers, params)

if __name__ == __main__:
    main()








# %%
