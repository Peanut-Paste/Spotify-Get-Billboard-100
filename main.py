import requests
import spotipy
from bs4 import BeautifulSoup
import os

u_year = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
redirect_url = "http://localhost:8888/callback/"

url = "https://www.billboard.com/charts/hot-100/" + u_year

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
billboard_top = [container.find("h3", id="title-of-a-story").getText().strip()
                 for container in soup.find_all("div", class_="o-chart-results-list-row-container")]

sp_client_cre = spotipy.oauth2.SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=redirect_url,
    scope="playlist-modify-private"
)

sp = spotipy.client.Spotify(oauth_manager=sp_client_cre)
user = sp.current_user()

track_uri = [sp.search(q=f"track: {song} year: {int(u_year[:4])-1}-{u_year[:4]}",
                       type="track",
                       limit=1)["tracks"]["items"][0]["uri"]
             for song in billboard_top]

playlist = sp.user_playlist_create(
    user=user["id"],
    name=f"{u_year[:4]} Top 100 Billboard",
    public=False,
)

playlist_id = playlist["id"]

sp.playlist_add_items(playlist_id=playlist_id, items=track_uri)
