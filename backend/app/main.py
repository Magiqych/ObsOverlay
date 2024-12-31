"""
このモジュールはFastAPIアプリケーションのエントリーポイントです。
モジュールは以下の機能を提供します:
- FastAPIアプリケーションのインスタンス化
- CORSミドルウェアの設定
- エンドポイントのルーティング設定
エンドポイント:
- GET /: ルートエンドポイント。シンプルなメッセージを返します。
インポート:
- app.api.endpoints.example: エンドポイントのルーターを含むモジュール
- fastapi.FastAPI: FastAPIアプリケーションのクラス
- fastapi.middleware.cors.CORSMiddleware: CORSミドルウェアのクラス
"""
from app.api.endpoints import example
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(example.router, prefix="/api", tags=["example"])


@app.get("/")
def read_root():
    return {"message": "Hello World"}
