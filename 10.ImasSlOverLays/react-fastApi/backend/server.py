from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import threading
import time
import asyncio
import os
from models import *

# スクリプト自身のディレクトリを取得
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, '..','..','..',"00.DataStorage","cinderella.idolmaster.sl-stage.sqlite")
songDetail = None
songLevelDetail = None
songMetaData = None

app = FastAPI()
class SongSelection(BaseModel):
    SongName: str
    Level: str
    
# CORS設定を追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # すべてのオリジンを許可
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可
    allow_headers=["*"],  # すべてのヘッダーを許可
)

# WebSocket接続を管理するためのリスト
websockets = []

# WebSocketエンドポイントを追加
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websockets.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received message: {data}")
    except:
        websockets.remove(websocket)

# 曲選択が行われた
@app.post("/select_song")
async def select_song(selection: SongSelection):
    print(f"Received song selection: {selection.SongName}, Level: {selection.Level}")
    songDetail = get_song_meta_data_from_db(db_path,selection.SongName)
    # WebSocket接続にメッセージを送信
    for websocket in websockets:
        await websocket.send_text(f"Song selected: {selection.SongName}, Level: {selection.Level}")
    return {"status": "Song selection received"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)