import os
import json
import requests
import logging

import cv2
import numpy as np

logging.basicConfig(format='%(asctime)s:%(name):½(level): %(message)s', datefmt='%d-%m-%y %H:%M:%S')


class TelegramBot:

    def __init__(self, bot_credentials):
        """

        :param bot_credentials: dict object containing bot credentials or file path to a credentials json file
        :type bot_credentials: dict or str
        """
        if isinstance(bot_credentials, str):
            with open(bot_credentials, 'r') as fp:
                bot_credentials = json.load(fp)

        self.name = bot_credentials.get('name', 'Bot')
        self.token = bot_credentials['token']
        self.chat_id = bot_credentials['chat_id']
        self.base_url = f'https://api.telegram.org/bot{self.token}'

    def set_chat_id(self, chat_id):
        self.chat_id = chat_id

    def set_token(self, token):
        self.token = token
        self.base_url = f'https://api.telegram.org/bot{self.token}'

    def send_message(self, message):
        url = f'{self.base_url}/sendMessage'
        data = {'chat_id': self.chat_id, 'text': f'[{self.name}] {message}'}

        response = requests.post(url=url, data=data)
        if response.status_code != 200:
            logging.error(f'Send message returned status code = {response.status_code}')
            return False

        return True

    def send_image(self, image_input, enc_ext='.jpg'):

        if isinstance(image_input, bytes):
            input_type = 'bytes'
            image_bytes = image_input

        elif isinstance(image_input, str):
            input_type = 'file'
            if os.path.isfile(image_input):
                image_bytes = open(image_input, 'rb')
            else:
                logging.error(f'Input image file: {image_input} not found')
                return False

        elif isinstance(image_input, np.ndarray):
            input_type = 'array'
            image_bytes = cv2.imencode(enc_ext, img=image_input)[1].tobytes()

        else:
            input_type = type(image_input)
            logging.error(f'Input image type {input_type} is not supported')
            return False

        url = f'{self.base_url}/sendPhoto'
        data = {'chat_id': self.chat_id}
        files = {'photo': image_bytes}
        response = requests.post(url=url, data=data, files=files)
        if response.status_code != 200:
            logging.error(f'Send photo returned status code = {response.status_code}')
            return False

        if input_type == 'file':
            image_bytes.close()

        return True

    def send_video(self, video_input):
        if isinstance(video_input, bytes):
            input_type = 'bytes'
            video_bytes = video_input

        elif isinstance(video_input, str):
            input_type = 'file'
            if os.path.isfile(video_input):
                video_bytes = open(video_input, 'rb')
            else:
                logging.error(f'Input video file: {video_input} not found')
                return False

        else:
            input_type = type(video_input)
            logging.error(f'Input video type {input_type} is not supported')
            return False

        url = f'{self.base_url}/sendVideo'
        data = {'chat_id': self.chat_id}
        files = {'video': video_bytes}
        response = requests.post(url=url, data=data, files=files)
        if response.status_code != 200:
            logging.error(f'Send video returned status code = {response.status_code}')
            return False

        if input_type == 'file':
            video_bytes.close()

        return True

    def send_file(self, file_input):
        if isinstance(file_input, bytes):
            input_type = 'bytes'
            file_bytes = file_input

        elif isinstance(file_input, str):
            input_type = 'file'
            if os.path.isfile(file_input):
                file_bytes = open(file_input, 'rb')

            else:
                logging.error(f'Input file: {file_input} not found')
                return False

        else:
            input_type = type(file_input)
            logging.error(f'Input file type {input_type} is not supported')
            return False

        url = f'{self.base_url}/sendDocument'
        data = {'chat_id': self.chat_id}
        files = {'document': file_bytes}
        response = requests.post(url=url, data=data, files=files)
        if response.status_code != 200:
            logging.error(f'Send file returned status code = {response.status_code}')
            return False

        if input_type == 'file':
            file_bytes.close()

        return True


if __name__ == '__main__':

    cwd = os.path.dirname(os.path.realpath(__file__))
    bot_credentials_file = os.path.join(cwd, 'credentials.json')
    with open(bot_credentials_file, 'r') as fp:
        credentials = json.load(fp)

    bot = TelegramBot(bot_credentials=credentials)
    bot.send_message('Example message')


