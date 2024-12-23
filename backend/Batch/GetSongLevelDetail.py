import sqlite3
import os
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from bs4 import BeautifulSoup

def create_table_if_not_exists(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS SongLevelDetail (
        Level          INTEGER,
        Cost           INTEGER,
        Notes          INTEGER,
        TapIcon        INTEGER,
        LongIcon       INTEGER,
        FlickIcon      INTEGER,
        SlideIcon      INTEGER,
        DamageIcon     INTEGER,
        Density        NUMERIC,
        TapIconRatio   NUMERIC,
        LongIconRatio  NUMERIC,
        FlickIconRatio NUMERIC,
        SlideIconRatio NUMERIC,
        LevelUri       TEXT
    )
    """)

def insert_song_level_detail(conn, level, cost, notes, tap_icon, long_icon, flick_icon, slide_icon, damage_icon, density, tap_icon_ratio, long_icon_ratio, flick_icon_ratio, slide_icon_ratio, level_uri):
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO SongLevelDetail (Level, Cost, Notes, TapIcon, LongIcon, FlickIcon, SlideIcon, DamageIcon, Density, TapIconRatio, LongIconRatio, FlickIconRatio, SlideIconRatio, LevelUri)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (level, cost, notes, tap_icon, long_icon, flick_icon, slide_icon, damage_icon, density, tap_icon_ratio, long_icon_ratio, flick_icon_ratio, slide_icon_ratio, level_uri))
    conn.commit()
    
def fetch_and_parse_html(page,uri, retries=3, wait_time=1):
    for attempt in range(retries):
        try:
            page.goto(uri)
            page.wait_for_load_state('domcontentloaded', timeout=5000)  # タイムアウトを5秒に設定
            html = page.content()
            # BeautifulSoupで解析
            soup = BeautifulSoup(html, 'html.parser')
                
            # スクレイピング対象の情報を取得
            level = soup.select_one("body > div.wiki-contents > div.liquid > div.layout.theme0.btn-default-orange.image-align-bottom > div.main > div.markup.mu > div:nth-child(6) > table > tbody > tr:has(td:contains('楽曲Lv')) td:nth-child(2)").text
            cost = soup.select_one("body > div.wiki-contents > div.liquid > div.layout.theme0.btn-default-orange.image-align-bottom > div.main > div.markup.mu > div:nth-child(6) > table > tbody > tr:has(td:contains('消費スタミナ')) td:nth-child(2)").text
            notes = soup.select_one("body > div.wiki-contents > div.liquid > div.layout.theme0.btn-default-orange.image-align-bottom > div.main > div.markup.mu > div:nth-child(6) > table > tbody > tr:has(td:contains('ノート数')) td:nth-child(2)").text
            density = soup.select_one("body > div.wiki-contents > div.liquid > div.layout.theme0.btn-default-orange.image-align-bottom > div.main > div.markup.mu > div:nth-child(6) > table > tbody > tr:has(td:contains('密度')) td:nth-child(2)").text
            tap_icon = soup.select_one("body > div.wiki-contents > div.liquid > div.layout.theme0.btn-default-orange.image-align-bottom > div.main > div.markup.mu > div:nth-child(6) > table > tbody > tr:has(td:contains('タップアイコン数')) td:nth-child(2)").text
            tap_icon_ratio = soup.select_one("body > div.wiki-contents > div.liquid > div.layout.theme0.btn-default-orange.image-align-bottom > div.main > div.markup.mu > div:nth-child(6) > table > tbody > tr:has(td:contains('タップアイコン比')) td:nth-child(4)").text
            long_icon = soup.select_one("body > div.wiki-contents > div.liquid > div.layout.theme0.btn-default-orange.image-align-bottom > div.main > div.markup.mu > div:nth-child(6) > table > tbody > tr:has(td:contains('ロングアイコン数')) td:nth-child(2)").text
            long_icon_ratio = soup.select_one("body > div.wiki-contents > div.liquid > div.layout.theme0.btn-default-orange.image-align-bottom > div.main > div.markup.mu > div:nth-child(6) > table > tbody > tr:has(td:contains('ロングアイコン比')) td:nth-child(4)").text
            flick_icon = soup.select_one("body > div.wiki-contents > div.liquid > div.layout.theme0.btn-default-orange.image-align-bottom > div.main > div.markup.mu > div:nth-child(6) > table > tbody > tr:has(td:contains('フリックアイコン数')) td:nth-child(2)").text
            flick_icon_ratio = soup.select_one("body > div.wiki-contents > div.liquid > div.layout.theme0.btn-default-orange.image-align-bottom > div.main > div.markup.mu > div:nth-child(6) > table > tbody > tr:has(td:contains('フリックアイコン比')) td:nth-child(4)").text
            slide_icon = soup.select_one("body > div.wiki-contents > div.liquid > div.layout.theme0.btn-default-orange.image-align-bottom > div.main > div.markup.mu > div:nth-child(6) > table > tbody > tr:has(td:contains('スライドアイコン数')) td:nth-child(2)").text
            slide_icon_ratio = soup.select_one("body > div.wiki-contents > div.liquid > div.layout.theme0.btn-default-orange.image-align-bottom > div.main > div.markup.mu > div:nth-child(6) > table > tbody > tr:has(td:contains('スライドアイコン比')) td:nth-child(4)").text
            damage_icon = soup.select_one("body > div.wiki-contents > div.liquid > div.layout.theme0.btn-default-orange.image-align-bottom > div.main > div.markup.mu > div:nth-child(6) > table > tbody > tr:has(td:contains('ダメージアイコン数')) td:nth-child(2)").text
            return level, cost, notes, density, tap_icon, tap_icon_ratio, long_icon, long_icon_ratio, flick_icon, flick_icon_ratio, slide_icon, slide_icon_ratio, damage_icon
        except PlaywrightTimeoutError:
            print(f"Timeout error accessing {uri}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            wait_time += 1
    print(f"Failed to access {uri} after {retries} attempts.")
    return None, None, None, None, None, None, None, None, None, None, None, None, None

def convert_to_numeric(value):
    try:
        return float(value.lower())
    except ValueError:
        return None

def main():
    # データベースファイルのパスを設定
    script_dir = os.path.dirname(__file__)
    db_path = os.path.join(script_dir, '..', '..', 'cinderella.idolmaster.sl-stage.sqlite')

    # データベースに接続
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # テーブルが存在しない場合、テーブルを作成
    create_table_if_not_exists(cursor)

    # SongDetailテーブルからデータを取得
    cursor.execute("SELECT DEBUT, REGULAR, PRO, MASTER, [MASTER+], [レガシーMASTER+], WITCH, PIANO, FORTE, LIGHT, TRICK FROM SongDetail")
    rows = cursor.fetchall()
    
    # Uris配列を初期化
    Uris = []

    # rowsの各タプルを処理
    for row in rows:
        for item in row:
            if item is not None:
                Uris.append(item)

    # Playwrightのブラウザインスタンスを一度だけ作成
    with sync_playwright() as p:
        with p.chromium.launch(headless=True) as browser:  # ヘッドレスモードでブラウザを表示しない
            with browser.new_context() as context:
                page = context.new_page()
                # 各URIにアクセスして情報を取得
                for i, uri in enumerate(Uris):
                    print(f"Processing {uri} ({i + 1}/{len(Uris)})")
                    if uri:  # URIが存在する場合
                        cursor.execute("SELECT Level, SlideIconRatio FROM SongLevelDetail WHERE LevelUri = ?", (uri,))
                        result = cursor.fetchone()
                        if result and all(result):
                            print(f"Skipping {uri} as data already exists.")
                            continue
                        level, cost, notes, density, tap_icon, tap_icon_ratio, long_icon, long_icon_ratio, flick_icon, flick_icon_ratio, slide_icon, slide_icon_ratio, damage_icon = fetch_and_parse_html(page,uri)
                        if level is not None:
                            level = convert_to_numeric(level)
                        if cost is not None:
                            cost = convert_to_numeric(cost)
                        if notes is not None:
                            notes = convert_to_numeric(notes)
                        if density is not None:
                            density = convert_to_numeric(density)
                        if tap_icon is not None:
                            tap_icon = convert_to_numeric(tap_icon)
                        if tap_icon_ratio is not None:
                            tap_icon_ratio = convert_to_numeric(tap_icon_ratio)
                        if long_icon is not None:
                            long_icon = convert_to_numeric(long_icon)
                        if long_icon_ratio is not None:
                            long_icon_ratio = convert_to_numeric(long_icon_ratio)
                        if flick_icon is not None:
                            flick_icon = convert_to_numeric(flick_icon)
                        if flick_icon_ratio is not None:
                            flick_icon_ratio = convert_to_numeric(flick_icon_ratio)
                        if slide_icon is not None:
                            slide_icon = convert_to_numeric(slide_icon)
                        if slide_icon_ratio is not None:
                            slide_icon_ratio = convert_to_numeric(slide_icon_ratio)
                        if damage_icon is not None:
                            damage_icon = convert_to_numeric(damage_icon)
                        insert_song_level_detail(conn, level, cost, notes, tap_icon, long_icon, flick_icon, slide_icon, damage_icon, density, tap_icon_ratio, long_icon_ratio, flick_icon_ratio, slide_icon_ratio, uri)
                        
    # 接続を閉じる
    conn.close()

if __name__ == "__main__":
    main()