from oauth2client.service_account import ServiceAccountCredentials
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import *
import smtplib
import gspread
import os


class GoogleSheet:
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
            current_time = datetime.now().strftime('%d-%m-%y %H:%M')

            # Change shot progress to waiting for review
            self.wks.update_cell(row, 8, 'Needs Comp Review')
            self.wks.update_cell(row, 9, current_time)


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
