import sys

from userdata import SpotifyUser
from sklearn.manifold import TSNE
from sklearn.preprocessing import MinMaxScaler
import pandas as pd 
from sklearn.cluster import KMeans
import plotly.express as px

from tqdm import trange

from userdata import SpotifyUser

def plot_3d(x, centroids, text):
    fig = px.scatter_3d(
        x=x[:,0],
        y=x[:,1],
        z=x[:,2],
        color=centroids,
        size=[3]*x.shape[0],
        hover_name=text,
        opacity=0.9,
        title="t-SNE visualisation of all liked songs grouped into clusters",
        width=1800,
        height=900
    )
    
    fig.update_coloraxes(showscale=False)
    fig.update_layout(legend_title_text="color")
    fig.show()

def pre_process_df(df):
    features = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'speechiness', 'valence']
    labels = ['name', 'artist', 'album']
    X = df[features]
    Y = df[labels]
    scaler = MinMaxScaler()
    X = scaler.fit_transform(X)
    text = Y['name']+"-"+Y['artist']
    return X, text

def get_centroids(x, k):
    kmeans = KMeans(k, n_init='auto')
    return kmeans.fit_predict(x)

def get_tsne_features(x, dim):
    return TSNE(dim).fit_transform(x)

def process_df(df,dim=3,k=3):
    X, text = pre_process_df(df)
    X_tsne = get_tsne_features(X, dim)
    centroids = get_centroids(X_tsne,k)
    print("preparing 3D scatterplot")
    plot_3d(X_tsne, centroids, text)

def main():
    sp = SpotifyUser()
    songs_df = sp.get_liked_songs()
    audio_feats = sp.get_track_features(songs_df['uri'])
    df1 = pd.DataFrame(audio_feats)
    df2 = songs_df
    print("processing features...")
    df = df1.join(df2)
    process_df(df,k=3)

if __name__ == "__main__":
    main()