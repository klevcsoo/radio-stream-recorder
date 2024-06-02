from pathlib import Path

from oauth2client.service_account import ServiceAccountCredentials
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

from config import AppConfig


def upload_recording(config: AppConfig, path: Path):
    if config.drive_service_account_path is None:
        return

    scope = ["https://www.googleapis.com/auth/drive"]

    gauth = GoogleAuth()
    gauth.auth_method = 'service'
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
        config.drive_service_account_path, scope
    )

    drive = GoogleDrive(gauth)

    print(f"Authenticated as {drive.GetAbout()['name']}")

    file = drive.CreateFile({
        "title": path.name,
        "parents": [{"id": config.drive_parent_folder_id}]
    })
    file.SetContentFile(path)
    file.Upload()

    print(f"Google Drive uplod completed")
