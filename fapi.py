
#!/usr/bin/env python
import uvicorn
import re
import os
import markdown
from fastapi.responses import HTMLResponse, FileResponse
from squick import dumpQuickNote, list_files, quicknotelist, filterout
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
initfolder = os.getenv('QUICKNOTES', '/docs/')
if not initfolder.endswith('/'):
    initfolder = initfolder + "/"

_port = os.getenv('PORT', '8000')
_ip = os.getenv('IPADDRESS', '127.0.0.1')


# --- helper ----
def strip(s):
    return s.replace("%20", " ")


def template_loader(file):
    try:
        with open(file) as f:
            return f.read()
    except:
        return ""


def get_style():
    return template_loader(initfolder+"templates/style.template")


def build_response(body):
    template = template_loader(initfolder+"templates/body.template")
    if template == "":
        template = f"<h2>Populate the {initfolder}template folder.</h2><br>[BODY]"
    return template.replace("[STYLE]", get_style()).replace("[BODY]", body)


# --- API ---
@app.get("/", response_class=HTMLResponse)
async def root():
    template = template_loader(initfolder+"templates/root.template")
    return build_response(template.replace("[IPADDRESS]", _ip).replace("[PORT]", _port).replace("[INITFOLDER]", initfolder))


@app.get("/blah/blah", response_class=HTMLResponse)
async def blah():
    return "Sure bub, here is some blah blah for you."


@app.get("/list", response_class=HTMLResponse)
async def list_quick_notes():
    files = list_files(initfolder)
    quicknotes = sorted(quicknotelist(files), key=lambda x: int(re.split("-| ", x)[0]))
    add_list_converter = ('<li><a class="quickanchor" href="' + w + '">' + w + '</a></li>' for w in quicknotes)
    body = "<ul id='quicklist'>" + "\n".join(add_list_converter) + "</ul>"
    return build_response(body)


@app.get("/filter={filters}", response_class=HTMLResponse)
async def read_item(filters):
    files = list_files(initfolder)
    quicknotes = sorted(quicknotelist(files), key=lambda x: int(re.split("-| ", x)[0]))
    filter_list = filters.split(",")
    filter_list.reverse()
    filtered_list = quicknotes
    for s in filter_list:
        filtered_list = filterout(initfolder, filtered_list, s)
    add_list_converter = ('<li><a class="quickanchor" href="http://' + _ip + ':' + _port + '/' + w + '">' + w + '</a></li>' for w in filtered_list)
    body = "<ul>" + "\n".join(add_list_converter) + "</ul>"
    return build_response(body)


@app.get("/templates/{resource}")
async def templates_folder(resource: str):
    return HTMLResponse(build_response("No access."))


@app.get('/{filename}', include_in_schema=False)
async def all_others(filename: str):
    _, ext = os.path.splitext(filename)
    if ext.lower() in ['.jpg', '.gif', '.png', '.jpeg','.mp4']:
        with open(initfolder + filename, "rb") as f:
            return FileResponse(path=initfolder+filename)
    elif ext in ['.md', '.MD']:
        s, _ = dumpQuickNote(initfolder, strip(filename))
        s = markdown.markdown(s, extensions=md_extensions)
        s = "<div id='wrapper'>" + s + "</div>"
        return HTMLResponse(build_response(s))
    elif ext in ['.txt', '.TXT']:
        s, _ = dumpQuickNote(initfolder, strip(filename))
        s = "<div id='wrapper'><pre>" + s + "</pre></div>"
        return HTMLResponse(build_response(s))
    else:
        return HTMLResponse(build_response("Unsupported extension"))


if __name__ == '__main__':
    uvicorn.run(app='fapi:app', host='0.0.0.0', port=int(_port), reload=True, debug=True)
