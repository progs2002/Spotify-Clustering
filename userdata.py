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
        
        self.scope = "user-library-read user-top-read" if scope is None else scope

        self.sp_client = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=self.client_id,
                client_secret=self.client_secret,
                scope=self.scope,
                redirect_uri=self.redirect_uri
            )
        )

    def get_track_features(self, track_ids):

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

        tracks_features = self.sp_client.audio_features(track_ids)
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

    def get_top_artists(self, limit=90, time_range='long_term', csv_filename=None):
        #spotify api track limit bypass
        if limit <= 50:
            items = self.sp_client.current_user_top_artists(limit=limit, time_range=time_range)['items'] 
        else:
            items = self.sp_client.current_user_top_artists(limit=40, time_range=time_range)['items'] 
            items += self.sp_client.current_user_top_artists(limit=limit-40, offset=40, time_range=time_range)['items'] 
        
        df = pd.DataFrame(items, columns=['name','genres','popularity'])

        if csv_filename: 
            df.to_csv(csv_filename)
            print(csv_filename)

        return df
    
    
    def get_top_tracks(self, limit=90, time_range='long_term', csv_filename=None):

        def get_track_details(item):
            
            return {
                'name': item['name'],
                'artist': item['album']['artists'][0]['name'],
                'album': item['album']['name'],
                'popularity': item['popularity']
            }

        if limit <= 50:
            items = self.sp_client.current_user_top_tracks(limit=limit, time_range=time_range)['items'] 
        else:
            items = self.sp_client.current_user_top_tracks(limit=40, time_range=time_range)['items'] 
            items += self.sp_client.current_user_top_tracks(limit=limit-40, offset=40, time_range=time_range)['items'] 

        track_ids = [item['id'] for item in items]
        track_features_df = self.get_track_features(track_ids)

        items = [get_track_details(item) for item in items]
        items_df = pd.DataFrame(items)

        df = pd.concat([items_df, track_features_df], axis=1)
        
        if csv_filename: 
            df.to_csv(csv_filename)
            print(csv_filename)

        return df
    