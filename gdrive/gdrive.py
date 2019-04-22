import pathlib
import io
import os
import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload

class GDrive:

    def __init__(self, host="localhost", port=8898):
        # If modifying these scopes, delete the file token.json.
        self.SCOPES = 'https://www.googleapis.com/auth/drive'
        self.token_path = 'gdrive/token.pickle'
        self.credentials_path = 'gdrive/credentials.json'
        self.host = host
        self.port = port
        self.drive_service = self.establish_connection_gdrive()
        
    def establish_connection_gdrive(self):

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time.
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, self.SCOPES)
                creds = flow.run_local_server(host=self.host, port=self.port)
            # Save the credentials for the next run
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)

        drive_service = build('drive', 'v3', credentials=creds)

        return drive_service

    def list_files_in_folder(self, folder_id, parent_folder=""):

        page_token = None
        while True:
            response = self.drive_service.files().list(pageSize=1000, q= f"'{folder_id}' in parents",
                                                fields="nextPageToken, files(id, name, mimeType, parents)").execute()
            for file in response.get('files', []):
                print(f'''File name:  {file.get('name')}\nParent: {parent_folder}\nID: {file.get('id')}\n''')
                if file.get('mimeType') == 'application/vnd.google-apps.folder':
                    self.list_files_in_folder(self.drive_service, file.get('id'), parent_folder=file.get('name'))
                    print('\n') 
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

    def download_file(self, file_id, file_name, save_dir='image_data/'):

        pathlib.Path(save_dir).mkdir(parents=True, exist_ok=True)

        request = self.drive_service.files().get_media(fileId=file_id)

        fh = io.FileIO(save_dir + file_name, mode='wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Downloaded {int(status.progress() * 100)}%.")

    def get_file_size(self, file_id):

        f = self.drive_service.files().get(fileId=file_id, fields='size').execute()

        return {"file_id": file_id, "size": int(f.get('size'))}