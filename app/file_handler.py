import os
import shutil
import py7zr
import rarfile


class FileHandler:
    def __init__(self):
        pass

    def extract_archives(self, directory):
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isdir(filepath):
                self.extract_archives(filepath)

            elif filename.endswith((".zip", ".tar", ".tgz", ".gz")):
                print(f"Extracting archive: {filepath}")
                shutil.unpack_archive(filepath, directory)
                os.remove(filepath)

            elif filename.endswith(".rar"):
                with rarfile.RarFile(filepath) as rf:
                    try:
                        print(f"Extracting archive: {filepath}")
                        rf.extractall(directory)
                        os.remove(filepath)
                    except Exception as e:
                        print(f"Could not extract {filepath}: {e}")

            elif filename.endswith(".7z"):
                with py7zr.SevenZipFile(filepath, mode="r") as z:
                    try:
                        print(f"Extracting archive: {filepath}")
                        z.extractall(path=directory)
                        os.remove(filepath)
                    except Exception as e:
                        print(f"Could not extract {filepath}: {e}")

    def file_cleanup(self):
        if os.path.exists("songs.json"):
            os.remove("songs.json")
        if os.path.exists("response.json"):
            os.remove("response.json")
        print("Exiting...")
        exit()
