
# quicknotes
I use a simple set of quicknotes to store stuff I get hit with. This tool searches them.

## Notes

[Installation](./docs/000-Welcome_to_Quicknotes.md)

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
* set master to the FastAPI verison
* you can still find the older versions in their own branches. 
* allowing mp4 extension, but html is required to embed.
