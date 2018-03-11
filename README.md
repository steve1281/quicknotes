updates are not coming.

# quicknotes
I use a simple set of quicknotes to store stuff I get hit with. This tool searches them.

## Notes
* you should export a QUICKNOTES variable saying where your quicknotes are:
* 'export QUICKNOTES="/home/steve/Documents/quicknotes/"'
* (notes the trailing slash.  I may actually add a check for that)
* to run:
* python simpleserver.py
* then you just http://127.0.0.1/  

## Revision March 11, 2018
* Switched to markdown conversion. This means the previous pre tags are removed.
* I may add a flag to switch between the two, or maybe a file extension check? need to think about it.
* This does mean you will need to pip markdown now.
* Oh, I am now injecting a style into the head tag.
