import time
import os
import json
import requests # pip install requests
import pandas as pd # pip install pandas

__version__ = 'v1.1'
__author__ = 'Kaushika'

class AssemblyAI:
    BASE_URL = 'https://api.assemblyai.com/v2/'
    
    def __init__(self, api_key):
        self.api_key = api_key

    @property
    def headers(self):
        return {'authorization': self.api_key}

    def upload_audio_by_url(self, url_link, remove_filler_word=True, format_text=True, **kwarg):
        request_body = {
            'audio_url': url_link,
            'disfluencies': remove_filler_word,
            'format_text': format_text
        }

        for key, val in kwarg.items():
            request_body[key] = val

        response = requests.post(self.BASE_URL + 'transcript', headers=self.headers, json=request_body)
        return response

    def upload_audio_by_file(self, audio_file_path, chunk_size=5241880, remove_filler_word=True, format_text=True, **kwarg):
        if not os.path.exists(audio_file_path) or not os.path.isfile(audio_file_path):
            print('File is not found')
            return
        
        def read_file(file_path, chunk_size=chunk_size):
            with open(file_path, mode='rb') as _file:
                while True:
                    data = _file.read(chunk_size)
                    if not data:
                        break
                    yield data
        
        audio_data = read_file(audio_file_path)
        headers = self.headers
        headers['content-type'] = 'application/json'
        upload_response = requests.post(self.BASE_URL + 'upload', headers=headers, data=audio_data)
        
        response = self.upload_audio_by_url(upload_response.json()['upload_url'], remove_filler_word=remove_filler_word, format_text=format_text, **kwarg)
        return response

    def retrieve_transcript(self, transcript_id):
        response = requests.get(self.BASE_URL + 'transcript/' + transcript_id, headers=self.headers)
        return response.json()