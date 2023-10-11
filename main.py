#!/usr/bin/python

from userdata import SpotifyUser

def main():
    sp = SpotifyUser()
    sp.create_playlists()

if __name__ == '__main__':
    main()