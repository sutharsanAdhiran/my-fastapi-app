from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from shiny import App, ui
import os

# 1. Your Actual FastAPI App
api_app = FastAPI()

@api_app.get("/api/test")
async def test_api():
    return {"status": "success", "message": "FastAPI is fully operational!"}

# Serve React build
if os.path.exists("static"):
    api_app.mount("/static", StaticFiles(directory="static"), name="static")

@api_app.get("/{catchall:path}")
async def serve_react_app(catchall: str):
    file_path = os.path.join("static", catchall)
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    index_path = os.path.join("static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "Static folder or index.html missing"}

# 2. The Shiny "Gateway"
# We create a dummy UI so Shiny doesn't complain
app_ui = ui.page_fluid(ui.h3("Server Redirecting..."))

def server(input, output, session):
    pass

# 3. Create the Shiny App
app = App(app_ui, server)

# 4. The Hijack Logic (Middleware)
# This forces the underlying Starlette/Uvicorn handler 
# to use your FastAPI app instead of the Shiny UI.
app.asgi_app = api_app