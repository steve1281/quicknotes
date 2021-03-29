# Quicknotes - simpleserver launcher
FROM ubuntu
MAINTAINER steve1281@hotmail.com

RUN apt-get update
RUN apt-get -y install python3
RUN apt-get -y install git
RUN apt-get -y install python3-pip
RUN python3 -m pip install mdtex2html
RUN python3 -m pip install markdown
RUN git clone --branch python391_version --single-branch https://github.com/steve1281/quicknotes
ENV QUICKDIR=/quicknotes
ENV QUICKNOTES=/docs/
CMD ["python3","/quicknotes/simpleserver.py"]
