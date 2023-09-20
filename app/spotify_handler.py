import os
import json
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyHandler:
    def __init__(self):
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    def spotify_data(self, url):
        sp_regex = r"\bhttps?:\/\/[^/]*\bspotify\.com\/playlist\/([^\s?]+)"
        url = url
        match = re.search(sp_regex, url)

        while not match:
            print("Invalid Spotify playlist URL. Please enter a valid url.")
            url = input("Paste the Spotify playlist URL here: ")
            match = re.search(sp_regex, url)

        client_credentials_manager = SpotifyClientCredentials(
            client_id=self.client_id, client_secret=self.client_secret
        )
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        playlist_id = re.search(sp_regex, url).group(1)
        print(f"Spotify playlist ID: {playlist_id}")

        results = sp.playlist_tracks(playlist_id)
        tracks = results["items"]
        while results["next"]:
            results = sp.next(results)
            tracks.extend(results["items"])

        songs = []
        for track in tracks:
            song_name = track["track"]["name"]
            artist_name = track["track"]["artists"][0]["name"]
            search = f"{song_name} {artist_name}"
            songs.append({"name": song_name, "artist": artist_name, "search": search})
        with open("songs.json", "w") as f:
            json.dump(songs, f)
