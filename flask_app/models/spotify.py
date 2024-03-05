from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import spotipy
import pprint


load_dotenv()

username = "maxrice92"
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)

    json_result = json.loads(result.content)
    token = json_result["access_token"]

    return token


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def search_for_song_and_artist(artist_name, song_keywords):
    token = get_token()
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)

    query = f'?q={artist_name + " " + song_keywords}&type=artist,track&market=US&limit=1'

    query_url = url + query

    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)

    spot_id = json_result['artists']['items'][0]['id']
    title = json_result['tracks']['items'][0]['name']
    artists = json_result['artists']['items']
    artists_names = ', '.join([artists[0]['name'] for artist in artists])
    cover_link = json_result['tracks']['items'][0]['album']["images"][0]['url']
    song_link = json_result['tracks']['items'][0]['external_urls']["spotify"]
    # for api link ["external_url"]["href"] -- needs a token to make this work
    duration = json_result['tracks']['items'][0]['duration_ms']

    song_dict = {
        "spot_id": spot_id,
        "title": title,
        "artist_names": artists_names,
        "cover_link": cover_link,
        "track_link": song_link,
        "duration": duration

    }
    return song_dict


def get_song_struct(title, artist):
    token = get_token()
    search_for_song_and_artist(token, artist, title)
