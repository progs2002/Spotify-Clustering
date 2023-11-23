import os 
from dotenv import load_dotenv

import spotipy 
from spotipy.oauth2 import SpotifyOAuth

import pandas as pd 


class SpotifyUser:
    def __init__(self, redirect_uri=None, scope=None):
        load_dotenv()
        self.client_id = os.environ['CLIENT_ID']
        self.client_secret = os.environ['CLIENT_SECRET']
        
        self.redirect_uri = 'http://localhost:3000'if redirect_uri is None else redirect_uri
        
        self.scope = "user-library-read user-top-read playlist-modify-private playlist-modify-public user-read-private" if scope is None else scope

        self.sp_client = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=self.client_id,
                client_secret=self.client_secret,
                scope=self.scope,
                redirect_uri=self.redirect_uri
            )
        )

    def _get_track_features(self, uris):
        audio_feats = []
        
        for i in range(0,len(uris),100):
            audio_feats += self.sp_client.audio_features(uris[i:i+100])
        
        return audio_feats

    def get_track_features(self, uris):

        feature_columns = [
            'acousticness',
            'danceability',
            'energy',
            'instrumentalness',
            'key',
            'liveness',
            'loudness',
            'mode',
            'speechiness',
            'tempo',
            'time_signature',
            'valence'
        ]

        tracks_features = self._get_track_features(uris)
        tracks_features_df = pd.DataFrame(tracks_features, columns=feature_columns)
        
        #fix key
        keys = ['NotDetected','C','C#','D','Eb','E','F','F#','G','G#','A','Bb','B']
        tracks_features_df['key'] = tracks_features_df['key'].apply(
            lambda x: keys[x + 1]
        )

        #fix mdoe
        tracks_features_df['mode'] = tracks_features_df['mode'].apply(
            lambda x: 'Major' if x == 1 else 'minor'
        )

        #fix time_signature
        tracks_features_df['time_signature'] = tracks_features_df['time_signature'].apply(
            lambda x: f'{x}/4'
        )

        return tracks_features_df
    
    def save_to_csv(self, df, csv_filename):
        df.drop('uri',axis=1).to_csv(csv_filename)
        print(f'{csv_filename} saved to disk')

    def get_top_artists(self, time_range, limit=90, csv_filename=None):
        #spotify api track limit bypass
        if limit <= 50:
            items = self.sp_client.current_user_top_artists(limit=limit, time_range=time_range)['items'] 
        else:
            items = self.sp_client.current_user_top_artists(limit=40, time_range=time_range)['items'] 
            items += self.sp_client.current_user_top_artists(limit=limit-40, offset=40, time_range=time_range)['items'] 
        
        df = pd.DataFrame(items, columns=['name','genres','popularity'])

        if csv_filename:
            self.save_to_csv(df, csv_filename)

        return df
    
    def get_track_details(self, item):    
        return {
            'name': item['name'],
            'artist': item['album']['artists'][0]['name'],
            'album': item['album']['name'],
            'popularity': item['popularity'],
            'uri': item['uri']
        }
    
    def get_top_tracks(self, time_range, limit=90, csv_filename=None):

        if limit <= 50:
            items = self.sp_client.current_user_top_tracks(limit=limit, time_range=time_range)['items'] 
        else:
            items = self.sp_client.current_user_top_tracks(limit=40, time_range=time_range)['items'] 
            items += self.sp_client.current_user_top_tracks(limit=limit-40, offset=40, time_range=time_range)['items'] 

        track_ids = [item['id'] for item in items]
        track_features_df = self.get_track_features(track_ids)

        items = [self.get_track_details(item) for item in items]
        items_df = pd.DataFrame(items)

        df = pd.concat([items_df, track_features_df], axis=1)

        if csv_filename:
            self.save_to_csv(df, csv_filename)

        return df
        
    def create_playlists(self, time_range):
        user_id = self.sp_client.me()['id']

        tracks = self.get_top_tracks(time_range=time_range)

        #check if playlist exists
        playlists = self.sp_client.current_user_playlists()['items']
        playlist_name = f'{time_range}_fav_tracks'
        current_playlist_names = [p['name'] for p in playlists]
        is_present = playlist_name in current_playlist_names

        if not is_present:
            print('creating playlist')
            pl = self.sp_client.user_playlist_create(user=user_id, name=playlist_name, public=True)
            self.sp_client.playlist_add_items(pl['id'], tracks['uri'].values.tolist())
            print('playlist created, tracks added')    
        else:
            print('updating playlists')
            p_id = current_playlist_names.index(playlist_name)
            self.sp_client.playlist_replace_items(playlists[p_id]['uri'], tracks['uri'].values.tolist())
            print('playlist updated')

    def get_liked_songs(self, csv_filename=None):
        songs = []
        offset = 0
        
        print("fetching all liked songs.....")

        while True:
            out = self.sp_client.current_user_saved_tracks(limit=50, offset=offset)['items']
            if len(out) == 0:
                break
            songs += [ self.get_track_details(track['track']) for track in out ]
            offset += 50

        df = pd.DataFrame(songs)

        if csv_filename:
            self.save_to_csv(df, csv_filename)

        return df