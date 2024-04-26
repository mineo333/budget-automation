FROM python:3.11

RUN /usr/sbin/useradd -u 1000 user

RUN mkdir -p /home/user/templates

#COPY purchase receipt
COPY purchase_receipt.txt /home/user/templates/
COPY compile_pdf.py /home/user/
COPY ritseclogo.png /home/user
COPY app.py /home/user
RUN chown -R user:user /home/user

RUN apt-get update -y
RUN apt-get install texlive-latex-base texlive-latex-extra -y


USER 1000

#install dependencies
RUN pip3 install pdflatex
RUN pip3 install Jinja2
RUN pip3 install flask

#chmod all files
RUN chmod 755 /home/user/compile_pdf.py
RUN chmod 755 /home/user/templates/purchase_receipt.txt
RUN chmod 755 /home/user/app.py

WORKDIR /home/user

CMD /home/user/app.py
