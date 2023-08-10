"""
This module handles the authentication for the gmail API.
"""

import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
TOKEN_FILE = "token.json"

script_dir = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(script_dir, os.getenv("API_CREDENTIALS_FILE"))


def get_gmail_creds(token_file=TOKEN_FILE):
    """
    Get the credentials for the gmail API.
    """
    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_file, "w", encoding="utf-8") as token:
            token.write(creds.to_json())
    return creds


def build_api_service():
    """
    Build the gmail API service.
    """
    creds = get_gmail_creds()
    service = build("gmail", "v1", credentials=creds)
    return service
