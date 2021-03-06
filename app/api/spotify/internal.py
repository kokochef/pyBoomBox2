import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

from .models import *

username = 'username'
client_id='clientid'
client_secret='clientsecret'
redirect_uri='redirecturl'

#gets a list of playlist from the spotify username with a random offset if none provided
def get_random_playlists(limit=1,offset=-1):
    if(offset==-1):
        offset = random.randint(0,1500)
    return get_playlist('spotify',limit=limit,offset=offset)

#generates and returns a token 
def get_token():
    scope = 'playlist-modify-private'
    token = util.prompt_for_user_token(username,scope,client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri)
    return token

#gets a users public playlist , returns models.Playlist[]
def get_playlists(user,limit,offset):
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    playlists_json = sp.user_playlists(user,limit=limit,offset=offset)
    playlists = []
    for playlist_json in playlists_json['items']:
        playlists.append(Playlist(playlist_json))
    return playlists

#gets the content from the users playlists and returns a models.Track[]
def get_playlist_content(user,playlistid=None,fields=None):
    sp = spotipy.Spotify(auth=get_token())
    all_tracks_json = []
    results = sp.user_playlist(username, playlistid,fields="tracks,next")
    tracks = results['tracks']
    all_tracks_json.append(results['tracks'])
    while tracks['next']:
        all_tracks_json.append(sp.next(tracks))
    all_tracks_j = all_tracks_json[0]['items']
    all_tracks = []
    for track in all_tracks_j:
        all_tracks.append(Track(track,is_playlist_track=True))
    return all_tracks

#expects a models.playlist and models.Tracks[]
def add_songs_to_playlist(user, playlist,songs=[]):
    sp = spotipy.Spotify(auth=get_token())

    list_of_songs = []
    for song in songs:
        list_of_songs.append(song.id)

    sp.user_playlist_add_tracks(username, playlist_id=playlist.id, tracks=list_of_songs)

#returns a models.Track object from the id 
def get_track(track_id):
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    track_json = sp.track(track_id)
    return Track(json)

#returns models.Track[] for all the trackids
def get_tracks(track_ids):
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    tracks_json = sp.tracks(track_ids)
    tracks = []
    for track_json in tracks_json['tracks']:
        tracks.append(Track(track_json))
    return tracks

#Returns the current track playing 
def get_current_track():
    sp = spotipy.Spotify(auth=get_token())
    json = sp.current_user_playing_track()
    #TODO Need to handle if no track is playing
    #TODO Need to store the other data provided , time till finish , is_playing ,check if its a song 
    track = json['item']
    return Track(track)

#creates a new playlist from a models.Track[] object
def create_playlist(user,playlist_name,tracks_to_add,description=''):
    sp = spotipy.Spotify(auth=get_token())
    #Need to test this 
    playlist = Playlist(sp.user_playlist_create(user, playlist_name, public=True, description=description))
    
    tracks = []
    for track in tracks_to_add:
        tracks.append(track)
    sp.user_playlist_add_tracks(user, playlist.id , tracks, position=None)
    return None
