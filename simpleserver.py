#!/usr/bin/env python

import sys
import os
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from squick import *

TEMPLATE_RESPONSE = """<html><head><title>Python Test</title></head><body>[BODY]</body></html>"""

MENU_HEADER = """

    <div><pre>
        QuickNotes: Search and Display (HTTP interface)
        Source folder is: " +  [INITFOLDER]
        http://127.0.0.1:8000/help  - this help
        http://127.0.0.1:8000/list  - list the files
        http://127.0.0.1:8000/filter/filter1/filter2/...
    </pre></div>

    """


class MyHttpRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.response_code = 200

        response_string = TEMPLATE_RESPONSE
        body = self.get_body(self.requestline)
        response_string = response_string.replace("[BODY]", body)
        self.send_response(self.response_code)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", len(response_string ))
        self.end_headers()
        self.wfile.write(response_string)

    def get_body(self, request):
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
            add_list_converter = ('<li><a href="'+w+'">'+w+'</a></li>' for w in quicknotes)
            return "<ul>"+"\n".join(add_list_converter)+"</ul>"
        elif (len(argument_string) >= 6 and argument_string[:6]=='filter' or None):
            filters = argument_string.split("/")
            filters.reverse()
            filters.pop()
            filtered_list = quicknotes
            for filter in filters:
                filtered_list = filterout(filtered_list, filter)
            add_list_converter = ('<li><a href="http://127.0.0.1:8000/'+w+'">'+w+'</a></li>' for w in filtered_list)
            return "<ul>"+"\n".join(add_list_converter)+"</ul>"
        elif argument_string == "favicon.ico":
            return ""
        else:
            s = "Error has occurred"
            try:
                s = "<pre>" + dumpQuickNote([self.strip(argument_string)], newfilterstring) + "</pre>"
            except Exception as e:
                self.response_code = 404
            return s

    def strip(self,s):
        return s.replace("%20", " ")

HandlerClass = MyHttpRequestHandler
ServerClass = BaseHTTPServer.HTTPServer
Protocol = "HTTP/1.0"

if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8000

server_address = ('127.0.0.1', port)

HandlerClass.protocol_version = Protocol
httpd = ServerClass(server_address, HandlerClass)
sa = httpd.socket.getsockname()
print "Serving HTTP on", sa[0], "port", sa[1], "..."

httpd.serve_forever()
