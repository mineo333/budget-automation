#!/usr/local/bin/python3

from flask import Flask, Response, request
from compile_pdf import *


app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit_form():
    data = request.get_json()

    compile_receipt(data)
    return 'receipt.txt'
    
if __name__ == '__main__':
    app.run(host='0.0.0.0')