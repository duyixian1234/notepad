import random
from base64 import urlsafe_b64encode

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from html_dsl.common import *
from html_dsl.elements import BaseHtmlElement


def render(element: BaseHtmlElement):
    return HTMLResponse(str(element))


app = FastAPI()


@app.get("/")
async def root():
    id = urlsafe_b64encode(random.randbytes(6)).decode()
    return RedirectResponse(f"/{id}")


@app.get("/{id}")
async def note(id: str):
    return render(
        HTML(lang="en")[
            HEAD[
                META['charset="utf-8"'],
                META['name="viewport" content="width=device-width, initial-scale=1"'],
                TITLE["Notepad"],
                SCRIPT[
                    """
setInterval(() => {fetch(location.toString(),{method:'POST',body:document.getElementById("editor").value})},3000)
"""
                ],
            ],
            BODY[
                TEXTAREA(
                    id="editor",
                    placeholder="input text here",
                    style="width:100%;height:100%;font-size:20px;",
                )
            ],
        ]
    )


@app.post("/{id}")
async def note_post(id: str, request: Request):
    print(await request.body())
    return ""
