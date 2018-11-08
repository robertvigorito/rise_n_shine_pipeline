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


def send_review(artist_name=None, shot_code=None, content=None, review_version=None):
    # Sign-in information
    email_user = 'auto.message.vfx@gmail.com'
    email_password = 'risenshine1212'
    email_recipient = 'robertvigorito@gmail.com'

    # Create message content
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_recipient
    msg['Subject'] = 'Shot {} Review'.format(shot_code)

    content = content.replace('\n', '<br/>')
    # Body information
    html = '<html><head><font color="#372868"> <h1>Shot Submitted for Review</h1> </font></head>' \
           '<body><font size="3" > Artist: {}<br/> Version: {}<br/>Notes:<br/>{}<br/><br/>' \
           '<a href = "https://docs.google.com/spreadsheets/d/1-LyNRzh_wcDA4gLGYhvH-8ZoMjW8PzPFkadrXfK5-bE/edit?usp' \
           '=drive_web&ouid=103267484209890756123">Open Tracker</a></font>' \
           '</html>'.format(artist_name, review_version, content)

    msg.attach(MIMEText(html, 'html'))
    msg = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    # Next, log in to the server
    server.login(email_user, email_password)

    # Send the mail
    server.sendmail(email_user, email_recipient, msg)
    server.quit()


def create_jpg_from_mov(mov_file, jpg_file):
    """
    Create jpg from mov file
    """
    video_capture = cv2.VideoCapture(mov_file)
    complete, image = video_capture.read()
    cv2.imwrite(jpg_file, image)
    return complete


if __name__ == '__main__':
    """
    Updating thumbnails on rise n shine tracker
    """
    google_drive_dir = os.path.join(json_read_write(), 'Comp/')
    gs = GoogleSheet()
    gd = GoogleDrive()

    for shot_code in os.listdir(google_drive_dir):

        comp_mov_dir = os.path.join(google_drive_dir, shot_code, 'Renders/Review/Comp/')

        thumbnail = os.path.join(google_drive_dir, shot_code, 'Source Files/Thumbnail')

        comp_mov_file = glob.glob(comp_mov_dir + '*.mov')
        if comp_mov_file:
            comp_mov_file = comp_mov_file[-1]

            jpeg_name = comp_mov_file.rsplit('\\', 1)[-1].replace('.mov', '.jpeg')
            jpeg_file_path = os.path.join(thumbnail, jpeg_name)
            try:
                os.makedirs(thumbnail)
            except WindowsError:
                pass
            create_jpg_from_mov(comp_mov_file, jpeg_file_path)

        if os.path.exists(thumbnail):
            thumbnail_file = glob.glob(thumbnail + '/*.jpeg')[-1]
            jpeg_file_name = thumbnail_file.rsplit('\\', 1)[-1]
            time.sleep(5)
            try:
                file_id = gd.find_file(jpeg_file_name).get('id', '')
                gs.set_thumbnail(shot_code, file_id)
            except IndexError:
                print 'error' + comp_mov_file
