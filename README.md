
# quicknotes
I use a simple set of quicknotes to store stuff I get hit with. This tool searches them.

## Notes

[Installation/Documentation](./docs/000-Welcome_to_Quicknotes.md)

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
* Expanded the style to make the page a little more pleasant
* Added unix script for launching/monitoring.

## Revision March 27, 2021
* converted to python 3
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

## Revision April 3, 2021
* set master to the python3 version
* set master to the FastAPI version
* you can still find the older versions in their own branches. 
* allowing mp4 extension, but html is required to embed.

## Revision April 9, 2021
* added support for fortune files
* you need to put a fortune file in the document folder, then you can open with /fortune/{filename} api

## Revision April 11, 2021
* added support for html/htm extensions. Place the file in your document folder. Note that html files are not filtered and are not listed as quicknotes. (yet)
* added support for css and js. Note that css files served by the quickserver _must_ be in subfolder called css off of document folder. (there is a subfolder called js for javascript).
* restructured the docs folder so you can copy it directly as a starting point. Contains example html game, and fortune files.

```
docs
├── 000-Welcome_to_Quicknotes.md
├── 001-Running_Quicknotes_manually.md
├── 002-Running_Quicknotes_docked.md
├── breakout.html
├── css
│   └── breakout.css
├── js
│   └── breakout.js
├── obscene
├── scene
└── templates
    ├── body.template
    ├── root.template
    └── style.template
```
 
## Revision update April 17, 2021
* added /links/{folder_name} api - will read a folder_name with url, desktop, and build a web page of clickable links. 
* added fractal.html (demonstration) - playing with javascript canvas
* added /unjumble={comma deliminated list of jumbled words} api - will unjumble words
* added a requirements.txt to track the libraries that need to be pipped
* added a rumors (Nethack fortune cookie) file. Use the /fortune/rumors to get a fortune.

## Revision update July 4, 2025
* stood up a manual running version on Windows 11
* had to install python 3.x on my windows
* use *set* instead of *export*
* some minor code changes
* see *windows_ver* branch

## Revision update July 5, 2025
* modified the Dockerfile to get the pips going again.
* when you run in a windows environment use full paths, for example:
```
  docker run -d -v c:\Users\steve\python_projects\quicknotes\docs:/docs -p 8001:8001 -e "PORT=8001" -e IPADDRESS="127.0.0.1" -e "QUICKNOTES=/docs/" quicknotes:0.1
```
  
