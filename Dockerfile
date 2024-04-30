FROM python:3.11

RUN /usr/sbin/useradd -u 1000 user

RUN mkdir -p /home/user/templates
RUN mkdir -p /home/user/receipts
#COPY purchase receipt
COPY assets/purchase_receipt.txt /home/user/assets/
COPY assets/ritseclogo.png /home/user/assets/
COPY requirements.txt /home/user

COPY utils.py /home/user/
COPY models.py /home/user/
COPY constants.py /home/user/
COPY app.py /home/user
RUN chown -R user:user /home/user

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

#chmod all files
RUN chmod 755 /home/user/app.py

WORKDIR /home/user

CMD /home/user/app.py
