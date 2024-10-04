import json
import aiofiles
from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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
# 曲情報を格納する変数
songDetail = None
songLevelDetail = None
songMetaData = None
songRecords = None
# 曲選択情報を格納するクラス
class SongSelection(BaseModel):
    SongName: str
    Level: str

# FastAPIのインスタンスを作成
app = FastAPI()
# CORS設定を追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # すべてのオリジンを許可
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可
    allow_headers=["*"],  # すべてのヘッダーを許可
)
# 静的ファイルのルーティング
app.mount("/public", StaticFiles(directory=os.path.join(script_dir, 'public')), name="public")

# WebSocket接続を管理するためのリスト
websockets = []

# SongdoDetailテーブルから曲の詳細情報を取得
async def GetSongData_json(name:str,level:str):
    """
    指定されたNameでSongDetailテーブルを検索し、結果を返すメソッド。
    
    :param name: 検索する曲の名前
    """
    level = level.upper()
    # データベースから曲の詳細情報を取得
    songDetail = get_song_details_from_db(db_path,name)
    if level == "MASTER+":
        level = "MASTER_plus"
    songLevelDetail = get_song_level_details_from_db(db_path,songDetail.__dict__[level])
    # songDetailとsongLevelDetailを辞書に変換してマージ
    songDetail_dict = songDetail.__dict__
    songLevelDetail_dict = songLevelDetail.__dict__
    # バイト型のデータを削除
    songDetail_dict = {key: value for key, value in songDetail_dict.items() if not isinstance(value, bytes)}
    songLevelDetail_dict = {key: value for key, value in songLevelDetail_dict.items() if not isinstance(value, bytes)}
    merged_data = {**songDetail_dict, **songLevelDetail_dict}
    # 新しいキーと値を追加
    if level == "MASTER_plus":
        level = "MASTER+"
    merged_data["SelectedLevel"] = level
    # マージしたデータをJSONファイルとして保存
    await save_merged_data(merged_data,os.path.join(script_dir, 'public','data','songInfo.json'))

async def GetSongRecord_json(name:str,level:str):
    level = level.upper()
    # データベースから曲の詳細情報を取得
    songRecords = get_records_from_db(db_path,name,level)
    # レコード情報を辞書に変換
    songRecords_dict = [record.__dict__ for record in songRecords]
    # マージしたデータをJSONファイルとして保存
    await save_merged_data(songRecords_dict,os.path.join(script_dir, 'public','data','recordInfo.json'))


# 非同期にファイルを書き込む
async def save_merged_data(data,path):
    # ディレクトリが存在しない場合は作成
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # 非同期にファイルを書き込む
    async with aiofiles.open(path, 'w', encoding='utf-8') as f:
        await f.write(json.dumps(data, ensure_ascii=False, indent=4))
        print(f"作成されました：{path}")

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
async def select_song(selection:SongSelection):
    await GetSongData_json(selection.SongName,selection.Level)
    # WebSocket接続にメッセージを送信
    for websocket in websockets:
        await websocket.send_text("select_song")
    await GetSongRecord_json(selection.SongName,selection.Level)

@app.post("/test_select_song")
async def test_select_song():
    selection = SongSelection(SongName="Take me☆Take you",Level="master+")
    await GetSongData_json(selection.SongName,selection.Level)
    # WebSocket接続にメッセージを送信
    for websocket in websockets:
        await websocket.send_text("select_song")
    await GetSongRecord_json(selection.SongName,selection.Level)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)