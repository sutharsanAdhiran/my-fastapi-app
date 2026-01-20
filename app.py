from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from shiny import App, ui
import os

# --- 1. Your FastAPI Logic ---
api_app = FastAPI()

@api_app.get("/api/test")
async def test_api():
    return {"status": "success", "message": "API is working through the Shiny host!"}

# Serve React build from the 'static' folder
if os.path.exists("static"):
    api_app.mount("/static", StaticFiles(directory="static"), name="static")

@api_app.get("/{catchall:path}")
async def serve_react_app(catchall: str):
    file_path = os.path.join("static", catchall)
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    index_path = os.path.join("static", "index.html")
    return FileResponse(index_path) if os.path.exists(index_path) else {"error": "No index.html"}

# --- 2. The Shiny "Mask" ---
# This is what Posit Connect Cloud looks for.
app_ui = ui.page_fluid(ui.h3("Backend Active")) 
app = App(app_ui, None)

# The "Magic" line: Replace Shiny's internal handler with FastAPI
app.asgi_app = api_app