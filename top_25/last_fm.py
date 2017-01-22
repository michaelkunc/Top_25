import credentials
import requests


# Last FM Api Call
payload = {'api_key': credentials.LAST_FM_KEY, 'format': 'json',
           'limit': '25', 'method': 'user.gettoptracks', 'user': 'teamkuntz'}

url = 'http://ws.audioscrobbler.com//2.0/'

r = requests.get(url, params=payload)

data = r.json()['toptracks']['track']


song_artist = ((i['name'], i['artist']['name']) for i in data)

for s in song_artist:
    print(s)


# get the Spotify song id for a given song.

song = requests.get(
    'https://api.spotify.com/v1/search?q=wednesday%20artist:drive%20by%20truckers&type=track')

song = song.json()
