from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from oauth2client.service_account import ServiceAccountCredentials
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import *
import smtplib
import gspread
import time
import os
from base_functions import *
import glob
try:
    import cv2
except ImportError:
    pass


class GoogleDrive(object):
    SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'

    def __init__(self):
        """
        Setup for connecting to your google drive
        """
        store = file.Storage('tokens.json')
        creds = store.get()

        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', self.SCOPES)
            creds = tools.run_flow(flow, store)
        self.service = build('drive', 'v3', http=creds.authorize(Http()))

    def find_file(self, file_name):
        """
        Searching the google drive for the file by exact name, returning name and id
        """
        name = 'name = "{}"'.format(file_name)
        results = self.service.files().list(q=name, fields="files(id, name)").execute()
        return results.get('files', [])[-1]


class GoogleSheet(object):
    def __init__(self):
        # Google Drive connection and setup
        scope = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(os.path.dirname(os.path.realpath(__file__)) + '/google_service.json', scope)
        google_cloud = gspread.authorize(credentials)
        self.wks = google_cloud.open('Rise n Shine Tracker').sheet1

    def set_tracker_status(self, shot_code=None):
        if shot_code:
            # Find shot code and row
            row = self.wks.find(shot_code).row

            # Assign current time
            current_time = datetime.now().strftime('%d-%m-%y')

            # Change shot progress to waiting for review
            self.wks.update_cell(row, 8, 'Needs Comp Review')
            self.wks.update_cell(row, 9, current_time)

    def set_thumbnail(self, shot_code, google_file_id):
        row = self.wks.find(shot_code).row
        value = r'=Image("http://drive.google.com/uc?export=view&id={}", 2)'.format(google_file_id)
        self.wks.update_cell(row, 3, value)


def create_jpg_from_mov(mov_file, jpg_file):
    """
    Create jpg from mov file
    """
    video_capture = cv2.VideoCapture(mov_file)
    complete, image = video_capture.read()
    cv2.imwrite(jpg_file, image)
    return complete


if __name__ == '__main__':
