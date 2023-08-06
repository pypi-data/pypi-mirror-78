# GuardCam
Visual movement detector with remote notification utilities

## Installation

    pip install guardcam

## Usage

Use guardcam-start-detector entry point command in a terminal:

```bash
guardcam-start-detector [-h] -o OUTDIR [-nF NUMAVGFRAMES] [-bS BLURKERNELSIZE] [-rT RECORDTIME] [--streamingPort STREAMINGPORT]
                               [--notificationBotName NOTIFICATIONBOTNAME] [--notificationUserName NOTIFICATIONUSERNAME]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTDIR, --outDir OUTDIR
                        Output directory to store the detections captures
  -nF NUMAVGFRAMES, --numAvgFrames NUMAVGFRAMES
                        Number of averaging frames
  -bS BLURKERNELSIZE, --blurKernelSize BLURKERNELSIZE
                        Blur kernel size
  -rT RECORDTIME, --recordTime RECORDTIME
                        Minimum recording time after detection in seconds
  --streamingPort STREAMINGPORT
                        Port for live video streaming. If None, no video streaming is served
  --notificationBotName NOTIFICATIONBOTNAME
                        Notification bot name
  --notificationUserName NOTIFICATIONUSERNAME
                        Notification target user name
```

- If --streamingPort is set, the detector will serve live video streaming from the default webcam on the input port
- If --notificationBotName and --notificationUserName are set, the detector app will try to extract the corresponding 
telegram bot token and user chat id from a credentials file located in $HOME/.guardcam/credentials.json. This credentials file 
must follow the following structure:
```json
{
  "bot_tokens": {
       "cam_botX": "0000000:XXXXXXXXXXXXXX",
       "cam_botY": "0000000:XXXXXXXXXXXXXX",
       ...
  },
  "user_ids": {
       "john_doe": "0101011110010",
       "jane_doe": "0101011110010",
       ...
  }
}
```

## Example

```bash
guardcam-start-detector -o /home/user/guardcam_captures -nF 2 -bS 7 -rT 5 --streamingPort 8192 --notificationBotName cam_botX --notificationUserName john_doe
```
