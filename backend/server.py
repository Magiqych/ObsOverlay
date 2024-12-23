from dataclasses import dataclass
import datetime
import importlib
import json
import subprocess
import webbrowser
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
from Module.DataManager import DataManager

#region 定数定義
# スクリプト自身のディレクトリを取得
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, '..','..','..',"00.DataStorage","cinderella.idolmaster.sl-stage.sqlite")
# 曲情報を格納する変数
songDetail = None
songLevelDetail = None
songMetaData = None
songRecords = None
# DataManagerのインスタンスを作成
manager = DataManager()
@dataclass(frozen=True)
class State:
    NORMAL: str = 'normal'
    SELECT_SONG: str = 'select_song'
    SHOW_SCORE: str = 'show_score'
    OCR_PROCESSING :str = 'ocr_processing'
#endregion

#region クラス定義
class SongSelection(BaseModel):
    '''
    曲選択情報を格納するクラス
    SongName: str : 曲名
    Level: str : レベル
    '''
    SongName: str
    Level: str
class ScoreData(BaseModel):
    '''
    スコア情報を格納するクラス
    Perfect: str : パーフェクト
    Great: str : グレート
    Nice: str : ナイス
    Bad: str : バッド
    Miss: str : ミス
    Combo: str : コンボ
    Score: str : スコア
    HighScore: str : ハイスコア
    UPRP: str : UPRP
    PRP: str : PRP
    '''
    Perfect:str
    Great:str
    Nice:str
    Bad:str
    Miss:str
    Combo:str
    Score:str
    HighScore:str
    UPRP:str
    PRP:str

class ScoreOCRData(BaseModel):
    '''
    スコアOCR情報を格納するクラス
    RawScore: str : スコアOCRの生データ
    '''
    RawScore:str
#endregion

#region FastAPI設定
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
#endregion

#region 内部処理関数
async def SetSongData_json(name:str,level:str):
    '''
    指定された曲名とレベルに対応する曲の情報をJSONファイルとして保存する関数
    name: str : 曲名
    level: str : レベル
    '''
    level = level.upper()
    # データベースから曲の詳細情報を取得
    songDetail = get_song_details_from_db(db_path,name)
    if not level == "MV":
        if level == "MASTER+":
            level = "MASTER_plus"
        songLevelDetail = get_song_level_details_from_db(db_path,songDetail.__dict__[level])
        if songLevelDetail is None:
            return
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
    else:
        merged_data = {**songDetail.__dict__}
    merged_data["SelectedLevel"] = level
    merged_data["SongImage"] = await GetSongImage(name)
    # マージしたデータをJSONファイルとして保存
    await SaveJsonFileAsync(merged_data,os.path.join(script_dir, 'public','data','songInfo.json'))

async def SetSongRecord_json(name:str,level:str):
    '''
    指定された曲名とレベルに対応する曲のスコア情報をJSONファイルとして保存する関数
    name: str : 曲名
    level: str : レベル
    '''
    level = level.upper()
    # データベースから曲の詳細情報を取得
    songRecords = get_records_from_db(db_path,name,level)
    # レコード情報を辞書に変換
    songRecords_dict = [record.__dict__ for record in songRecords]
    # マージしたデータをJSONファイルとして保存
    await SaveJsonFileAsync(songRecords_dict,os.path.join(script_dir, 'public','data','recordInfo.json'))

async def InsertScoreToRecord(record:Record):
    '''
    Recordテーブルにスコア情報を保存する関数
    record: Record : スコア情報
    '''
    insert_record_into_db(db_path,record)

# 曲の画像を取得
async def GetSongImage(name:str):
    '''
    指定された曲名に対応する画像のファイル名を取得する関数
    name: str : 曲名
    return: str : 画像のファイル名
    '''
    jsonpath = os.path.join(script_dir, 'public','songimage','song_list.json')
    songImageList = await ReadJsonFileAsync(jsonpath)
    for record in songImageList:
        if record['song_name'] == name:
            return 'http://localhost:8000/public/songimage/'+record['file_name']
    return None

# 非同期にファイルを読み込む
async def ReadJsonFileAsync(path):
    '''
    指定されたパスのJSONファイルを非同期に読み込む関数
    path: str : ファイルのパス
    return: Any : 読み込んだデータ
    '''
    try:
        async with aiofiles.open(path, 'r', encoding='utf-8') as f:
            raw_data = await f.read()
            return json.loads(raw_data)
    except Exception as e:
        print(f"エラーが発生しました：{e}")
        return None
    
# 非同期にファイルを書き込む
async def SaveJsonFileAsync(data,path):
    '''
    指定されたデータをJSONファイルとして非同期に保存する関数
    data : Any : 保存するデータ
    path : str : 保存先のファイルパス
    '''
    try:
        # ディレクトリが存在しない場合は作成
        os.makedirs(os.path.dirname(path), exist_ok=True)
        # 非同期にファイルを書き込む
        async with aiofiles.open(path, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(data, ensure_ascii=False, indent=4))
            print(f"作成されました：{path}")
    except Exception as e:
        print(f"エラーが発生しました：{e}")
#endregion

#region APIエンドポイント
# WebSocketエンドポイントを追加
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    '''
    WebSocket接続を処理する関数
    websocket: WebSocket : WebSocketオブジェクト
    '''
    await websocket.accept()
    websockets.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received message: {data}")
    except:
        websockets.remove(websocket)

