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
    print(s[1])

# get the Spotify song id for a given song.

song_ids = []


# def get_song_ids(song):
# print(song)
# song = requests.get(
#     'https://api.spotify.com/v1/search?q={0}%20artist:{1}&type=track'.format(song.replace(' ', '%20'), artist.replace(' ', '%20')))

# song = song.json()

# return song['tracks']['items'][0]['id']


# for s in song_artist:
#     print(get_song_ids(s[0]))


# print(song_ids)
