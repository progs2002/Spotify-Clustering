#!/usr/bin/python

from userdata import SpotifyUser
from clusters import plot_clusters
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="mode")
    top_tracks = subparsers.add_parser('top_tracks', help="get top tracks of specified time range along with track features")
    top_artists = subparsers.add_parser('top_artists', help="get top artists of specified time range")
    playlist = subparsers.add_parser('playlist', help="create/update a playlist with top tracks of specified time range")
    cluster = subparsers.add_parser('cluster', help="3d plot all liked songs grouped into specified number of clusters")
    top_tracks.add_argument('-t', choices=['long','medium','short'], default='long')
    top_tracks.add_argument('-n', required=True, help='csv filename')
    top_artists.add_argument('-t', choices=['long','medium','short'], default='long')
    top_artists.add_argument('-n', required=True, help='csv filename')
    playlist.add_argument('-t', choices=['long','medium','short'], default='long')
    cluster.add_argument('-k', default=3, help='number of clusters')
    args = parser.parse_args()

    sp = SpotifyUser()

    if args.mode == 'top_tracks':
        sp.get_top_tracks(f'{args.t}_term', csv_filename=args.n)
    elif args.mode == 'top_artists':
        sp.get_top_artists(f'{args.t}_term', csv_filename=args.n)
    elif args.mode == 'playlist':
        sp.create_playlist(f'{args.t}_term')
    elif args.mode == 'cluster':
        plot_clusters(int(args.k))
