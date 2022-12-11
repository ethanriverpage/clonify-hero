import os
import json
import spotipy
import requests
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import urllib.request
import urllib.parse
import cgi
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaIoBaseDownload
import re
import io

load_dotenv()

# Replace these with your own Spotify API credentials
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

creds = service_account.Credentials.from_service_account_file("service_account.json")
if True:
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secrets.json", scopes=["https://www.googleapis.com/auth/drive.file"]
    )
    creds = flow.run_console()

creds_dict = json.loads(creds.to_json())
creds = Credentials.from_authorized_user_info(info=creds_dict)


def SpotifyData():
    # The URL of the playlist you want to get the songs from
    playlist_url = input("Paste the Spotify playlist URL here: ")

    # Use the SpotifyClientCredentials class to authenticate with the Spotify API
    client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Parse the playlist URL to get the playlist's ID
    playlist_id = playlist_url.split("?")[0].split("/")[4]
    print(playlist_id)

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
    if os.path.exists("response.json") or os.path.exists("songs.json"):
        overwrite = input("File already exists! Would you like to overwrite it? (y/n) ")
        if overwrite == "y":
            os.remove("response.json")
            os.remove("songs.json")
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
                # How to get this to check if song already exists in existing_data to avoid extra API queries?
                print(f"Found song: " + new_song["songs"]["name"])
                existing_data["songs"].append(new_song)
        else:
            print("...")

        # Write the combined data back to the file
        with open("response.json", "w") as f:
            json.dump(existing_data, f)


def ChorusAPIParse():
    with open("response.json") as f:
        api_response = json.load(f)

    if not os.path.exists("songs"):
        os.makedirs("songs")

    for song in api_response["songs"]:
        try:
            url = song["songs"]["directLinks"]["archive"]
            remotefile = urllib.request.urlopen(url)
            remotefile_info = remotefile.info()["Content-Disposition"]
            value, params = cgi.parse_header(remotefile_info)
            file_name = params["filename"]
            file_path = os.path.join("songs", file_name)
            try:
                if not os.path.exists(file_path):
                    urllib.request.urlretrieve(url, file_path)
                    print(f"Song downloaded: {song['songs']['name']}")
                else:
                    print(f"Already downloaded: {song['songs']['name']}")
            except Exception as e:
                print(f"Failed to download: {song['songs']['name']}: {e}")
        except:
            for key in song["songs"]["directLinks"]:
                os.makedirs(
                    os.path.join("songs", (song["songs"]["name"])), exist_ok=True
                )
                url = song["songs"]["directLinks"][key]

                if not "google" in url:
                    try:
                        remotefile = urllib.request.urlopen(url)
                        remotefile_info = remotefile.info()["Content-Disposition"]
                        value, params = cgi.parse_header(remotefile_info)
                        file_name = params["filename"]
                        file_path = os.path.join("songs", (song["songs"]["name"]))
                        file_path_join = os.path.join(file_path, file_name)
                        try:
                            if not os.path.exists(file_path_join):
                                urllib.request.urlretrieve(url, file_path_join)
                                print(f"File downloaded: {file_path}")
                            else:
                                print(f"Already downloaded: {song['songs']['name']}")
                        except Exception as e:
                            print(f"Failed to download: {song['songs']['name']}: {e}")
                    except Exception as e:
                        print(f"Invalid URL: " + url)
                        print(f"Exception: {e}")
                else:
                    service = build("drive", "v3", credentials=creds)
                    file_id = re.split(r"=|&", url)
                    print(file_id)
                    request = service.files().get_media(fileId=file_id[1])
                    fh = io.BytesIO()
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while done is False:
                        status, done = downloader.next_chunk()
                        print("Download %d%%." % int(status.progress() * 100))

        # print(f"Link: {song['songs']['link']}")
        # print(f"DL: {song['songs']['directLinks']['archive']}")


FileCheck()
SpotifyData()
ChorusAPIQuery()
ChorusAPIParse()
