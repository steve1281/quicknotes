#!/usr/bin/env python
import random

import uvicorn
import os
import markdown
from fastapi.responses import HTMLResponse, FileResponse
from starlette.responses import RedirectResponse

from fortune import get_fortune, get_record_count
from squick import dump_quick_note, list_files, build_quick_note_list, build_filtered_file_list
from fastapi import FastAPI

app = FastAPI()

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

# ---- globals ----
document_sources = os.getenv('QUICKNOTES', '/docs/').split(',')
document_folder = document_sources[0]
if not document_folder.endswith('/'):
    document_folder = document_folder + "/"
_port = os.getenv('PORT', '8000')
_ip = os.getenv('IPADDRESS', '127.0.0.1')


# --- helper ----
def strip(s):
    return s.replace("%20", " ")


def template_loader(file):
    try:
        with open(file) as f:
            return f.read()
    except FileNotFoundError:
        return ""


def get_style():
    return template_loader(document_folder + "templates/style.template")


def build_response(body):
    template = template_loader(document_folder + "templates/body.template")
    if template == "":
        template = f"<h2>Populate the {document_folder} template folder.</h2><br>[BODY]"
    return template.replace("[STYLE]", get_style()).replace("[BODY]", body)


def build_quick_notes():
    files = list_files(document_folder)
    quick_notes = sorted(build_quick_note_list(files), key=lambda x: int(x.split('-')[0]))
    return quick_notes


def select_fortune(filename):
    """
    A random fortune
    :param filename: filename to pull the fortune from
    :return:
    """
    record_count = get_record_count(document_folder+filename)
    random_record = random.randint(0, record_count-1)
    s = get_fortune(document_folder+filename, random_record)
    return f'<a href="/">home</a><hr><div><br><pre><span class="inner-pre" style="font-size: 18px">{s}</span></pre><br></div>'


# --- API ---
@app.get("/", response_class=HTMLResponse)
async def root():
    template = template_loader(document_folder + "templates/root.template")
    return build_response(template.replace("[IPADDRESS]", _ip).replace("[PORT]", _port)
                          .replace("[INITFOLDER]", document_folder))


@app.get("/blah/blah", response_class=HTMLResponse)
async def blah():
    return "Sure bub, here is some blah blah for you."


@app.get("/list", response_class=HTMLResponse)
async def list_quick_notes():
    quick_notes = build_quick_notes()
    add_list_converter = ('<li><a class="quickanchor" href="' + w + '">'
                          + w + '</a></li>' for w in quick_notes)
    body = "<ul id='quicklist'>" + "\n".join(add_list_converter) + "</ul>"
    return build_response(body)


@app.get("/filter={filters}", response_class=HTMLResponse)
async def read_item(filters):
    quick_notes = build_quick_notes()
    filter_list = filters.split(",")
    filter_list.reverse()
    filtered_list = quick_notes
    for s in filter_list:
        filtered_list = build_filtered_file_list(document_folder, filtered_list, s)
    add_list_converter = ('<li><a class="quickanchor" href="http://' + _ip + ':' + _port + '/' + w + '">'
                          + w + '</a></li>' for w in filtered_list)
    body = "<ul>" + "\n".join(add_list_converter) + "</ul>"
    return build_response(body)


@app.get("/templates/{resource}")
async def templates_folder(resource: str):
    return HTMLResponse(build_response(f"No access to {resource}."))


@app.get('/sources')
async def list_docs():
    body = f"Current document source: <b>{document_folder}</b>"
    body = body + f"<h2>Available sources</h2>"
    body = body + f"<ol>"
    for idx, src in enumerate(document_sources):
        body = body + f"<li><a href='//{_ip}:{_port}/setsource/{idx}'>{src}</a></li>"
    body = body + "</ol>"
    return HTMLResponse(build_response(body))


@app.get('/setsource/{srcid}')
async def set_document_source(srcid: int):
    global document_folder
    document_folder= document_sources[srcid]
    if not document_folder.endswith('/'):
        document_folder = document_folder + "/"
    return RedirectResponse(url='/')


@app.get('/fortune')
async def fortune():
    return HTMLResponse(build_response(select_fortune("scene")))


@app.get('/fortune/obscene')
async def fortune_obscene():
    return HTMLResponse(build_response(select_fortune("obscene")))


@app.get('/{filename}', include_in_schema=False)
async def all_others(filename: str):
    _, ext = os.path.splitext(filename)
    if ext.lower() in ['.jpg', '.gif', '.png', '.jpeg', '.mp4']:
        return FileResponse(path=document_folder + filename)
    elif ext in ['.md', '.MD']:
        s, _ = dump_quick_note(document_folder, strip(filename))
        s = markdown.markdown(s, extensions=md_extensions)
        s = "<div id='wrapper'>" + s + "</div>"
        return HTMLResponse(build_response(s))
    elif ext in ['.txt', '.TXT']:
        s, _ = dump_quick_note(document_folder, strip(filename))
        s = "<div id='wrapper'><pre>" + s + "</pre></div>"
        return HTMLResponse(build_response(s))
    else:
        return HTMLResponse(build_response("Unsupported extension"))



if __name__ == '__main__':
    uvicorn.run(app='fapi:app', host='0.0.0.0', port=int(_port), reload=True, debug=False)
