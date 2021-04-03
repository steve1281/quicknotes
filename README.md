updates are not coming.

# quicknotes
I use a simple set of quicknotes to store stuff I get hit with. This tool searches them.

## Notes
* you should export a QUICKNOTES variable saying where your quicknotes are:
* 'export QUICKNOTES="/home/steve/Documents/quicknotes/"'
* (notes the trailing slash.  I may actually add a check for that)
* to run:
* python simpleserver.py
* then you just http://127.0.0.1:8000/  

## Revision March 11, 2018
* Switched to markdown conversion. This means the previous pre tags are removed.
* I may add a flag to switch between the two, or maybe a file extension check? need to think about it.
* This does mean you will need to pip markdown now.
* Oh, I am now injecting a style into the head tag.

## Revision March 12, 2018
* set the environment variable `$QUICKNOTES` to set the folder where the quicknotes are stored.
* added extensions to the markdown, removed css hack to work around it.

## Revision March 29, 2018
* Only .md files get md rendered now.
* Expanded the style to make the page a little more pleasent

* there is some libs to pip
```
sudo pip install py-gfm
sudo pip install markdown
```

* Script you can use.
```
./scripts/qserv
```

## Revision March 27, 2021
* converted (finally) to python 3
* this has been a long time coming - back in 2018 I was just learning python, and it shows! 
* I ran the 2to3 conversion, and changed markdown libraries. 
* This needs a LOT of love.

## Revision March 28, 2021
* Got tired of running this in a VirtualBox VM, so stood up a docker.
* Look promising, but will need some more work.

## Revision April 2, 2021
* added docs
* removed old (broken) CLI functionality
* deleted unused methods
* modernized file handling (with)
* first pass refactor (lots of love needed)
