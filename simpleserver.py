#!/usr/bin/env python

import sys
import os
# https://github.com/polarwinkel/mdtex2html
# import mdtex2html
import markdown
import http.server
from http.server import SimpleHTTPRequestHandler

import logging
logging.basicConfig(filename='quicknotes.log', level=logging.DEBUG)

from squick import *


_port = os.getenv('PORT','8000')
_ip   = os.getenv('IPADDRESS', '127.0.0.1')

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

TEMPLATE_RESPONSE = """<html><head><title>Placeholder</title>[STYLE]</head><body>[BODY]</body></html>"""

MENU_HEADER = """

    <div><pre>
        QuickNotes: Search and Display (HTTP interface)
        Source folder is: " +  [INITFOLDER]
        http://ipaddress:port/help  - this help
        http://ipaddress:port/list  - list the files
        http://ipaddress:port/filter/filter1/filter2/...
    </pre></div>

    """


class MyHttpRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        logging.debug(f"do_GET called: {self.requestline}")
        self.response_code = 200

        response_string = TEMPLATE_RESPONSE
        body = self.get_body(self.requestline)
        if body == "":
            self.send_response(403)
            return
        
        response_string = response_string.replace("[BODY]", body)
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
        global initfolder
        # initfolder = os.getcwd() + "/"
        files = list_files(initfolder)
        quicknotes = sorted(quicknotelist(files),key = lambda x: int(re.split("-| ",x)[0]))
        newfilterstring= ""
        argument_string = len(request) >= 14 and request[5:-9] or None


        if argument_string is None:
            return MENU_HEADER.replace("[INITFOLDER]",  initfolder)
        elif argument_string == 'blah/blah':
            return "Sure bub, here is some blah blah for you."
        elif argument_string == "?":
            return MENU_HEADER.replace("[INITFOLDER]",  initfolder)
        elif argument_string == "list":
            add_list_converter = ('<li><a class="quickanchor" href="'+w+'">'+w+'</a></li>' for w in quicknotes)
            return "<ul id='quicklist'>"+"\n".join(add_list_converter)+"</ul>"
        elif (len(argument_string) >= 6 and argument_string[:6]=='filter' or None):
            filters = argument_string.split("/")
            filters.reverse()
            filters.pop()
            filtered_list = quicknotes
            for filter in filters:
                filtered_list = filterout(filtered_list, filter)
            add_list_converter = ('<li><a class="quickanchor" href="http://'+_ip+':'+_port+'/'+w+'">'+w+'</a></li>' for w in filtered_list)
            return "<ul>"+"\n".join(add_list_converter)+"</ul>"
        elif argument_string == "favicon.ico":
            return ""
        else:
            s = "Error has occurred"
            try:
                s,ext =  dumpQuickNote([self.strip(argument_string)], newfilterstring) 
                if ext in ['.md', '.MD']:
                    # s = markdown.convert(s, extensions=md_extensions)
                    s = markdown.markdown(s, extensions=md_extensions)
                else:
                    s = "<pre>" + s + "</pre>"
            except Exception as e:
                logging.error(e)
                self.response_code = 404
            s = "<div id='wrapper'>"+s+"</div>"
            return s

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
