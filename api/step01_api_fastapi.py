# terminal:  pip install "fastapi[standard]"
# file: main.py
from fastapi import FastAPI

app = FastAPI(title="GeoAI Flood Service")

@app.get("/")                        # handle GET requests to "/"
def root():
    return {"message": "GeoAI API is running", "docs": "/docs"}

@app.get("/hello/{name}")            # {name} is a path parameter
def hello(name: str):
    return {"greeting": f"Hello, {name}"}
