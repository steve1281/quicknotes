# Quicknotes - Welcome

## Disclaimer

This was created to assist me in learning python. Some of this code is really[^1] old. 

There is no warranty of any kind.

[^1]: This started as a commandline tool I created for searching through text documents. 

## What is a Quicknote?

A quicknote is anologous to the stuff you would write in your notebook.  

Imagine that each notebook has 1000 pages, numbered 000 to 999. 

Every quicknote is numbered, 000 to 999.  The format is:

```
000-Some_Informative_Title.md (or .txt)
```

The content of the quicknote depends on whether you use markdown or text. 

If its a text file, then it wil be rendered exactly as you entered it; I simply wrap your
text in a `<pre>` tag.

If its a markdown (md) file, then it is rendered.



## What can I do with this?

Quicknote server runs a (small) webserver (on port 8000 by default). 

It has the ability to list and search your notes.  The more criteria you provide, the better the 
search result.

```
http://localhost:8000/filter/search1/search2/search3/.../searchN
```

So, instead of flipping through the your notebook, you can limit your searching to pages with 
the pertinant information in it.


## How do I run this?

There are two ways to run quicknotes:

* [Running Quicknotes manually](001-Running_Quicknotes_manually.md)
* [Running Quicknotes docked](002-Running_Quicknotes_docked.md)

## Note about supported filetypes

As mentioned above, txt an md files are supported. The code looks for those extensions. Nothing stops you from renaming a binary file to a txt or md file; this will break the quicknote server.

Graphic files (jpg, jpeg, png, gif) are rendered as binary files.

Support for other media (mp4, wav, etc) is coming, as of April 2, 2021 they are NOT supported.


## Error messages

* Unhandled extension  - Tried to open a file with an unsupported extension. 
* An error has occurred - Server could not find/resolve the file you wanted to open.

## Programmer's notes

This was orginally written in python2.7 - and a limited version of quicknotes still exists.  Now the code has been ported to 3.9 (and tested in 3.8 ok). 

Quicknotes uses an insecure, non-swagger, adhoc, home hacked webserver at its core, and a search engine written by a C programmer learning python 2.7.  

This is not a CMS. 

This is not fit for production.


