#!/usr/bin/env python
import random

import uvicorn
import os
import markdown
from fastapi.responses import HTMLResponse, FileResponse
from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from fortune import get_fortune, get_record_count
from webloc import get_webloc_files, build_url_list
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

# --- static file mounts ----


def purge_route(route_name):
    for x in app.routes:
        if x.name == route_name:
            app.routes.remove(x)


def create_static_mounts():
    purge_route('js')
    app.mount(
        "/js",
        StaticFiles(directory=document_folder + "/js"),
        name="js"
    )

    purge_route('css')
    app.mount(
        "/css",
        StaticFiles(directory=document_folder + "/css"),
        name="css"
    )


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
    return template.replace("[STYLE]", get_style()) .replace("[BODY]", body) .replace("[IPADDRESS]",_ip) .replace("[PORT]",_port)


def build_url_div(url_list):
    div_contents = "<div>\n"

    div_contents = div_contents + "<table class='sortable' id='quicknote_table'>\n"
    div_contents = div_contents + "<thead>\n"
    div_contents = div_contents + "<tr>\n"
    div_contents = div_contents + "<th style='width:50%'>Web Link</th>\n"
    div_contents = div_contents + "<th style='width:25%'>Link Type</th>\n"
    div_contents = div_contents + "<th class='date' style='width:35%'>Created</th>\n"
    div_contents = div_contents + "</tr>\n"
    div_contents = div_contents + "</thead>\n"

    div_contents = div_contents + "<tbody>\n"

    for key in url_list:
        anchor_string = f'<a href="{url_list[key]["url"]}" target="_blank">{key}</a>'
        div_contents = div_contents + "<tr>\n"
        div_contents = div_contents + "<td>" + anchor_string + "</td>\n"
        div_contents = div_contents + "<td>" + url_list[key]['link type'] + "</td>\n"
        div_contents = div_contents + "<td>" + url_list[key]['created'] + "</td>\n"
        div_contents = div_contents + "</tr>\n"

    div_contents = div_contents + "</tbody>\n"

    div_contents = div_contents + "</table>\n"

    div_contents = div_contents + "<script src='/js/sort-table.js'></script>\n"
    div_contents = div_contents + "</div>\n"
    return div_contents


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
    document_folder = document_sources[srcid]
    if not document_folder.endswith('/'):
        document_folder = document_folder + "/"
    create_static_mounts()
    return RedirectResponse(url='/')


@app.get('/fortune/{filename}')
async def fortune(filename: str):
    record_count = get_record_count(document_folder + filename)
    if record_count > 0:
        random_record = random.randint(0, record_count - 1)
        s = get_fortune(document_folder+filename, random_record)
        body = f'''
        <pre>
            <span class="inner-pre" style="font-size: 18px">{s}</span>
        </pre>
        <a href="//{_ip}:{_port}/fortune/{filename}/{random_record}">{random_record}</a>
        '''
    else:
        body = f'Error reading {filename}.'
    return HTMLResponse(build_response(body))


@app.get('/links/{folder_name}')
async def build_webloc_link_page(folder_name :str):
    body = ""
    files = get_webloc_files(document_folder, folder_name)
    if files:
        url_list = build_url_list(files)
        if url_list:
            body = build_url_div(url_list)
        else:
            body = f"No urls found in {folder_name}"
    else:
        body = f"No files found in {folder_name}"
    return HTMLResponse(build_response(body))


@app.get('/fortune/{filename}/{record_number}')
async def fortune(filename: str, record_number: int):
    record_count = get_record_count(document_folder + filename)
    if record_count < record_number:
        body = f"Invalid record_number {record_number}. Must be less than {record_count}."
    else:
        s = get_fortune(document_folder + filename, record_number)
        body = f'<pre><span class="inner-pre" style="font-size: 18px">{s}</span></pre>'
    return HTMLResponse(build_response(body))


@app.get('/{filename}', include_in_schema=False)
async def all_others(filename: str):
    _, ext = os.path.splitext(filename)
    if ext.lower() in ['.jpg', '.gif', '.png', '.jpeg', '.mp4', '.htm', '.html']:
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
    create_static_mounts()
    uvicorn.run(app='fapi:app', host='0.0.0.0', port=int(_port), reload=True, debug=False)
