from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from shiny import App, ui
import os

# --- 1. Your FastAPI App ---
api_app = FastAPI()

@api_app.get("/api/test")
async def test_api():
    return {"status": "success", "message": "FastAPI is working inside Shiny!"}

# --- 2. Serving React ---
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
    return {"error": "Static files not found"}

# --- 3. The Shiny Wrapper (The Part Posit Cloud Sees) ---
app_ui = ui.page_fluid(
    ui.h2("Application Gateway"),
    ui.p("If you see this, the server is live. Go to /api/test to check the API."),
    ui.tags.script("window.location.href = '/api/test';") # Optional: Auto-redirect to API
)

def server(input, output, session):
    pass

app = App(app_ui, server)

# MOUNT FastAPI to the Shiny ASGI app
# This makes FastAPI handle routes starting with /api or any other specified
app.mount("/", api_app)