import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
#
# from app.db import Base
from app.models.db import engine, SessionLocal
from app.api.api import api_router

app = FastAPI()
app.include_router(api_router)

# app.mount("/static", StaticFiles(directory="static"), name="static")


# @app.get("/")
# async def root():
#     return FileResponse('static/index.html')


@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f'Message text was: {data}')


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)