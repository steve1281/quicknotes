#!/usr/bin/env python
import uvicorn
import os
import markdown
from fastapi.responses import HTMLResponse, FileResponse
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
document_folder = os.getenv('QUICKNOTES', '/docs/')
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
        template = f"<h2>Populate the {document_folder}template folder.</h2><br>[BODY]"
    return template.replace("[STYLE]", get_style()).replace("[BODY]", body)


def build_quick_notes():
    files = list_files(document_folder)
    quick_notes = sorted(build_quick_note_list(files), key=lambda x: int(x.split('-')[0]))
    return quick_notes


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
    uvicorn.run(app='fapi:app', host='0.0.0.0', port=int(_port), reload=True, debug=True)
