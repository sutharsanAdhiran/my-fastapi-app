import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from shiny import App, ui

# 1. Your FastAPI Logic
api_app = FastAPI()

@api_app.get("/test") # This will be available at /api/test
async def test_api():
    return {"status": "success", "message": "FastAPI is active on /api path!"}

# 2. The Shiny UI (The Entry Point)
# This will be the first thing people see. We provide a direct link
# to your React frontend to ensure the user gets there.
app_ui = ui.page_fluid(
    ui.h2("Application Gateway"),
    ui.p("Click the button below to enter the application."),
    ui.a("Enter App", href="/app/", class_="btn btn-primary"),
    # This meta tag tries to do it automatically
    ui.head_content(
        ui.tags.meta(http_equiv="refresh", content="0; url=/app/")
    )
)

def server(input, output, session):
    pass

app = App(app_ui, server)

# 3. Handle the React Frontend manually via FastAPI
# We create a separate FastAPI instance specifically for the Frontend
frontend_app = FastAPI()

if os.path.exists("static"):
    frontend_app.mount("/assets", StaticFiles(directory="static"), name="assets")

@frontend_app.get("/{catchall:path}")
async def serve_react(catchall: str):
    index_path = os.path.join("static", "index.html")
    return FileResponse(index_path)

# 4. MOUNT BOTH TO THE SHINY APP
# This is the most stable way to avoid route conflicts on Connect Cloud
app.mount("/api", api_app)      # Your API logic is now at /api
app.mount("/app", frontend_app) # Your React app is now at /app