[BACK](000-Welcome_to_Quicknotes.md)

# Running Quicknotes Manually
[TOC]

## Note about windows

I don't support Windows. I don't see any reason why Quicknotes won't run on it; I just can't be bothered.
If you really want Windows, I suggest setting up on WSL2, which I have used and works decently, once you get all the Windows powershell sillyness out of the way.

## Run on a server, standalone, on an Ubuntu system

This assumes you have a dedicated server (VM) for running this on. For example, I have run this on Virtualbox and Oracle Cloud free tier using very small foot prints.

You can of course do this on non-ubuntu systems - change the apt-get to yum as appropiate.

```
cd
sudo apt-get update
sudo apt-get install python3 git 
git clone --branch master --single-branch https://github.com/steve1281/quicknotes
cd quicknotes
pip install -y markdown fastapi uvicorn aiofiles
export QUICKDIR=.
export QUICKNOTES=~/docs/
export PORT=8000
export IPADDRESS=127.0.0.1
python3 fapi.py
```

You can change the environment variables to adjust to your preferences.

## Running locally

If you decide to run this locally, I recommend installing pyenv and using virtualenv.
So you might (as an example) do it this way:

```
cd 
git clone --branch master --single-branch https://github.com/steve1281/quicknotes
cd projects/quicknotes
pyenv version 3.8.6
python3 -m venv virtualenv
. virtualenv/bin/activate
pip install markdown fastapi uvicorn aiofiles beautifulsoup4 lxml
export QUICKNOTES=./docs/
export PORT=8000
export IPADDRESS=127.0.0.1
python3 fapi.py
```

## About the Environment variables

* QUICKNOTES is where your quick notes are. 
* PORT is the port you want to use for your webserver.
* IPADDRESS is the ip address you want the webserver to advertise on. Leave as 127.0.0.1 for local use. 
