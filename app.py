import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Spotify API credentials
SPOTIPY_CLIENT_ID = 'your_client_id'
SPOTIPY_CLIENT_SECRET = 'your_client_secret'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'
SCOPE = 'playlist-modify-public'

sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                        client_secret=SPOTIPY_CLIENT_SECRET,
                        redirect_uri=SPOTIPY_REDIRECT_URI,
                        scope=SCOPE)

def read_albums_from_file(filename='albums.txt'):
    albums = []
    with open(filename, 'r') as file:
        for line in file:
            # Assuming the format is "Rank: ..., Name: ..., Artist: ..."
            name_start_index = line.find('Name: ') + len('Name: ')
            artist_end_index = line.find(',', name_start_index)
            album_name = line[name_start_index:artist_end_index].strip()
            artist_start_index = line.find('Artist: ', artist_end_index) + len('Artist: ')
            artist_name = line[artist_start_index:].strip()
            albums.append(album_name+' '+artist_name)

    return albums



def add_albums_to_playlist():
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        code = sp_oauth.get_auth_response()
        token_info = sp_oauth.get_access_token(code)

    sp = spotipy.Spotify(auth=token_info['access_token'])

    albums = read_albums_from_file()

    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(user_id, 'Apple Music Top 100 Albums')

    for album in albums:
        results = sp.search(q='album:' + album, type='album')
        if results['albums']['items']:
            album_id = results['albums']['items'][0]['id']
            tracks = sp.album_tracks(album_id)['items']
            track_ids = [track['id'] for track in tracks]
            sp.playlist_add_items(playlist['id'], track_ids)

    print("Albums added successfully to the playlist!")

if __name__ == '__main__':
    add_albums_to_playlist()
