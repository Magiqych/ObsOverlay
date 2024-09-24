from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import sqlite3
import os

# スクリプトのディレクトリを取得
script_dir = os.path.dirname(os.path.abspath(__file__))

# SQLiteデータベースの相対パス
db_relative_path = os.path.join(script_dir, '..','..', '00.DataStorage', 'cinderella.idolmaster.sl-stage.sqlite')

# 楽曲メタデータ取得
def get_song_meta_data(url, cursor, conn):
    with sync_playwright() as p:
        with p.chromium.launch(headless=True) as browser:  # ヘッドレスモードでブラウザを表示しない
            with browser.new_context() as context:
                page = context.new_page()
                page.goto(url)

                # ページのHTMLを取得
                html = page.content()
                soup = BeautifulSoup(html, 'html.parser')

                # 最初のtbodyを取得
                first_tbody = soup.find('tbody')
                if first_tbody:
                    rows = first_tbody.find_all('tr')
                    batch_size = 100
                    count = 0
                    for row in rows:
                        cols = row.find_all('td')
                        if len(cols) > 0:
                            # 各列のデータを取得
                            title = cols[0].find('a').get_text().strip()
                            detail_uri = cols[0].find('a')['href']
                            category = cols[1].get_text().strip()
                            kind = cols[2].get_text().strip()
                            m_plus = 1 if cols[3].get_text().strip() == "○" else 2 if cols[3].get_text().strip() == "×" else 0
                            wi = 1 if cols[4].get_text().strip() == "○" else 2 if cols[4].get_text().strip() == "×" else 0
                            gr = 1 if cols[5].get_text().strip() == "○" else 2 if cols[5].get_text().strip() == "×" else 0
                            sm = 1 if cols[6].get_text().strip() == "○" else 2 if cols[6].get_text().strip() == "×" else 0
                            implementation_date = cols[7].get_text().strip()
                            unlock_conditions = cols[8].get_text().strip()

                            # データベースに存在するか確認
                            cursor.execute('''
                            SELECT COUNT(*) FROM SongMetaData WHERE Name = ? AND ReleaseDate = ?
                            ''', (title, implementation_date))
                            exists = cursor.fetchone()[0]

                            if exists == 0:
                                # データベースに挿入
                                cursor.execute('''
                                INSERT INTO SongMetaData (Name, Type, Kind, [Master+], Wicth, Grand, Smart, ReleaseDate, Memo, DetailUri)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                ''', (title, category, kind, m_plus, wi, gr, sm, implementation_date, unlock_conditions, detail_uri))
                                count += 1

                                # バッチサイズごとにコミット
                                if count % batch_size == 0:
                                    conn.commit()

                    # 最後のバッチをコミット
                    conn.commit()

def main():
    # データベースに接続
    with sqlite3.connect(db_relative_path) as conn:
        cursor = conn.cursor()

        # テーブル作成
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS SongMetaData (
            Name TEXT,
            Type TEXT,
            Kind TEXT,
            [Master+] INTEGER,
            Wicth INTEGER,
            Grand INTEGER,
            Smart INTEGER,
            ReleaseDate TEXT,
            Memo TEXT,
            DetailUri TEXT
        )
        ''')

        # 楽曲メタデータを取得してデータベースに挿入
        url = "https://gamerch.com/imascg-slstage-wiki/entry/515998"
        get_song_meta_data(url, cursor, conn)

if __name__ == "__main__":
    main()