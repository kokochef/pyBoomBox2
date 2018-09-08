import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

def get_random_playlists(limit=1,offset=-1):
    if(offset==-1):
        offset = random.randint(0,1500)
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    playlists = sp.user_playlists('spotify',limit=limit,offset=offset)
    return playlists

def get_token():
    scope = 'playlist-modify-private'
    token = util.prompt_for_user_token(username,scope,client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri)
    return token