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
    
    def get_top_artists(self, limit=90, time_range='long_term', save_to_csv=False):
        #spotify api track limit bypass
        if limit <= 50:
            items = self.sp_client.current_user_top_artists(limit=limit, time_range=time_range)['items'] 
        else:
            items = self.sp_client.current_user_top_artists(limit=40, time_range=time_range)['items'] 
            items += self.sp_client.current_user_top_artists(limit=limit-40, offset=40, time_range=time_range)['items'] 
        
        df = pd.DataFrame(items, columns=['name','genres','popularity'])

        if save_to_csv: 
            df.to_csv('top_artists.csv')
            print('top_artists.csv saved to disk')

        return df
    
    def get_top_tracks(self, limit=90, time_range='long_term', save_to_csv=False):

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

        items = [get_track_details(item) for item in items]
        
        df = pd.DataFrame(items)
        
        if save_to_csv: 
            df.to_csv('top_tracks.csv')
            print('top_tracks.csv saved to disk')

        return df