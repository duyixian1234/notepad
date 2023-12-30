import random
from base64 import urlsafe_b64encode

from fastapi.responses import HTMLResponse
from html_dsl.common import *
from html_dsl.elements import BaseHtmlElement

script = """
function save() {
  fetch(location.toString(), {
    method: "POST",
    body: document.getElementById("editor").value,
  });
}
document.addEventListener('keydown', function(event) {
    if (event.ctrlKey && event.key === 's') {
        save();
        event.preventDefault();
}});
"""

head = HEAD[
    META['charset="utf-8"'],
    META['name="viewport" content="width=device-width, initial-scale=1"'],
    TITLE["Notepad"],
    SCRIPT[script],
]


def render(element: BaseHtmlElement):
    return HTMLResponse(str(element))


def render_note(content: str):
    return render(
        HTML(lang="en")[head, BODY[BUTTON(onClick="save()")["Save"], editor(content)]]
    )


def editor(content):
    return TEXTAREA(
        id="editor",
        placeholder="input text here",
        style="width:100%;height:100%;font-size:20px;",
    )[content or "input text here"]


def gen_note_id():
    return urlsafe_b64encode(random.randbytes(6)).decode()
