from dataclasses import dataclass

from litestar import Litestar, get, post
from litestar.config.cors import CORSConfig


@dataclass
class TodoItem:
    title: str
    done: bool

TODO_LIST: list[TodoItem] = [
    TodoItem(title="Start writing TODO list", done=True),
    TodoItem(title="???", done=False),
    TodoItem(title="Profit", done=False),
]

@get("/")
async def get_list(done: bool | None = None) -> list[TodoItem]:
    if done is None:
        return TODO_LIST
    return [item for item in TODO_LIST if item.done == done]

@post("/")
async def add_item(data: TodoItem) -> list[TodoItem]:
    TODO_LIST.append(data)
    return TODO_LIST

app = Litestar([get_list, add_item], cors_config=CORSConfig(allow_origins=["*"]))
