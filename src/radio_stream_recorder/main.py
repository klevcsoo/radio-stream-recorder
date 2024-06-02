from argparse import ArgumentParser
from time import sleep

import schedule

from config import AppConfig
from config import load_config
from drive import upload_recording
from stream import record_stream


def run_recording_once(config: AppConfig):
    recording_path = record_stream(config)
    if config.drive_service_account_path is not None:
        upload_recording(config, recording_path)


def main():
    parser = ArgumentParser(prog="Online Radio Stream Recorder")
    parser.add_argument(
        "--config-file", type=str, default="config.properties", required=True
    )
    args = parser.parse_args()
    try:
        config = load_config(args.config_file)
    except Exception as e:
        print(f"Configuration error: {e}")
        exit(1)

    if config.scheduler_start_at is None:
        print("\nStarting one-time recording...")
        run_recording_once(config)
        print("Done.")
    else:
        schedule.every().day.at(config.scheduler_start_at).do(
            run_recording_once, config
        )
        print("\nScheduler started")
        while True:
            schedule.run_pending()
            sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting process...")
        exit(0)
