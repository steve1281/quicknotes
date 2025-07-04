[BACK](000-Welcome_to_Quicknotes.md)

# Running Quicknotes Manually

## Note about windows

I didn't originally support Windows. Lately I find myself coding a lot in windows, and thought why not see what is required to make quicknotes work in windows.
 

Steps:

```
cd
git clone --branch master --single-branch https://github.com/steve1281/quicknotes
cd quicknotes
pip install markdown fastapi uvicorn aiofiles bs3
set QUICKDIR=.
set QUICKNOTES=c:\Users\steve\python_projects\docs
set PORT=8000
set PADDRESS=127.0.0.1
python3 fapi.py
```

## About the Environment variables

* QUICKNOTES is where your quick notes are. 
* PORT is the port you want to use for your webserver.
* IPADDRESS is the ip address you want the webserver to advertise on. Leave as 127.0.0.1 for local use. 

## code changes

fapi.py:

```
-    uvicorn.run(app='fapi:app', host='0.0.0.0', port=int(_port), reload=True, debug=False)
+    uvicorn.run(app='fapi:app', host='0.0.0.0', port=int(_port), reload=True)

```

squick.py:

```
-        with open(document_folder + filename, "rU") as f:
+        with open(document_folder + filename, "r") as f:
```


