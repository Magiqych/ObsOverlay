"""
このモジュールは、楽曲のメタデータを表すモデルを提供します。
"""
import ulid
from sqlalchemy import Column, String

from .base import Base


class SongMetaData(Base):
    """
    SongMetaDataクラスは、楽曲のメタデータを表します。
    属性:
        id (str): 楽曲の一意の識別子。デフォルトで新しいULIDが生成されます。
        name (str): 楽曲の名前。
        type (str): 楽曲のタイプ。
        kind (str): 楽曲の種類。
        master_plus (str): "Master+"の難易度。
        witch (str): 楽曲のウィッチ。
        grand (str): 楽曲のグランド。
        smart (str): 楽曲のスマート。
        release_date (str): 楽曲のリリース日。
        memo (str): 楽曲に関するメモ。
        detail_uri (str): 楽曲の詳細情報へのURI。
    """
    __tablename__ = "song_metadata"
    __table_args__ = {"schema": "cinderella.idolmaster.sl-stage"}

    id = Column(String, primary_key=True, default=lambda: ulid.new().str)
    name = Column(String)
    type = Column(String)
    kind = Column(String)
    master_plus = Column("Master+", String)
    witch = Column(String)
    grand = Column(String)
    smart = Column(String)
    release_date = Column(String)
    memo = Column(String)
    detail_uri = Column(String)
