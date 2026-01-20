from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from shiny import App, ui
import os

# --- 1. Your FastAPI Setup ---
api_app = FastAPI()

# API Endpoint
@api_app.get("/api/test")
async def test_api():
    return {"status": "success", "message": "FastAPI is live!"}

# Serve React static assets (JS/CSS)
if os.path.exists("static"):
    # This mounts the folder 'static' to the URL path '/static'
    api_app.mount("/static", StaticFiles(directory="static"), name="static")

# Catch-all to serve index.html for the React Frontend
@api_app.get("/{catchall:path}")
async def serve_react_app(catchall: str):
    file_path = os.path.join("static", catchall)
    # 1. Check if the specific file exists (like /favicon.ico)
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    
    # 2. Otherwise, serve index.html for React Router
    index_path = os.path.join("static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    
    return {"error": "React build (index.html) not found in /static folder"}

# --- 2. The Shiny Wrapper ---
# We create a minimal Shiny app, but we immediately 
# overwrite its handler with our FastAPI app.
app = App(ui.page_fluid(), None)

# IMPORTANT: This line redirects ALL traffic to FastAPI
# It must come after 'app' is defined.
app.handler = api_app