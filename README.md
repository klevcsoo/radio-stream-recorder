# Online Radio Stream Recording Tool

This tool allows you to record an online audio stream
onto your local machine, and then upload the
recordings to Google Drive.

## Requirements

- python3
- pip3
- ffmpeg

## Setup

To run the script itself, all you need to do is

- clone the Git repository (or download as a ZIP then
  extract),
- create a virtual Python environment & install the
  required packages,
- execute the `main.py` script with the specified
  configuration
  file,

However, to customise the behaviour of the app or
launch it automatically on Unix systems, we need to
tweek the configuration.

## Configuration

The `main.py` entry script needs one argument, which
is the path to the _.properties_ file containing the
configuration.<br/>
For example (from the repository root):

```shell
python3 src/radio_stream_recorder/main.py --config-file configuration.properties
```

The app supports the following config properties:

| Name                              | Description                                                                                                                                                                                                                                                                                                                                                                                                          | Example value                               | Required |
|-----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------|----------|
| stream.url                        | The URL pointing to the live audio file.                                                                                                                                                                                                                                                                                                                                                                             | https://icast.connectmedia.hu/5201/live.mp3 | Yes      |
| recording.duration                | The duration of the recording as a string in the following format: "HH:mm:ss"                                                                                                                                                                                                                                                                                                                                        | 03:00:00                                    | Yes      |
| recording.output_directory        | The directory to which the recordings should be saved. **The app will not create the directory for you if it doesn't exist, so make sure that it does first.** Default value is the _recordings_ directory in the repository root.                                                                                                                                                                                   | /home/pi/Videos/recordings                  | No       |
| recording.filename                | The filename template that should be used for creating recordings. It supports interpolation, more on that below. Default value is _stream_%date%_%time%.mp3_.                                                                                                                                                                                                                                                       | recording_%date%_%day%_%type%.mp3           | No       |
| scheduler.start_at                | Time of the day when the scheduled recording should begin, in "HH:mm" format. If set, the app will start in **scheduled** mode, which means that every day, it will start recording at the given time for the given duration. If ommited, the app then starts in **one-time** mode, where the recording begins immediately and lasts for the given duration.                                                         | 21:00                                       | No       |
| google_drive.service_account_path | The path to the service account through which the Google Drive API should be accessed. I've got a guide below on how to get your on service account. If ommited, the app will look for it under the default path, which is **gdrive-service-account.json**. If that doesn't exist the app will not attempt to upload the recordings.                                                                                 | ./service-account.json                      | No       |
| google_drive.parent_folder_id     | The ID of the folder that the recordings should be placed inside on Google Drive. If ommited, the files won't be placed inside of any folder. I don't recommend not setting this property, because the uploaded recordings just sort of disappear (?), altough I'm no expert on the Google Drive API, so it might be possible I overlooked something. Without an existing service account, this property is ignored. | 10ONXcCMQUmU3o82etIzOxKVm_WLpWAL8           | No       |

> The example values above configure the app to start
> recording the stream of the Hungarian Rádió 1 radio
> channel every day at 9 PM for 3 hours, and then using
> the given service account, upload the recordings to
> Google Drive.

### Filename configuration

To customise the names of the recording files, you can
use the following "macros", which will be replaced
with their respective values at that moment:

| Macro    | Description                                                                                        |
|----------|----------------------------------------------------------------------------------------------------|
| `%date%` | Gets replaced with the currrent date in "YYYY-mm-dd" format. Example value: 2024-06-02.            |
| `%time%` | Gets replaced with the current time in "HH:MM:SS" format. Example value: 21:30:50.                 |
| `%day%`  | Gets replaced with the current day of the week in a three-letter short format. Example value: Sun. |
| `%type%` | Gets replaced with the type of the current recording. Can either be "one-time" or "scheduled".     |

### Google Drive API

If you'd like the app to automatically upload the
recordings to your Google Drive, you need to **create a
Google Cloud Platform project** and enable the API there.

1. Head to
   the [project creation page](https://console.cloud.google.com/projectcreate)
   and create a new
   project.
2. Using the search bar on the top or by
   following [this](https://console.cloud.google.com/marketplace/product/google/drive.googleapis.com)
   link, enable the Google Drive API for your project.
3. Go to
   the [API Credentials](https://console.cloud.google.com/apis/credentials)
   page and create a new **service account credential**.
4. Follow the instructions on screen, and create the
   service account.
5. Head to
   the [Service Accounts page](https://console.cloud.google.com/iam-admin/serviceaccounts)
   and
   select the one you've just created.
6. Switch to the _Keys_ tab (towards the top), click
   _ADD KEY_ and create a new **JSON key**.
7. Download the JSON key to a place of your choosing
   (I recommend the repository directory).
8. Lastly, set the **google_drive.
   service_account_path** property in your config file,
   and you're done!

## Registering the app as a service

If you plan on running this 24/7 on a server, I
recommend setting up some kind of auto-start feature.
<br/>
For example, on a Rapsberry PI running Raspbian OS (a
Debian-based Linux distro) it can be achieved by
registering a service. For this, you can find the
`example-run.sh` and the `example.service` in the repo
as references.

1. First, copy the service file (I recommend giving it a
   bit more descriptive name first).
    ```shell
    sudo cp radio_stream_recording.service /etc/systemd/system
    ```

2. Reload the daemon.
    ```shell
   sudo systemctl daemon-reload
    ```
3. Enable the service
    ```shell
   sudo systemctl enable radio_stream_recording.service
   ```
4. Start the service
   ```shell
   sudo systemctl start radio_stream_recording.service
   ```

Now, you can check on the status by running

```shell
sudo systemctl status radio_stream_recording.service
```

and view the live logs with

```shell
sudo journalctl -u radio_stream_recording -f
```
