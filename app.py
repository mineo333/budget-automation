#!/usr/local/bin/python3
import uvicorn
from fastapi import FastAPI
import utils
import binascii
import requests
from models import Submission, SubmissionResponse, ErrorType
from constants import MAILGUN_API_KEY, DOMAIN, OUTGOING_EMAIL

app = FastAPI()
"""
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
gauth = GoogleAuth(
    settings={
        "client_config_backend": "file",
        "client_config_file": "assets/client_secrets.json",
        "save_credentials": False,
        "oauth_scope": ["https://www.googleapis.com/auth/drive"],
    }
)
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)
"""


@app.post("/submit")
def submit_form(data: Submission) -> SubmissionResponse:
    """Submits our purchase reciept data and returns a googledrive
    link to compiled and uploaded reciept.

    Args:
        data (Submission): Submission details, will be used to populate
        our LaTeX template.

    Returns:

    """

    path = utils.compile_receipt(data)
    utils.send_email_via_mailgun(
        api_key=MAILGUN_API_KEY,
        domain=DOMAIN,
        recipient=OUTGOING_EMAIL,
        pdf_file_path=path,
        vendor_name=data.vendor_name,
        first_name=data.first_name,
        last_name=data.last_name,
        purchase_date=data.purchase_date,
    )

    return SubmissionResponse(gdrive_link=path)


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)
