# Spotify-Clustering

[Live 3d-plot](https://progs2002.github.io/SpotifyGenreClustering/)

An ongoing effort to leverage the Spotify API and perform various tasks like :- 
* gathering the user's top tracks along with audio features and saving it as a csv
* gathering the user's top artists 
* creating a playlist of top tracks 
* getting all liked songs, creating feature vectors and clustering them in 3d (using t-SNE and k-means)

## Setting up

Install the required modules with ```$ pip install -r requirements.txt```

To actually call the spotify api, you would need to create a demo app on [developer.spotify.com](https://developer.spotify.com/) to get a ```CLIENT_ID``` and ```CLIENT_SECRET``` for your app.

Now create a  ```.env``` file with your ```CLIENT_ID``` and ```CLIENT_SECRET``` tokens like :-

``` txt
CLIENT_ID=*******************
CLIENT_SECRET=****************
```
## Running the script

Gathering top tracks and saving to disk as csv.
These tracks can be either long term(default), short term or medium term specified with the -t flag.
Filename is specified by the -n flag.
Use -h or --help for further details.

```sh
python main.py top_tracks -t long -n long_term_fav_tracks.csv
```

Gathering top artists and saving to disk as csv 
These artists can be either long term, short term or medium term specified with the -t flag.
Use -h or --help for further details

```sh
python main.py top_artists -t long -n long_term_fav_artists.csv
```

Creating a playlist of top tracks.
Time range is again specified with the -t flag.

```sh
python main.py playlist -t long
```

Clustering all liked songs (more tracks are usually needed for clustering)
Number of clusters is specified with the -k flag, 3 by default.

```sh
python main.py cluster -k 3
```

Below is a link to a live 3d plot of all my liked songs clustered with k=3  
[Live 3d plot](https://progs2002.github.io/SpotifyGenreClustering/)
