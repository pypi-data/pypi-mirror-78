import os
from threading import Thread
from time import time, sleep
from datetime import datetime

import cv2
import numpy as np

from guardcam.notification import NotificationHandler


class Camera:
    """
    Class to run a webcam recording in a background thread.
    Current frame can be accessed through self.frame attribute
    Current frame read time can be accessed through self.read_time attribute (useful to sync i/o)
    """

    def __init__(self):
        self.frame = None
        self.read_time = None
        self.cap = cv2.VideoCapture(0)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)

    def read(self):
        return self.frame, self.read_time

    def start(self):
        while True:
            ret, frame = self.cap.read()
            self.frame = frame
            self.read_time = time()

    def start_on_background(self):
        proc = Thread(target=self.start, daemon=True)
        proc.start()
        sleep(3)
        return proc


class VisualMovementDetector:

    def __init__(self, out_detections_dir, n_avg_frames, min_recording_time_after_detection=5, blur_kernel_size=5, active_pixel_thr=0.1, notif_bot_credentials=None):

        self.n_avg_frames = n_avg_frames
        self.avg_factor = 1.0 / self.n_avg_frames
        self.blur_kernel_size = blur_kernel_size
        self.active_pixel_thr = active_pixel_thr
        self.date = datetime.now().strftime("%d-%m-%Y")
        self.out_detections_dir = os.path.join(out_detections_dir, self.date)
        os.makedirs(self.out_detections_dir, exist_ok=True)
        self.last_detection_time = 0
        self.min_recording_time_after_detection = min_recording_time_after_detection
        self.notif_handler = NotificationHandler(bot_credentials=notif_bot_credentials) if notif_bot_credentials is not None else None
        self._wf = -1
        self._hf = -1
        self.num_img_pixels = -1

    def _set_bg(self, frame):
        self.bg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        w, h = frame.shape[0:2]
        self._wf = w
        self._hf = h
        self.num_img_pixels = w * h

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
        thresh = cv2.threshold(disp_diff, 30, 255, cv2.THRESH_BINARY)[1]
        num_act_pixels = np.count_nonzero(thresh)
        if num_act_pixels / self.num_img_pixels <= self.active_pixel_thr:
            detection = False
        else:
            detection = True
            self.last_detection_time = time()

        return detection

    def start(self, camera_instance: Camera):

        frame, read_time = camera_instance.read()
        self._set_bg(frame)

        video_writer = cv2.VideoWriter()
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        h, w = frame.shape[0:2]

        out_video_path = None
        last_frame_read_time = read_time
        while True:
            frame, read_time = camera_instance.read()
            # ensure a new frame is taken from the async camera object. If not, wait until a new frame is read
            if read_time == last_frame_read_time:
                sleep(0.0025)   # add very short sleep to avoid exploding cpu usage due to very fast while iterations
                continue
            else:
                last_frame_read_time = read_time

            detection = self.evaluate_frame(frame)
            last_det_elapsed = time() - self.last_detection_time
            if detection or (last_det_elapsed < self.min_recording_time_after_detection):

                if not video_writer.isOpened():
                    det_time = datetime.now().strftime("%H:%M:%S")
                    msg = f'Intruder detected!! Time:  {self.date}_{det_time}'
                    print(msg)
                    if self.notif_handler is not None:
                        self.notif_handler.append(notif_input=msg, notif_type='message')

                    out_video_path = os.path.join(self.out_detections_dir, f'det_{det_time}.mp4')
                    video_writer.open(filename=out_video_path, fourcc=fourcc, fps=camera_instance.fps, frameSize=(w, h))

                video_writer.write(frame)

            else:
                video_writer.release()
                if self.notif_handler is not None and out_video_path is not None:
                    self.notif_handler.append(notif_input=out_video_path, notif_type='video')
                    out_video_path = None

            self.add_frame_to_buffer(frame)
            if self.notif_handler is not None:
                self.notif_handler.flush(max_retries=0)
