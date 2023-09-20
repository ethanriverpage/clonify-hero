import argparse
import logging
import os
from file_handler import FileHandler
from api_query import APIQuery
from spotify_handler import SpotifyHandler
from download_handler import DownloadHandler
from dotenv import load_dotenv

file = FileHandler()
api = APIQuery()
spotify = SpotifyHandler()
download = DownloadHandler()

load_dotenv()


def file_check():
    prompt = input(
        "1. New session \n2. Use previous session\n3. Extract all archives\n... "
    )
    if prompt == "1":
        if os.path.exists("response.json"):
            os.remove("response.json")
        if os.path.exists("songs.json"):
            os.remove("songs.json")
        return 1
    elif prompt == "2":  # Parse api, extract archives, cleanup
        return 2
    elif prompt == "3":  # Extract archives, cleanup
        return 3
    else:
        print("Invalid input. Valid options are: '1','2','3'")


def title_matching_check() -> bool:
    title_matching = input(
        "Would you like the chart title to match the song title? \nIf not, you may grab songs that are covers or don't exactly match. (Y/n)\n... ? "
    )
    if title_matching.lower() == "y":
        return True
    elif title_matching.lower() == "n":
        return False
    elif not title_matching.lower() == "y" or not title_matching.lower() == "n":
        print("Invalid input. Valid options are 'y' and 'n'.\n... ")
        title_matching = input()


def main(args):
    logging.basicConfig(level=logging.INFO)
    print("Starting up...")
    if args.verbose:
        logging.info("Verbose mode enabled.")

    user_options = file_check()
    if user_options == 1:
        url = input("Paste the Spotify playlist URL here: ")
        title_matching = title_matching_check()
        download.gdrive_authenticate()
        spotify.spotify_data(url)
        api.chorus_api_query(title_matching=title_matching)
        api.chorus_api_parse()
        file.extract_archives(".\\songs")
        file.file_cleanup()
    elif user_options == 2:
        download.gdrive_authenticate()
        api.chorus_api_parse()
        file.extract_archives(".\\songs")
        file.file_cleanup()
    elif user_options == 3:
        file.extract_archives(".\\songs")
        file.file_cleanup()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="enable verbose mode"
    )
    args = parser.parse_args()

    main(args)
