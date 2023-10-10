#!/usr/bin/python

from userdata import SpotifyUser

def main():
    sp = SpotifyUser()
    sp.get_top_tracks(time_range='long_term', csv_filename='top_tracks_long.csv')
    sp.get_top_tracks(time_range='medium_term', csv_filename='top_tracks_medium.csv')
    sp.get_top_tracks(time_range='short_term', csv_filename='top_tracks_short.csv')
    sp.get_top_artists(csv_filename='top_artists.csv')
    sp.create_playlists()

if __name__ == '__main__':
    main()