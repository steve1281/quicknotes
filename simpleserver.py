#!/usr/bin/env python

import os
import re
# https://github.com/polarwinkel/mdtex2html
# import mdtex2html
import markdown
import http.server
from http.server import SimpleHTTPRequestHandler
from squick import dumpQuickNote, list_files, quicknotelist, filterout

import logging

initfolder = os.getenv('QUICKNOTES', '/docs/')
if not initfolder.endswith('/'):
    initfolder = initfolder + "/"

_port = os.getenv('PORT', '8000')
_ip = os.getenv('IPADDRESS', '127.0.0.1')

_debug_level = os.getenv("DEBUG_LEVEL", "ERROR")
if _debug_level == "ERROR":
    logging.basicConfig(level=logging.ERROR)
elif _debug_level == "WARNING":
    logging.basicConfig(level=logging.WARNING)
elif _debug_level == "INFO":
    logging.basicConfig(level=logging.INFO)
elif _debug_level == "DEBUG":
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.DEBUG)
    logging.ERROR(f"{_debug_level} unknown.")


class MyHttpRequestHandler(SimpleHTTPRequestHandler):
    global _port
    global _ip
    global initfolder

    # https://python-markdown.github.io/extensions/
    md_extensions = [
        'extra',
        'abbr',
        'attr_list',
        'def_list',
        'fenced_code',
        'footnotes',
        'md_in_html',
        'tables',
        'admonition',
        'codehilite',
        'legacy_attrs',
        'legacy_em',
        'meta',
        'nl2br',
        'sane_lists',
        'smarty',
        'toc',
        'wikilinks'
    ]

    TEMPLATE_RESPONSE = """
    <html>
        <head>
            <link href="data:image/x-icon;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQEAYAAABPYyMiAAAABmJLR0T///////8JWPfcAAAACXBIWXMAAABIAAAASABGyWs+AAAAF0lEQVRIx2NgGAWjYBSMglEwCkbBSAcACBAAAeaR9cIAAAAASUVORK5CYII=" rel="icon" type="image/x-icon" />
            <title>Quicknotes</title>
            [STYLE]
        </head>
        <body>
            [BODY]
        </body>
    </html>
    """

    MENU_HEADER = """

    <div>
        <h2>QuickNotes: Search and Display (HTTP interface)</h2>
        
        <h3>Source folder is:  [INITFOLDER]</h3>
        <br/>
        <a href="http://[IPADDRESS]:[PORT]/list"> http://[IPADDRESS]:[PORT]/list  - list the files </a><br/>
        <a href="http://[IPADDRESS]:[PORT]/filter"> http://[IPADDRESS]:[PORT]/filter/filter1/filter2/...</a> <br/>
    </div>

    """

    def do_GET(self):
        logging.debug(f"do_GET called: {self.requestline}")
        self.response_code = 200

        response_data = self.TEMPLATE_RESPONSE
        body,bflag = self.get_body(self.requestline)
        logging.debug(f"Writing response for {self.requestline}")
        if body == "":
            logging.debug(f"Body is empty, sending a 403, binary flag is ({bflag}) ")
            self.send_response(403)
            return
        if bflag:
            logging.debug(f"binary flag set ({bflag}) ")
            self.send_response(self.response_code)
            self.send_header("Content-length", len(body))
            self.end_headers()
            self.wfile.write(body)
        else:
            logging.debug(f"binary flag not set ({bflag})")
            response_string = response_data.replace("[BODY]", body)
            hstyle = self.get_style(self.requestline)
            response_string = response_string.replace("[STYLE]", hstyle)
            self.send_response(self.response_code)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(response_string ))
            self.end_headers()
            self.wfile.write(response_string.encode())

    def get_style(self, request):
        # return "<style>code {white-space: pre ; display: block; unicode-bidi: embed} ul#quicklist{list-style-type: none;} a.quickanchor{text-decoration: none;}</style>"
        return """<style>
                 body{background-color:#FDF6E3;}
                 ul#quicklist{list-style-type: none;} 
                 a.quickanchor{text-decoration: none;} 
                 div#wrapper{
                             padding:5px;
                             margin:auto; width:80%;
                             background-color:#eee8d5;
                             }
                </style>"""

    def get_body(self, request):
        logging.debug(f"get_body called: {request}")
        # Initialize the Markdown parser:

        self.MENU_HEADER = self.MENU_HEADER.replace("[INITFOLDER]", initfolder)
        self.MENU_HEADER = self.MENU_HEADER.replace("[PORT]", _port)
        self.MENU_HEADER = self.MENU_HEADER.replace("[IPADDRESS]", _ip)

        files = list_files(initfolder)
        quicknotes = sorted(quicknotelist(files),key = lambda x: int(re.split("-| ",x)[0]))
        argument_string = len(request) >= 14 and request[5:-9] or None
        bflag = None

        if argument_string is None:
            return self.MENU_HEADER, bflag
        elif argument_string == 'blah/blah':
            return "Sure bub, here is some blah blah for you.", bflag
        elif argument_string == "?":
            return self.MENU_HEADER, bflag
        elif argument_string == "list":
            add_list_converter = ('<li><a class="quickanchor" href="'+w+'">'+w+'</a></li>' for w in quicknotes)
            return "<ul id='quicklist'>"+"\n".join(add_list_converter)+"</ul>", bflag
        elif (len(argument_string) >= 6 and argument_string[:6]=='filter' or None):
            filters = argument_string.split("/")
            filters.reverse()
            filters.pop()
            filtered_list = quicknotes
            for filter in filters:
                filtered_list = filterout(initfolder, filtered_list, filter)
            add_list_converter = ('<li><a class="quickanchor" href="http://'+_ip+':'+_port+'/'+w+'">'+w+'</a></li>' for w in filtered_list)
            return "<ul>"+"\n".join(add_list_converter)+"</ul>", bflag
        elif argument_string == "favicon.ico":
            return "", bflag
        else:
            s = "<div id='wrapper'>An error has occurred</div>"
            try:
                filename = self.strip(argument_string)
                _, ext = os.path.splitext(filename)
                logging.debug(f"filename is {initfolder+filename} extension is {ext}")
                if ext.lower() in ['.jpg', '.gif','.png','jpeg']:
                    logging.debug(f"Reading and returning binary data")
                    bflag = True
                    with open(initfolder+filename, "rb") as f:
                        return f.read(), bflag
                elif ext in ['.md', '.MD']:
                    logging.debug(f"Reading and converting markdown data")
                    s,_ = dumpQuickNote(initfolder, self.strip(argument_string))
                    s = markdown.markdown(s, extensions=self.md_extensions)
                    s = "<div id='wrapper'>" + s + "</div>"
                elif ext in ['.txt', '.TXT']:
                    logging.debug(f"Reading and returning plain text")
                    s,_ = dumpQuickNote(initfolder, self.strip(argument_string))
                    s = "<div id='wrapper'><pre>" + s + "</pre></div>"
                else:
                    logging.debug(f"Unhandled extension {ext}")
                    s = f"<div id='wrapper'>Unhandled extension {ext}</div>"
            except Exception as e:
                logging.error(e)
                self.response_code = 404
            return s, bflag

    def strip(self,s):
        return s.replace("%20", " ")


HandlerClass = MyHttpRequestHandler
ServerClass = http.server.HTTPServer
Protocol = "HTTP/1.0"

port = int(_port)
server_address = ('0.0.0.0', port)

HandlerClass.protocol_version = Protocol
httpd = ServerClass(server_address, HandlerClass)
sa = httpd.socket.getsockname()
logging.info(("Serving HTTP on", sa[0], "port", sa[1], "..."))

httpd.serve_forever()
