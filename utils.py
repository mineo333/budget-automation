#!/usr/local/bin/python3
import subprocess
import tempfile
import os

import base64
from jinja2 import Environment, FileSystemLoader
from models import Submission
import uuid
from constants import RECEIPTS_DIR
from pdflatex import PDFLaTeX
import requests

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

def send_email_via_mailgun(
    api_key: str,
    domain: str,
    recipient: str,
    pdf_file_path: str,
    vendor_name: str,
    first_name: str,
    last_name: str,
    purchase_date: str,
):
    url = f"https://api.mailgun.net/v3/{domain}/messages"
    with open(pdf_file_path, "rb") as pdf_file:
        files = [("attachment", ("filename.pdf", pdf_file))]
        data = {
            "from": f"Ritsec <ritsec@{domain}>",
            "to": recipient,
            "subject": f"Purchase Receipt for {vendor_name}",
            "text": f"There has been a new purchase. The purchase was for {vendor_name} and was purchased by {first_name} {last_name}. It was purchased on {purchase_date}. \n\nThe receipt can be found below.",
        }

        # Send the request
        response = requests.post(
            url, auth=("api", api_key), files=files, data=data, timeout=45
        )

        # Check the response
        if response.status_code == 200:
            print("Email sent successfully!")
        else:
            print(f"Failed to send email: {response.status_code} - {response.text}")


def compile_receipt(receipt_data: Submission) -> str:
    """Compile a LaTeX document to PDF using pdflatex.

    Args:
        receipt_data (Submission): Submission details, will be used to populate
        our LaTeX template.

    Returns:
        str: relative path to the populated pdf.
    """

    with tempfile.TemporaryDirectory() as tmp_dir:
        temp_tex_file = os.path.join(tmp_dir, "receipt.tex")

        environment = Environment(loader=FileSystemLoader("assets/"))
        template = environment.get_template("purchase_receipt.txt")
        image_path = os.path.join(tmp_dir, uuid.uuid4().hex + ".png")
        
        gauth = GoogleAuth(settings= {
            "client_config_backend": "service",
            "service_config": {
                "client_json_file_path": "secrets/service_account.json",
            }
        })
        
        gauth.ServiceAuth()
        drive = GoogleDrive(gauth)
        image_file = drive.CreateFile({'id': receipt_data.image_id})
        
        image_file.GetContentFile(image_path)

        content = template.render(image_path=image_path, **receipt_data.model_dump())

        with open(temp_tex_file, mode="w", encoding="utf-8") as message:
            message.write(content)
        print(temp_tex_file)
        # Compile the modified LaTeX document to PDF using pdflatex
        # subprocess.run(["pdflatex", temp_tex_file])
        receipts_dir = os.path.join(RECEIPTS_DIR)

        # subprocess.run(["pdflatex", "-output-directory", reciepts_dir, temp_tex_file])
        """
        pdfl = PDFLaTeX.from_texfile(temp_tex_file)
        filename = uuid.uuid4().hex + ".pdf"
        pdfl.set_pdf_filename(filename)
        pdfl.set_output_directory(reciepts_dir)

        pdf, _, _ = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=False)
        """
        output_file = uuid.uuid4().hex
        subprocess.run(
            [
                "pdflatex",
                "-output-directory",
                receipts_dir,
                "-jobname",
                output_file,
                temp_tex_file,
            ]
        )
    #    os.remove(f"receipts/{output_file}.log")
    #    os.remove(f"receipts/{output_file}.aux")
        return os.path.join(receipts_dir, output_file + ".pdf")
