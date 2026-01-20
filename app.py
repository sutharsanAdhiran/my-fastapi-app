from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.applications import Starlette
from starlette.routing import Mount
from shiny import App, ui
import os

# 1. Your FastAPI Logic
api_app = FastAPI()

@api_app.get("/api/test")
async def test_api():
    return {"status": "success", "message": "API via Starlette-Shiny Hybrid!"}

# 2. Setup Starlette Routing
# This handles the React static files and the catch-all routing
routes = []

# Serve static folder if it exists
if os.path.exists("static"):
    routes.append(Mount("/static", app=StaticFiles(directory="static"), name="static"))

# 3. Create a Placeholder Shiny App 
# Connect Cloud requires the 'shiny' package and a 'shiny.App' object to be present.
app_ui = ui.page_fluid(ui.h3("App Loading..."))
shiny_app = App(app_ui, None)

# 4. The Final Combined App (The "Magic")
# We create a Starlette app that handles your API and React files.
# Then we attach it to the Shiny object so the server runs THIS instead.
combined_app = FastAPI()

# Mount your actual API logic
combined_app.mount("/api", api_app)

# Mount the static files
if os.path.exists("static"):
    combined_app.mount("/static", StaticFiles(directory="static"), name="static")

# Catch-all for React index.html
@combined_app.get("/{catchall:path}")
async def serve_react(catchall: str):
    index_path = os.path.join("static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "React build not found"}

# Tell the Shiny App object to use our combined FastAPI/Starlette app as its engine
shiny_app.asgi_app = combined_app

# Posit Connect Cloud looks for the variable named 'app'
app = shiny_app