---
tags:
  - web
created: 2023-11-18
presented:
---
# 0x02

---

# What is a server

[https://www.youtube.com/watch?v=VXmvM2QtuMU](https://www.youtube.com/watch?v=VXmvM2QtuMU)

---

# What is a protocol

[https://www.youtube.com/watch?v=d-zn-wv4Di8](https://www.youtube.com/watch?v=VXmvM2QtuMU)

---

# Building an (insecure) TODO app

---

# LITESTAR
![litestar logo](./assets/0x02-litestar-logo.svg)

- new $\implies$ fun
- python

---

```py [1|3-5|7]
from litestar import Litestar, get

@get("/")
async def hello_world() -> str:
    return "Hello, world!"

app = Litestar([hello_world])
```

---

```py 
@get("/")
async def hello_world() -> str:
    return "Hello, world!"
```

```py 
async def hello_world() -> str:
    return "Hello, world!"

hello_world = get("/")(hello_world)
```

---

```py [1-13|15-17]
def log_args(func):
    def wrapper(*args, **kwargs):
        arg_values = ', '.join(str(arg) for arg in args)
        kwarg_values = ', '.join(
	        f"{key}={value}" for key, value in 
	        kwargs.items()
	    )
        print(
	        f"Calling {func.__name__} with args: \
	        {arg_values} and kwargs: {kwarg_values}"
        )
        return func(*args, **kwargs)
    return wrapper

@log_args
def my_function(a, b, c=3):
    return a + b + c
```

---

```py [3|3-6|9-13]
from dataclasses import dataclass

@dataclass
class TodoItem:
    title: str
    done: bool


TODO_LIST: list[TodoItem] = [
    TodoItem(title="Start writing TODO list", done=True),
    TodoItem(title="???", done=False),
    TodoItem(title="Profit", done=False),
]
```

```py
@get("/")
async def get_list() -> list[TodoItem]:
    return TODO_LIST

app = Litestar([get_list])
```

---

```py
@get("/")
async def get_list(done: str) -> list[TodoItem]:
    if done == "1":
        return [item for item in TODO_LIST if item.done]
    return [item for item in TODO_LIST if not item.done]
```

http://localhost:8000/?done=1

---

```py [2|]
@get("/")
async def get_list(done: bool) -> list[TodoItem]:
    return [
	    item for item in TODO_LIST 
	    if item.done == done
	]
```

---

```py
@get("/")
async def get_list(
	done: bool | None = None
) -> list[TodoItem]:
    if done is None:
        return TODO_LIST
    return [item for item in TODO_LIST if item.done == done]
```

http://localhost:8000/schema/elements#/

---

```py
@post("/")
async def add_item(data: TodoItem) -> list[TodoItem]:
    TODO_LIST.append(data)
    return TODO_LIST
```

http://localhost:8000/schema/elements#/

---

# Quick Refactor to Use SQLite

- advantages of using a database?
- advantages of using an ORM?

---

I don't know how to use `LIKE` in `sqlalchemy` so I wrote some raw SQL.

```py
@get("/search")
async def search_for_item(
	state: State, title: str | None = None
) -> TodoCollectionType:
    async with sessionmaker(bind=state.engine) as session:
        if title is not None:
            todos = await session.execute(text(
	            f"SELECT title, done FROM todo_items \
	            WHERE title LIKE '%{title}%';"
	        ))
            return [
	            {"title": t[0], "done": bool(t[1])}
	            for t in todos
	        ]

    return []
```