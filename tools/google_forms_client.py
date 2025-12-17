import os
from typing import List, Dict, Any
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/forms.body",
    "https://www.googleapis.com/auth/forms.responses.readonly",
    "https://www.googleapis.com/auth/drive",
]
CLIENT_SECRETS_FILE = "credentials.json"
TOKEN_FILE = "token.json"


def _get_creds() -> Credentials:
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES
            )
            creds = flow.run_local_server(
                port=0, access_type="offline", prompt="consent"
            )
        with open(TOKEN_FILE, "w") as token_file:
            token_file.write(creds.to_json())
    return creds


class GoogleFormsClient:
    def __init__(self):
        creds = _get_creds()
        self.creds = creds
        self.service = build("forms", "v1", credentials=creds)

    def list_forms(self) -> List[Dict[str, Any]]:
        """
        Возвращает список файлов-форм (id + name + mimeType) на Google Drive,
        у которых mimeType = 'application/vnd.google-apps.form'.
        """
        drive = build("drive", "v3", credentials=self.creds)
        forms = []
        page_token = None
        query = "mimeType = 'application/vnd.google-apps.form' and trashed = false"
        while True:
            response = (
                drive.files()
                .list(
                    q=query,
                    spaces="drive",
                    fields="nextPageToken, files(id, name, mimeType)",
                    pageToken=page_token,
                )
                .execute()
            )
            items = response.get("files", [])
            forms.extend(items)
            page_token = response.get("nextPageToken")
            if not page_token:
                break
        return forms

    def create_form(self, title: str, description: str = "") -> Dict[str, Any]:
        body = {"info": {"title": title, "description": description}}
        return self.service.forms().create(body=body).execute()

    def get_form(self, form_id: str) -> Dict[str, Any]:
        return self.service.forms().get(formId=form_id).execute()

    def close_form_for_responses(self, form_id: str) -> dict:
        body = {
            "publishSettings": {
                "publishState": {"isPublished": True, "isAcceptingResponses": False}
            }
        }
        return (
            self.service.forms().setPublishSettings(formId=form_id, body=body).execute()
        )

    def batch_update(
        self,
        form_id: str,
        requests: List[Dict[str, Any]],
        include_form_in_response: bool = True,
    ) -> Dict[str, Any]:
        body = {"requests": requests, "includeFormInResponse": include_form_in_response}
        return self.service.forms().batchUpdate(formId=form_id, body=body).execute()


client = GoogleFormsClient()
