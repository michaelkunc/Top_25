import credentials
import requests
import collections


Api = collections.namedtuple('Api', 'url data params')

last_fm = Api(url='http://ws.audioscrobbler.com//2.0/', data=None, params={'api_key': credentials.LAST_FM_KEY, 'format': 'json',
                                                                           'limit': '25', 'method': 'user.gettoptracks', 'user': 'teamkuntz'})


def spotify_song_id_url(song, artist):
    return 'https://api.spotify.com/v1/search?q={0}%20artist:{1}&type=track'.format(song.replace(' ', '%20'), artist.replace(' ', '%20'))


def last_fm_api_call(url, params):
    r = requests.get(url, params=params)
    data = r.json()['toptracks']['track']
    return [(i['@attr']['rank'], i['name'], i['artist']['name']) for i in data]


# print(last_fm_api_call(last_fm.url, last_fm.params))
# get the Spotify song id for a given song.


def get_song_ids(song, artist):
    song = requests.get(spotify_song_id_url(song, artist))
    return song.json()['tracks']['items'][0]['id']

last_fm_songs = last_fm_api_call(last_fm.url, last_fm.params)

spotify_song_ids = [(s[0], s[1], s[2], get_song_ids(s[1], s[2]))
                    for s in last_fm_songs]
print(spotify_song_ids)

# print(song_ids)

# get current content of Top 25
# top_25_headers = {'Accept': 'application/json',
#                   'Authorization': 'Bearer {0}'.format(credentials.SPOTIFY_OAUTH_TOKEN)}


# tracks = requests.get(
#     'https://api.spotify.com/v1/users/mjkunc/playlists/2sQXVImsw9uZZKbmBKZxyZ/tracks', headers=top_25_headers)

# print(tracks.status_code)

# tracks = tracks.json()['items']

# top_25_ids = [i['track']['id'] for i in tracks]

# print(top_25_ids)

# delete current songs from playlist
# remove_header = {'Accept': 'application/json',
# 'Authorization': 'Bearer {0}'.format(credentials.SPOTIFY_OAUTH_TOKEN),
# 'Content-Type': 'application/json', }


# data_string = ['{{"positions":[{0}],"uri":"spotify:track:{1}"}}'.format(
# i, v) for i, v in enumerate(top_25_ids)]

# remove_data = '{{"tracks":[{0}]}}'.format(",".join(data_string))

# print(remove_data)

# r = requests.delete('https://api.spotify.com/v1/users/mjkunc/playlists/2sQXVImsw9uZZKbmBKZxyZ/tracks',
#                     headers=remove_header, data=remove_data)


# add the songs to the playlist
# add_songs_header = {'Accept': 'application/json',
# 'Authorization': 'Bearer {0}'.format(credentials.SPOTIFY_OAUTH_TOKEN),
# 'Content-Type': 'application/json', }

# track_uris = ',spotify:track:'.join(song_ids)

# r = requests.post(
#     'https://api.spotify.com/v1/users/mjkunc/playlists/2sQXVImsw9uZZKbmBKZxyZ/tracks?uris=spotify:track:{0}'.format(track_uris), headers=add_songs_header)

# print(r.text)
