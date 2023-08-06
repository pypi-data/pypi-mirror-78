import os
import json
import argparse
from threading import Thread

from guardcam.detection import VisualMovementDetector
from guardcam.streaming import Camera, VideoStreamingServer


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('-o', '--outDir', type=str, required=True, help='Output directory to store the detections captures')
    ap.add_argument('-nF', '--numAvgFrames', type=int, required=False, default=3, help='Number of averaging frames')
    ap.add_argument('-bS', '--blurKernelSize', type=int, required=False, default=7, help='Blur kernel size')
    ap.add_argument('-rT', '--recordTime', type=int, required=False, default=5, help='Minimum recording time after detection in seconds')

    ap.add_argument('--streamingPort', type=int, required=False, default=None, help='Port for live video streaming. If None, no video streaming is served')
    ap.add_argument('--notificationBotName', type=str, required=False, default=None, help='Notification bot name')
    ap.add_argument('--notificationUserName', type=str, required=False, default=None, help='Notification target user name')
    return ap.parse_args()


def get_credentials(bot_name, user_id):
    home = os.path.expanduser('~')
    local_credentials_file = os.path.join(home, '.guardcam', 'credentials.json')
    with open(local_credentials_file, 'r') as fp:
        credentials_db = json.load(fp)

    credentials = {'token': credentials_db['bot_tokens'][bot_name],
                   'chat_id': credentials_db['user_ids'][user_id],
                   'name': 'GuardCam'}
    return credentials


def main():

    args = parse_args()

    # start camera recording in background thread
    camera = Camera()
    cam_thread = camera.start_on_background()

    if args.notificationBotName and args.notificationUserName:
        credentials = get_credentials(bot_name=args.notificationBotName,
                                      user_id=args.notificationUserName)
    else:
        credentials = None

    vmd = VisualMovementDetector(out_detections_dir=args.outDir,
                                 n_avg_frames=args.numAvgFrames,
                                 min_recording_time_after_detection=args.recordTime,
                                 blur_kernel_size=args.blurKernelSize,
                                 notif_bot_credentials=credentials)

    if args.streamingPort is None:
        vmd.start(camera_instance=camera)
    else:
        vmd_thread = Thread(target=vmd.start, kwargs={'camera_instance': camera}, daemon=True)
        vmd_thread.start()

        vss = VideoStreamingServer(port=args.streamingPort)
        vss.start(camera_instance=camera)


if __name__ == '__main__':
    main()
