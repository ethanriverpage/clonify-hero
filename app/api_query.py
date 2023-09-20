import json
import os
import re
import requests
from download_handler import DownloadHandler

download = DownloadHandler()


class APIQuery:
    def __init__(self):
        pass

    def chorus_api_query(self, title_matching):
        with open("songs.json") as json_file:
            data = json.load(json_file)

        existing_data = {"songs": []}
        if os.path.exists("response.json"):
            with open("response.json", "r") as f:
                existing_data = json.load(f)

        for song in data:
            search = song["search"].replace("'", "")
            search = re.sub(r"[^\w\d\s']", "", search)
            print(f"Searching for: " + search)
            response = requests.get(
                "https://chorus.fightthe.pw/api/search/",
                params={"query": search},
                timeout=20,
            )

            if "songs" in response.json() and response.json()["songs"]:
                for i in range(len(response.json()["songs"])):
                    new_song = {
                        "songs": {
                            "name": response.json()["songs"][i]["name"],
                            "artist": response.json()["songs"][i]["artist"],
                            "link": response.json()["songs"][i]["link"],
                            "directLinks": response.json()["songs"][i]["directLinks"],
                        }
                    }
                    if title_matching:
                        if new_song["songs"]["name"] == song["name"]:
                            print(f"Found chart {i}: " + new_song["songs"]["name"])
                            existing_data["songs"].append(new_song)
                        else:
                            print(
                                f"Found chart {i}, but title doesn't match. Skipping..."
                            )
                            continue
                    elif not title_matching:
                        print(f"Found chart {i}: " + new_song["songs"]["name"])
                        existing_data["songs"].append(new_song)

            else:
                print("No chart found...")
            with open("response.json", "w") as f:
                json.dump(existing_data, f)

    def chorus_api_parse(self):
        with open("response.json") as f:
            api_response = json.load(f)

        for song in api_response["songs"]:
            songname = re.sub(r"[^\w]", "", (song["songs"]["name"]))
            songartist = re.sub(r"[^\w]", "", (song["songs"]["artist"]))
            file_path = os.path.join("songs", f"{songartist}_{songname}")
            i = 1
            while os.path.exists(file_path):
                file_path = os.path.join("songs", f"{songartist}_{songname}_{i}")
                i += 1
            os.makedirs(file_path)
            for key in song["songs"]["directLinks"]:
                url = song["songs"]["directLinks"][key]
                try:
                    if "google" in url:
                        file_id_parse = re.split(r"=|&", url)
                        download.drive_download(
                            file_id=file_id_parse[1], file_path=file_path
                        )
                    else:
                        download.other_download(url=url, file_path=file_path)
                except Exception as e:
                    print(f"Could not download {url}: {e}")
