from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    return {"message": "Hello World"}


@app.get("/blog/{blog_id}")
def show(blog_id: int):
    return {"data": blog_id}


@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello {name}"}
