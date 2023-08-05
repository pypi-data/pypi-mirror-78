import os
from threading import Thread
from time import time, sleep
from datetime import datetime

import cv2
import numpy as np


class Camera:
    """
    Class to run a webcam recording in a background thread. Current frame can be accessed through self.current_frame attribute
    """

    def __init__(self):
        self.current_frame = None
        self.cap = cv2.VideoCapture(0)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)

    def read(self):
        return True, self.current_frame

    def start(self):
        while True:
            ret, frame = self.cap.read()
            self.current_frame = frame

    def start_on_background(self):
        proc = Thread(target=self.start, daemon=True)
        proc.start()
        sleep(3)
        return proc


class VisualMovementDetector:

    def __init__(self, out_detections_dir, n_avg_frames, min_recording_time_after_detection=5, blur_kernel_size=5, min_cnt_area=700, out_fps=20, notif_bot=None):

        self.n_avg_frames = n_avg_frames
        self.avg_factor = 1.0 / self.n_avg_frames
        self.blur_kernel_size = blur_kernel_size
        self.min_cnt_area = min_cnt_area
        self.date = datetime.now().strftime("%d-%m-%Y")
        self.out_detections_dir = os.path.join(out_detections_dir, self.date)
        os.makedirs(self.out_detections_dir, exist_ok=True)
        self.last_detection_time = 0
        self.min_recording_time_after_detection = min_recording_time_after_detection
        self.out_fps = float(out_fps)
        self.notif_bot = notif_bot
        self.current_frame = np.zeros((256, 256), dtype=np.uint8)

    def _set_bg(self, frame):
        self.bg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    def add_frame_to_buffer(self, frame):
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.bg = cv2.addWeighted(self.bg, 1 - self.avg_factor, frame_gray, self.avg_factor, gamma=0)

    def evaluate_frame(self, frame):

        if self.bg is None:
            self._set_bg(frame)

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        proc_bg = cv2.GaussianBlur(self.bg, ksize=(self.blur_kernel_size, self.blur_kernel_size), sigmaX=0).astype(float)
        proc_frame = cv2.GaussianBlur(frame_gray, ksize=(self.blur_kernel_size, self.blur_kernel_size), sigmaX=0).astype(float)

        diff = np.abs(proc_bg - proc_frame)

        disp_diff = diff.astype(np.uint8)
        thresh = cv2.threshold(disp_diff, 25, 255, cv2.THRESH_BINARY)[1]

        cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        detection = False

        for c in cnts:
            if cv2.contourArea(c) > self.min_cnt_area:
                detection = True
                self.last_detection_time = time()
                break

        return detection

    def start(self, camera_instance: Camera):

        frame = camera_instance.current_frame
        self._set_bg(frame)

        video_writer = cv2.VideoWriter()
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        h, w = frame.shape[0:2]

        out_video_path = None
        while True:
            frame = camera_instance.current_frame
            detection = self.evaluate_frame(frame)
            curr_t = time()
            last_det_elapsed = curr_t - self.last_detection_time
            if detection or last_det_elapsed < self.min_recording_time_after_detection:

                # cv2.imshow('Movement detected!', frame)  # for debugging
                # cv2.waitKey(30)
                if not video_writer.isOpened():
                    det_time = datetime.now().strftime("%H:%M:%S")
                    msg = f'Intruder detected!! Time:  {self.date}_{det_time}'
                    print(msg)
                    if self.notif_bot is not None:
                        self.notif_bot.send_message(msg)

                    out_video_path = os.path.join(self.out_detections_dir, f'det_{det_time}.mp4')
                    video_writer.open(filename=out_video_path, fourcc=fourcc, fps=self.out_fps, frameSize=(w, h))

                video_writer.write(frame)

            else:
                cv2.destroyAllWindows()
                video_writer.release()
                if self.notif_bot is not None and out_video_path is not None:
                    self.notif_bot.send_video(out_video_path)
                    out_video_path = None

            self.add_frame_to_buffer(frame)
