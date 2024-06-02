import re
from configparser import ConfigParser
from dataclasses import dataclass, fields
from pathlib import Path


@dataclass
class AppConfig:
    stream_url: str
    recording_duration: str
    recording_output_directory: Path
    recording_filename: str
    scheduler_start_at: str | None
    drive_service_account_path: Path | None
    drive_parent_folder_id: str | None

    def __str__(self):
        return "\n".join(
            [f"{f.name} = {self.__dict__.get(f.name)}" for f in fields(self.__class__)])


__REC_DURATION_PATTERN = "^[0-9][0-9]:[0-9][0-9]:[0-9][0-9]$"
__START_AT_PATTERN = "^([0-1][0-9]|(2[0-4])):[0-6][0-9]$"


def load_config(config_file_path) -> AppConfig:
    section_name = "CONFIG_SECTION"
    with open(config_file_path, "r") as f:
        config_string = f"[{section_name}]\n" + f.read()
    config = ConfigParser(interpolation=None)
    config.read_string(config_string)
    cfg_section = config[section_name]

    stream_url = cfg_section.get("stream.url", None)
    if stream_url is None:
        raise Exception("Stream URL missing or invalid")

    rec_duration = cfg_section.get("recording.duration", None)
    if rec_duration is None or re.match(__REC_DURATION_PATTERN, rec_duration) is None:
        raise Exception("Duration of recording missing or invalid")

    out_dir = Path(cfg_section.get("recording.output_directory", "recordings"))
    if not out_dir.is_dir():
        raise Exception("Recording output directory does not exist")

    out_file = cfg_section.get("recording.filename", "stream_%date%_%time%.mp3")

    start_at = cfg_section.get("scheduler.start_at", None)
    if start_at is not None and re.match(__START_AT_PATTERN, start_at) is None:
        raise Exception("Recording starting time is invalid")

    service_account: Path | None = Path(
        cfg_section.get("google_drive.service_account_path", "gdrive-service-account.json"))
    if not service_account.is_file():
        service_account = None

    parent_id = cfg_section.get("google_drive.parent_folder_id", None)

    return AppConfig(
        stream_url=stream_url,
        recording_duration=rec_duration,
        recording_output_directory=out_dir,
        recording_filename=out_file,
        scheduler_start_at=start_at,
        drive_service_account_path=service_account,
        drive_parent_folder_id=parent_id,
    )
