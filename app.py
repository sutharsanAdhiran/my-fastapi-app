from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from shiny import App, ui
import os

# 1. Your FastAPI App (The real logic)
api_app = FastAPI()

@api_app.get("/api/test")
async def test_api():
    return {"status": "success", "message": "FastAPI via Middleware is working!"}

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
    return {"error": "index.html not found"}

# 2. The Shiny "Shell" (The part that satisfies the Cloud)
app_ui = ui.page_fluid(ui.h3("Redirecting..."))
def server(input, output, session):
    pass

app = App(app_ui, server)

# 3. THE FIX: Attach FastAPI as the underlying ASGI handler
# This bypasses the Shiny UI and lets FastAPI handle everything.
app.asgi_app = api_app