@app.post("/show_normal")
async def show_normal():
    '''
    通常画面を表示するAPIエンドポイント
    '''
    # WebSocket接続にメッセージを送信
    for websocket in websockets:
        await websocket.send_text(State.NORMAL)

# 曲選択が行われた
@app.post("/select_song")
async def select_song(selection:SongSelection):
    '''
    曲選択が行われたときに呼び出される関数
    selection: SongSelection : 曲選択情報
    '''
    # 選択された曲の情報を設定
    manager.set_song_selection(selection)
    await SetSongData_json(selection.SongName,selection.Level)
    await SetSongRecord_json(selection.SongName,selection.Level)
    # WebSocket接続にメッセージを送信
    for websocket in websockets:
        await websocket.send_text(State.SELECT_SONG)
        
# スコアOCR結果が送信された
@app.post("/set_score")
async def set_score(rawscore:ScoreOCRData):
    '''
    スコアOCR結果が送信されたときに呼び出される関数
    '''
    manager.set_score_ocr_data(rawscore)
    # スコアOCRの生データを分割してRecordオブジェクトに変換
    fieldsValue = rawscore.RawScore.split(',')
    #現在時刻を取得
    now = datetime.datetime.now()
    record = Record(
        Name=manager.song_selection.SongName,
        Level=manager.song_selection.Level,
        Perfect=fieldsValue[0],
        Great=fieldsValue[1],
        Nice=fieldsValue[2],
        Bad=fieldsValue[3],
        Miss=fieldsValue[4],
        Combo=fieldsValue[5],
        Score=fieldsValue[6],
        HighScore=fieldsValue[7],
        UPrp=fieldsValue[8],
        Prp=fieldsValue[9],
        Date=now.strftime('%Y-%m-%d %H:%M:%S')
    )
    # スコア情報を保存
    insert_record_into_db(db_path,record)
    # スコアOCRの生データを分割してScoreDataオブジェクトに変換
    score = ScoreData(
        Perfect=fieldsValue[0],
        Great=fieldsValue[1],
        Nice=fieldsValue[2],
        Bad=fieldsValue[3],
        Miss=fieldsValue[4],
        Combo=fieldsValue[5],
        Score=fieldsValue[6],
        HighScore=fieldsValue[7],
        UPRP=fieldsValue[8],
        PRP=fieldsValue[9]
    )
    # スコア情報を保存
    manager.set_score_data(score)
    scoreDict = {key.upper(): value for key, value in score.__dict__.items()}
    await SaveJsonFileAsync(scoreDict,os.path.join(script_dir, 'public','data','scoreInfo.json'))
    # WebSocket接続にメッセージを送信
    for websocket in websockets:
        await websocket.send_text(State.SHOW_SCORE)

@app.post("/ocr_processing")
async def ocr_processing(rawscore:ScoreOCRData):
    '''
    OCR処理を行うAPIエンドポイント
    '''
    # WebSocket接続にメッセージを送信
    for websocket in websockets:
        await websocket.send_text(State.OCR_PROCESSING)
    
#endregion

#region テスト用APIエンドポイント
# テスト用の通常画面表示が行われた
@app.post("/test_show_normal")
async def test_show_normal():
    '''
    テスト用の通常画面表示が行われたときに呼び出される関数
    '''
    await show_normal()

# テスト用の曲選択が行われた
@app.post("/test_select_song")
async def test_select_song():
    '''
    テスト用の曲選択が行われたときに呼び出される関数
    '''
    selection = SongSelection(SongName="Take me☆Take you",Level="MASTER+")
    await select_song(selection)
    
# テスト用のスコアOCR結果が送信された
@app.post("/test_set_score")
async def test_set_score():
    '''
    テスト用のスコアOCR結果が送信されたときに呼び出される関数
    '''
    selection = SongSelection(SongName="Take me☆Take you",Level="MASTER+")
    await select_song(selection)
    await asyncio.sleep(2)
    scoreData = ScoreOCRData(RawScore="514,14,6,0,5,150,511581,575714,59,831")
    await set_score(scoreData)
#endregion

#region メイン処理
# キャッシュ削除関数
def clear_cache():
    # importlibを使用してモジュールキャッシュをクリア
    importlib.invalidate_caches()
    
    # SQLiteのキャッシュをクリア
    conn = sqlite3.connect(':memory:')
    conn.execute('PRAGMA cache_size = 0')
    conn.close()
    
async def run_subprocess():
    '''
    OCR_CLIを実行する関数
    '''
    env = os.environ.copy()
    env['PROCESS_NAME'] = 'OCR_CLI_Process'
    # OcrCli.pyを実行
    await asyncio.create_subprocess_exec(
        os.path.join(script_dir, '..','..','..','.venv','Scripts','python.exe'),
        '-Xfrozen_modules=off', 
        os.path.join(script_dir, 'OcrCli.py'),
        '--Caller', 'Server.py',
        env=env
    )
async def main():
    await run_subprocess()
    # uvicornを非同期で実行
    config = uvicorn.Config("server:app", host="localhost", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()
# main
if __name__ == "__main__":
    clear_cache()
    asyncio.run(main())
#endregion