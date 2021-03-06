import credentials
import requests
import collections
import boto3
import botocore

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


# Writing out to S3
# eventually will write out a file every week with a filename like
# top_25_01_27_2017.txt
test_file = 'the_s_is_for_sucks.txt'

s3 = boto3.resource('s3')
data = open(test_file, 'rb')

last_fm_bucket = s3.Bucket(credentials.AWS_S3_BUCKET_NAME)


# will use something like this to see if a given file name is already in
# the bucket.
def write_to_s3(bucket_object, file):
    bucket_name = bucket_object.name
    try:
        s3.Object(bucket_name, file).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            s3.Bucket(bucket_name).put_object(Key=file, Body=data)
            return 'Your file is now saved on S3'
        else:
            raise
    else:
        return 'This file is already on s3'

print(write_to_s3(last_fm_bucket, test_file))

print(write_to_s3(last_fm_bucket, 'other_file.txt'))

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
