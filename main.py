#!/usr/bin/python

from userdata import SpotifyUser

if __name__ == '__main__':
    sp = SpotifyUser()
    sp.get_top_tracks(save_to_csv=True)
    sp.get_top_artists(save_to_csv=True)

