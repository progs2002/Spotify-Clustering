#!/usr/bin/python

from userdata import SpotifyUser

if __name__ == '__main__':
    sp = SpotifyUser()
    sp.get_top_tracks(csv_filename='top_tracks.csv')
    sp.get_top_artists(csv_filename='top_artists.csv')

