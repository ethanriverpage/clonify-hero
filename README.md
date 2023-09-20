# Clonify Hero: Find Clone Hero charts from a Spotify playlist
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit) [![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Description

Clonify Hero is a Python script to find & download Clone Hero charts from [chorus](https://chorus.fightthe.pw/) based on the songs within a Spotify playlist.

These songs are placed within the `./songs` directory, to then be copied to your Clone Hero `songs` directory.

**This project is for educational and research purposes only. It is not intended to be deployed as a fully functional or production-ready application.**
**Please be aware that this project may not be fully functional or optimized for actual usage.**

## Features

- Finding and downloading charts from a Spotify playlist
- Using Google's OAuth2 API to avoid rate limiting when downloading Google Drive files
- Auto-extraction of charts within an archive
- CLI interface with options of different functionality
- And more...

## Unimplemented Features

- Ability to search for charts containing specific instruments.
- Ability to specify download location.

## Known Issues

- If an invalid Spotify URL is provided (esp. private playlists), the script will throw an exception.
- Extracting may fail sporadically.
- Song title matching isn't great, because of extra words like "Remaster" in Spotify's song titles.
- Large playlists (e.g. > 100 songs) may fail.

## Environment Variables

1. `SPOTIFY_CLIENT_ID`: Specify your Spotify Web API's Client ID here.
2. `SPOTIFY_CLIENT_SECRET`: Specify your Spotify Web API's Client secret here.
   
   All these variables are defined in the `.env` file.

## Usage

1. You must set up a service account and an OAuth2 account with Google's APIs. Check out Google Cloud's documentation [here](https://cloud.google.com/docs/authentication) for more information.

```
service_account.json, client_secrets.json, and credentials.json are stored in the root directory of the project.
```

2. You need to create an app for Spotify's Web API and include your Client ID and secret within the `.env` file. Check out Spotify for Developers' documentation [here](https://developer.spotify.com/documentation/web-api) for more information.

3. Install the required modules using pip:

```
pip install -r requirements.txt
```

4. Run the script with Python:

```
python main.py
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Credits

- **[Paturages](https://github.com/Paturages) for his absolutely game-changing and crucial [Clone Hero-friendly Organized Repository of User-provided Songs](https://github.com/Paturages/chorus/).**
- [Spotify](https://spotify.com) for their [Web API](https://developer.spotify.com/documentation/web-api) which is required for this project.
- [Google Cloud](https://cloud.google.com/?hl=en) for their [Authentication and Drive APIs](https://cloud.google.com/docs) which is necessary for file downloads and avoiding rate-limiting.

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0). You can find the full license text in the [LICENSE](LICENSE) file.
