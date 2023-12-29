import random
from base64 import urlsafe_b64encode

from fastapi.responses import HTMLResponse
from html_dsl.common import *
from html_dsl.elements import BaseHtmlElement

script = """function save() {
  fetch(location.toString(), {
    method: "POST",
    body: document.getElementById("editor").value,
  });
}"""

head = HEAD[
    META['charset="utf-8"'],
    META['name="viewport" content="width=device-width, initial-scale=1"'],
    TITLE["Notepad"],
    SCRIPT[script],
]


def str_without_blanks(element: BaseHtmlElement):
    blank = ""
    attrs = (
        " {}".format(
            " ".join(
                f'{key.replace("_", "-")}="{str(element.attrs[key])}"'
                for key in element.attrs
            )
        )
        if element.attrs
        else ""
    )
    children = "\n".join(
        str_without_blanks(child)
        if isinstance(child, BaseHtmlElement)
        else blank + str(child)
        for child in element.children
    )
    if element.single:
        return "{blank}<{name}{attrs}>".format(
            blank=blank, name=element.name, attrs=attrs
        )
    if element.no_content:
        return "{blank}<{name}{attrs}/>".format(
            blank=blank, name=element.name, attrs=attrs
        )
    return "{blank}<{name}{attrs}>\n{children}\n{blank}</{name}>".format(
        blank=blank, name=element.name, attrs=attrs, children=children
    )


def render(element: BaseHtmlElement):
    return HTMLResponse(str_without_blanks(element))


def render_note(content: str):
    return render(
        HTML(lang="en")[
            head,
            BODY[
                BUTTON(onClick="save()")["Save"],
                TEXTAREA(
                    id="editor",
                    placeholder="input text here",
                    style="width:100%;height:100%;font-size:20px;",
                )[content or "input text here"],
            ],
        ]
    )


def gen_note_id():
    return urlsafe_b64encode(random.randbytes(6)).decode()
