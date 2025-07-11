# Quicknotes - simpleserver launcher
FROM ubuntu
MAINTAINER steve1281@hotmail.com

RUN apt-get update
RUN apt-get -y install python3
RUN apt-get -y install git
RUN apt-get -y install python3-pip
RUN python3 -m pip install mdtex2html
RUN python3 -m pip install markdown
RUN python3 -m pip install fastapi
RUN python3 -m pip install uvicorn
RUN python3 -m pip install aiofiles
RUN git clone --branch master --single-branch https://github.com/steve1281/quicknotes
ENV QUICKDIR=/quicknotes
ENV QUICKNOTES=/docs/
ARG PORT=8000
ARG IPADDRESS=127.0.0.1
CMD ["python3","/quicknotes/fapi.py"]
