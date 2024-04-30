FROM python:3.11

RUN /usr/sbin/useradd -u 1000 user

RUN mkdir -p /home/user/templates
RUN mkdir -p /home/user/receipts
RUN mkdir -p /home/user/constants
RUN mkdir -p /home/user/secrets
#COPY purchase receipt
COPY assets/purchase_receipt.txt /home/user/assets/
COPY assets/ritseclogo.png /home/user/assets/

COPY requirements.txt /home/user/

COPY utils.py /home/user/
COPY models.py /home/user/


#######

#both of these need to be mounted as secrets in the google drive

#COPY constants.py /home/user/constants/__init__.py
#COPY assets/service_account.json /home/user/secrets/

#######

COPY app.py /home/user/
RUN chown -R user:user /home/user

RUN ls -la /home/user/

RUN apt-get update -y
RUN apt-get install texlive-latex-base texlive-latex-extra -y

USER 1000

#install dependencies
RUN pip3 install Jinja2
RUN pip3 install fastapi
RUN pip3 install pdflatex
RUN pip3 install pydantic
RUN pip3 install Requests
RUN pip3 install uvicorn
RUN pip3 install pydrive2

#chmod all files
RUN chmod 755 /home/user/app.py

WORKDIR /home/user

CMD python3 /home/user/app.py   
