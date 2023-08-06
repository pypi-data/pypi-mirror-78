from time import sleep

import cv2
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import uvicorn

from guardcam.detection import Camera


def frame_to_content(frame, ext='png'):
    frame_bytes = cv2.imencode(f'.{ext}', frame)[1].tobytes()
    content_str = f'--frame\r\nContent-Type:image/{ext}\r\n\r\n'
    content = content_str.encode() + frame_bytes + b"\r\n"
    return content


class VideoStreamingServer:

    def __init__(self, host='0.0.0.0', port=7777):

        self.app = FastAPI()
        self.host = host
        self.port = port

    @staticmethod
    async def _cvcam_stream_content_generator():

        cam = cv2.VideoCapture(0)
        while True:
            ret, frame = cam.read()
            content = frame_to_content(frame, ext='jpg')
            yield content

    @staticmethod
    async def _camera_stream_content_generator(camera_instance):

        spf = 1 / camera_instance.fps
        while True:
            content = frame_to_content(camera_instance.frame, ext='jpg')
            yield content
            sleep(spf)

    def start(self, camera_instance=None):

        if camera_instance is not None:
            assert isinstance(camera_instance, Camera)
            frame_stream_generator = self._camera_stream_content_generator(camera_instance)
        else:
            frame_stream_generator = self._cvcam_stream_content_generator()

        @self.app.get('/')
        async def stream():
            return StreamingResponse(frame_stream_generator, media_type="multipart/x-mixed-replace; boundary=frame")

        print(f'\n\nUvicorn server running on http://{self.host}:{self.port}\n\n')
        uvicorn.run(app=self.app, host=self.host, port=self.port)


if __name__ == '__main__':

    vs = VideoStreamingServer()
    vs.start()

