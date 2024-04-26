#!/usr/local/bin/python3
import subprocess
import tempfile
import os
import json
import sys
from jinja2 import Environment, FileSystemLoader

def compile_receipt(json_string):
    try:
        # Create a new temporary directory
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create a new temporary file
            temp_tex_file = os.path.join(tmp_dir, "receipt.tex")

            environment = Environment(loader=FileSystemLoader("templates/"))
            template = environment.get_template("purchase_receipt.txt")

            content = template.render(json.loads(json_string))

            with open(temp_tex_file, mode="w", encoding="utf-8") as message:
                message.write(content)

            # Compile the modified LaTeX document to PDF using pdflatex
            subprocess.run(['pdflatex', temp_tex_file])
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while compiling LaTeX document: {e}")
    os.remove("receipt.aux")
    os.remove("receipt.log")
