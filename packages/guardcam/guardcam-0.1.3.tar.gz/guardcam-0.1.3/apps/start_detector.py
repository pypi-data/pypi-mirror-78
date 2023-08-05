import argparse
from threading import Thread

from guardcam.detection import VisualMovementDetector
from guardcam.streaming import Camera, VideoStreamingServer
from guardcam.notification import TelegramBot


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('-o', '--outDir', type=str, required=True, help='Output directory to store the detections captures')
    ap.add_argument('-nF', '--numAvgFrames', type=int, required=False, default=2, help='Number of averaging frames')
    ap.add_argument('-bS', '--blurKernelSize', type=int, required=False, default=7, help='Blur kernel size')
    ap.add_argument('-rT', '--recordTime', type=int, required=False, default=3, help='Minimum recording time after detection in seconds')
    ap.add_argument('-fps', '--outFPS', type=int, required=False, default=20, help='FPS for output detection captures')

    ap.add_argument('--streamingPort', type=int, required=False, default=None, help='Port for live video streaming. If None, no video streaming is served')
    ap.add_argument('--notificationTelegramBotCredentials', type=str, required=False, default=None, help='Bot credentials file to send notifications through Telegram. If None, disable notifications')
    return ap.parse_args()


def main():

    args = parse_args()

    bot_credentials = args.notificationTelegramBotCredentials
    notif_bot = TelegramBot(bot_credentials=bot_credentials) if bot_credentials is not None else None

    # start camera recording in background thread
    camera = Camera()
    cam_thread = camera.start_on_background()

    vmd = VisualMovementDetector(out_detections_dir=args.outDir,
                                 n_avg_frames=args.numAvgFrames,
                                 min_recording_time_after_detection=args.recordTime,
                                 blur_kernel_size=args.blurKernelSize,
                                 notif_bot=notif_bot)

    if args.streamingPort is None:
        vmd.start(camera_instance=camera)
    else:
        vmd_thread = Thread(target=vmd.start, kwargs={'camera_instance': camera}, daemon=True)
        vmd_thread.start()

        vss = VideoStreamingServer(port=args.streamingPort)
        vss.start(camera_instance=camera)


if __name__ == '__main__':
    main()
