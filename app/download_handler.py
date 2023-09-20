import os
import json
import io
import re
import urllib.request
import cgi
import logging
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError


class DownloadHandler:
    def __init__(self):
        logging.getLogger("googleapiclient.discovery_cache").setLevel(logging.ERROR)
        self.creds = service_account.Credentials.from_service_account_file(
            "service_account.json"
        )

    def gdrive_authenticate(self):
        if os.path.exists("credentials.json"):
            with open("credentials.json", "r") as f:
                creds_json = f.read()
                creds_dict = json.loads(creds_json)
            self.creds = Credentials.from_authorized_user_info(info=creds_dict)
            print("Existing Google credentials found, continuing...")
        else:
            if True:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "client_secrets.json",
                    scopes=["https://www.googleapis.com/auth/drive"],
                )
            self.creds = flow.run_console()
            creds_json = self.creds.to_json()
            creds_dict = json.loads(creds_json)
            self.creds = Credentials.from_authorized_user_info(info=creds_dict)
            with open("credentials.json", "w") as f:
                f.write(creds_json)
                print("Saved Google credentials to credentials.json!")

    def grab_file_name(self, url):
        try:
            remotefile = urllib.request.urlopen(url)
            remotefile_info = remotefile.info()["Content-Disposition"]
            value, params = cgi.parse_header(remotefile_info)
            file_name = params["filename"]
        except Exception as e:
            raise Exception(e)
        return file_name

    def drive_download(self, file_id, file_path):
        try:
            service = build("drive", "v3", credentials=self.creds)

            file_metadata = service.files().get(fileId=file_id).execute()
            file_name = file_metadata["name"]
            file_name = re.sub(r"[^\w.]", "", file_name)
            file_location = os.path.join(str(file_path), str(file_name))

            request = service.files().get_media(fileId=file_id)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()

            with open(file_location, "wb") as f:
                print(f"[GDrive] File downloaded: {file_location}")
                f.write(file.getvalue())

        except HttpError as error:
            if error.resp.status == 404:
                print("The file does not exist or was not found.")
            else:
                print(f"An error occurred: {error}")
            file = None

    def other_download(self, url, file_path):
        try:
            file_name = self.grab_file_name(url=url)
            file_name = re.sub(r"[^\w.]", "", file_name)
            file_location = os.path.join(str(file_path), str(file_name))
            urllib.request.urlretrieve(url, file_location)
            print(f"[Other] File downloaded: {file_location}")
        except Exception as e:
            print(f"An error occured: {e}")
