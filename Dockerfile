# Quicknotes - simpleserver launcher
FROM ubuntu
MAINTAINER steve1281@hotmail.com

RUN apt-get update
RUN apt-get -y install python3
RUN apt-get -y install git
RUN apt-get -y install python3-pip
RUN apt-get -y install python3.12-venv
# RUN python3 -m venv my-venv
# RUN python3 -m pip install python3-mdtex2html
RUN python3 -m pip install --break-system-packages mdtex2html
RUN python3 -m pip install --break-system-packages markdown
RUN python3 -m pip install --break-system-packages fastapi
RUN python3 -m pip install --break-system-packages uvicorn
RUN python3 -m pip install --break-system-packages aiofiles
RUN python3 -m pip install --break-system-packages bs4
RUN git clone --branch windows_ver --single-branch https://github.com/steve1281/quicknotes
ENV QUICKDIR=/quicknotes
ENV QUICKNOTES=/docs/
ARG PORT=8000
ARG IPADDRESS=127.0.0.1
CMD ["python3","/quicknotes/fapi.py"]
