from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
import threading
import time

# FastAPIアプリケーションの作成
app = FastAPI()

# CORS設定を追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Socket.IOの設定
sio = socketio.AsyncServer(cors_allowed_origins=["http://localhost:3000"])
sio_app = socketio.ASGIApp(sio, app)

@app.on_event("startup")
async def startup_event():
    def monitor_loop():
        while True:
            # ここに監視ロジックを追加
            time.sleep(10)  # 例として5秒ごとにチェック
            message = {'name': 'Event', 'image': 'path/to/image'}
            sio.emit('message', message)

    monitor_thread = threading.Thread(target=monitor_loop)
    monitor_thread.daemon = True
    monitor_thread.start()

@sio.event
async def connect(sid, environ):
    print('Client connected:', sid)

@sio.event
async def disconnect(sid):
    print('Client disconnected:', sid)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(sio_app, host="localhost", port=8000)