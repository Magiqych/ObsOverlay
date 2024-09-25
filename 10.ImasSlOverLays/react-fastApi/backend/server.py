from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import threading
import time
import asyncio
import os
from database import search_song_by_name, injectResult

app = FastAPI()

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

# ルートエンドポイントを追加
@app.get("/")
async def read_root():
    return RedirectResponse(url="http://localhost:3000/init")

# リダイレクトエンドポイントを追加
@app.get("/redirect")
async def redirect_to_react():
    return RedirectResponse(url="http://localhost:3000/init")

def start_uvicorn():
    uvicorn.run(app, host="localhost", port=8000)

async def manage_loop():
    while True:
        # イベントを監視するロジックをここに追加
        # イベントが発生したらリダイレクト
        print("イベントが発生しました。リダイレクトします。")
        search_song_by_name("とどけ！アイドル")
        for websocket in websockets:
            try:
                websocket.send_text("redirect")
            except:
                websockets.remove(websocket)
        await asyncio.sleep(2000000000000000) 

if __name__ == "__main__":
    # uvicornサーバーを別スレッドで起動
    uvicorn_thread = threading.Thread(target=start_uvicorn)
    uvicorn_thread.start()

    # 非同期関数を実行するためのイベントループを作成
    loop = asyncio.get_event_loop()
    loop.run_until_complete(manage_loop())