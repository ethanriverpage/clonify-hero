import os
import json
import spotipy
import requests
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

# Replace these with your own Spotify API credentials
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")


def SpotifyData():
    # The URL of the playlist you want to get the songs from
    playlist_url = "https://open.spotify.com/playlist/10Attpbti1MIUH2Og2IgIv"

    # Use the SpotifyClientCredentials class to authenticate with the Spotify API
    client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Parse the playlist URL to get the playlist's ID
    playlist_id = playlist_url.split("/")[-1]

    # Use the Spotify API to get the tracks in the playlist
    results = sp.playlist_tracks(playlist_id)
    tracks = results["items"]
    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])

    # Extract the names of the songs and save them to a JSON file
    songs = []
    for track in tracks:
        song_name = track["track"]["name"]
        artist_name = track["track"]["artists"][0]["name"]
        search = f"{song_name} {artist_name}"
        songs.append({"name": song_name, "artist": artist_name, "search": search})
    with open("songs.json", "w") as f:
        json.dump(songs, f)


def FileCheck():
    if os.path.exists("response.json"):
        overwrite = input("File already exists! Would you like to overwrite it? (y/n)")
        if overwrite == "y":
            os.remove("response.json")
            print("Overwriting...")
        else:
            print("Skipping overwrite...")


def ChorusAPIQuery():
    with open("songs.json") as json_file:
        data = json.load(json_file)

    for song in data:

        search = song["search"].replace("'", "")
        print(f"Searching for: " + search)

        response = requests.get(
            "https://chorus.fightthe.pw/api/search/", params={"query": search}
        )

        if not os.path.exists("response.json"):
            # Initialize the file with an empty songs array
            existing_data = {"songs": []}
        else:
            # Read the existing JSON data from the file
            with open("response.json", "r") as f:
                existing_data = json.load(f)

        # Append the response to the existing JSON data
        if "songs" in response.json() and response.json()["songs"]:
            for i in range(len(response.json()["songs"])):
                new_song = {
                    "songs": {
                        "name": response.json()["songs"][i]["name"],
                        "link": response.json()["songs"][i]["link"],
                        "directLinks": response.json()["songs"][i]["directLinks"],
                    }
                }

            existing_data["songs"].append(new_song)

        # Write the combined data back to the file
        with open("response.json", "w") as f:
            json.dump(existing_data, f)


def ChorusAPIParse():
    with open("response.json") as f:
        api_response = json.load(f)

    for song in api_response["songs"]:
        print(f"Name: {song['songs']['name']}")
        print(f"Link: {song['songs']['link']}")
        print(f"DL: {song['songs']['directLinks']['archive']}")


SpotifyData()
FileCheck()
ChorusAPIQuery()
ChorusAPIParse()
