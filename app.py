import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# 1. API Endpoint
@app.get("/api/test")
async def test_api():
    return {"status": "success", "message": "Native FastAPI is working!"}

# 2. Serve React Static Files
# This assumes your build files are in a folder named 'static'
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# 3. React Catch-all (Must be last)
@app.get("/{catchall:path}")
async def serve_react(catchall: str):
    # Check if a specific file exists (e.g., favicon.ico)
    file_path = os.path.join("static", catchall)
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    
    # Fallback to index.html for React Router
    index_path = os.path.join("static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "Static folder missing index.html"}