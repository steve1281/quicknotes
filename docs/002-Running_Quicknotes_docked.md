[BACK](000-Welcome_to_Quicknotes.md)

# Running Quicknotes Docked
[TOC]

This is probably the easiest way to get quickserver running, if you are docker saavy.  If you have never used docker, I strongly recommend it.  This note assumes you have docker up and running, and you know the basics.

## Dockerfile

The repo contains an example Dockerfile that you should adjust to fit your requirments/environment:

```
# Quicknotes - simpleserver launcher
FROM ubuntu

RUN apt-get update
RUN apt-get -y install python3
RUN apt-get -y install git
RUN apt-get -y install python3-pip
RUN python3 -m pip install mdtex2html
RUN python3 -m pip install markdown
RUN git clone --branch python391_version --single-branch https://github.com/steve1281/quicknotes
ENV QUICKDIR=/quicknotes
ENV QUICKNOTES=/docs/
ARG PORT=8000
ARG IPADDRESS=127.0.0.1
CMD ["python3","/quicknotes/simpleserver.py"]
```


## Building

The first build usually takes the longest. My preference, when developing, is to use `--no-cache` :

```
docker build -t quicknotes:0.1 . --no-cache 
```


## Running

Currently, the port that you map to should match the port your run at.  (This is due to simple nature of the quicknote program). You can change the ip address to the hosts if you want to; this will expose it to your whole network. (so security risk).

You should map a volume to wherever you want to keep your documents.

```
docker run -d -v ~/docs_old/:/docs -p 8001:8001 -e "PORT=8001" -e IPADDRESS="127.0.0.1" quicknotes:0.1
```

## Logging 

There is a quickserver.log generated, but in the case of docked you would need to enter the console to see it.
(This is simple to do using Docker Desktop)

