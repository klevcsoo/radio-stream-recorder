import subprocess
from datetime import datetime
from pathlib import Path

import logs
from config import AppConfig


def resolve_filename(config: AppConfig) -> str:
    resolve_map = {
        "%date%": datetime.now().strftime("%Y-%m-%d"),
        "%time%": datetime.now().strftime("%H-%M-%S"),
        "%day%": datetime.now().strftime("%a"),
        "%type%": "one-time" if config.scheduler_start_at is None else "scheduled"
    }

    filename = config.recording_filename
    for key in resolve_map:
        filename = filename.replace(key, resolve_map[key])

    return filename


def record_stream(config: AppConfig) -> Path:
    def timestamp():
        return datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    logs.log_info(f"Recording stream at {logs.C_HEADER}{timestamp()}{logs.C_RESET}...")

    output_file_path = config.recording_output_directory.joinpath(resolve_filename(config))
    try:
        cmd = [
            "ffmpeg", "-y",
            "-i", config.stream_url,
            "-t", config.recording_duration,
            "-c", "copy",
            output_file_path
        ]

        subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        logs.log_info(f"Stream recording finished at {logs.C_HEADER}{timestamp()}")
        logs.log_info(f"File: {logs.C_HEADER}{output_file_path}")

        return output_file_path
    except subprocess.CalledProcessError as e:
        logs.log_error(f"Stream decode error occured: {e.stderr.decode()}")
        exit(1)
    except Exception as e:
        logs.log_error(f"An error occured: {e}")
        exit(1)
