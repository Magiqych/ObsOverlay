import sqlite3
import os
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from bs4 import BeautifulSoup
import requests
import time
import re
import random
import asyncio

def create_table_if_not_exists(conn):
    """テーブルが存在しない場合に作成する関数"""
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS SongDetail (
        Name            TEXT,
        Image           BLOB,
        Type            TEXT,
        Length          TEXT,
        BPM             TEXT,
        ReleaseDate     TEXT,
        Credits         TEXT,
        DEBUT           TEXT,
        REGULAR         TEXT,
        PRO             TEXT,
        MASTER          TEXT,
        [MASTER+]       TEXT,
        [レガシーMASTER+] TEXT,
        WITCH           TEXT,
        PIANO           TEXT,
        FORTE           TEXT,
        LIGHT           TEXT,
        TRICK           TEXT
    )
    ''')
    conn.commit()

def get_uris_from_db(db_path):
    """データベースからURIリストを取得する関数"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT DetailUri FROM SongMetaData")
    uris = [row[0] for row in cursor.fetchall()]
    conn.close()
    return uris

def insert_song_detail(conn, song_detail):
    """スクレイピング結果をデータベースに挿入する関数"""
    cursor = conn.cursor()
    
    # 既存のデータをチェック
    cursor.execute("SELECT 1 FROM SongDetail WHERE Name = ?", (song_detail['name'],))
    exists = cursor.fetchone()
    
    if not exists:
        cursor.execute('''
            INSERT INTO SongDetail (Name, Image, Type, Length, BPM, ReleaseDate, Credits, DEBUT, REGULAR, PRO, MASTER, [MASTER+], [レガシーMASTER+], WITCH, PIANO, FORTE, LIGHT, TRICK)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
        ''', (
            song_detail['name'],
            song_detail['image'],
            song_detail['type'],
            song_detail['length'],
            song_detail['bpm'],
            song_detail['release_date'],
            song_detail['credits'],
            song_detail['debut'],
            song_detail['regular'],
            song_detail['pro'],
            song_detail['master'],
            song_detail['master_plus'],
            song_detail['legacy_master_plus'],
            song_detail['witch'],
            song_detail['piano'],
            song_detail['forte'],
            song_detail['light'],
            song_detail['trick']
        ))

async def main():
    # データベースファイルのパスを設定
    script_dir = os.path.dirname(__file__)
    db_path = os.path.join(script_dir, '..', '..', '00.DataStorage', 'cinderella.idolmaster.sl-stage.sqlite')
    
    # データベース接続を確立
    conn = sqlite3.connect(db_path)
    
    # テーブルが存在しない場合は作成
    create_table_if_not_exists(conn)
    
    # データベースからURIリストを取得
    uris = get_uris_from_db(db_path)
    
    # Playwrightのブラウザインスタンスを一度だけ作成
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # 各URIにアクセスしてスクレイピングを実行し、データベースに挿入
        batch_size = 10
        for i, uri in enumerate(uris):
            # SongMetaDataのNameがSongDetailに存在するか確認
            song_name = get_song_name_from_metadata(conn, uri)
            if song_exists_in_db(conn, song_name):
                print(f"Skipped {song_name} as it already exists in the database")
                continue
            
            try:
                song_detail = await scrape_page(page, uri)
                insert_song_detail(conn, song_detail)
                print(f"Inserted data for {song_detail['name']}")
            except PlaywrightTimeoutError:
                print(f"Failed to scrape {uri} after multiple attempts")
                continue
            
            # 1秒待機
            await asyncio.sleep(1)
            
            # バッチサイズごとにコミット
            if (i + 1) % batch_size == 0:
                conn.commit()
                print(f"Committed batch of {batch_size} records")
        
        # 最後のバッチをコミット
        conn.commit()
        print("Committed final batch")
        
        await browser.close()
    
    # データベース接続を閉じる
    conn.close()

async def scrape_page(page, uri):
    max_retries = 1
    headless_mode = True  # 初期設定はheadlessモード
    for attempt in range(max_retries):
        try:
            # page.set_extra_http_headers(get_random_headers())
            await page.goto(uri)
            await page.wait_for_load_state('domcontentloaded', timeout=5000)  # タイムアウトを5秒に設定
            html = await page.content()
            return parse_html(html)
        except PlaywrightTimeoutError:
            print(f"Timeout error on {uri}, retrying {attempt + 1}/{max_retries}")
            await asyncio.sleep(1)
            if attempt == max_retries - 1:
                headless_mode = False  # 最後の試行でheadlessモードをfalseに設定
                async with async_playwright() as p:
                    browser = await p.chromium.launch(headless=headless_mode)
                    page = await browser.new_page()
                    # page.set_extra_http_headers(get_random_headers())
                    await page.goto(uri)
                    input("Press Enter to continue...")  # ユーザー入力を待機
                    html = await page.content()
                    await browser.close()
                    return parse_html(html)
    raise PlaywrightTimeoutError(f"Failed to load {uri} after {max_retries} attempts")
def song_exists_in_db(conn, song_name):
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM SongDetail WHERE name = ?", (song_name,))
    return cursor.fetchone() is not None

def get_song_name_from_metadata(conn, uri):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM SongMetaData WHERE DetailUri = ?", (uri,))
    result = cursor.fetchone()
    return result[0] if result else None

def parse_html(html):
    """HTMLを解析して必要なデータを抽出する関数"""
    soup = BeautifulSoup(html, 'html.parser')
    
    # データを抽出
    name = soup.find('h1', class_='content-head').text.strip()
    image_tag = soup.find('span', class_='mu__img').find('img')
    image_url = image_tag['data-original']
    image_data = requests.get(image_url).content
    type_ = soup.select_one('body > div.wiki-contents > div.liquid > div.layout.theme0.btn-default-orange.image-align-bottom > div.main > div.markup.mu > div:nth-child(3) tbody tr:nth-child(1) td').text.strip()
    length = soup.select_one('body > div.wiki-contents > div.liquid > div.layout.theme0.btn-default-orange.image-align-bottom > div.main > div.markup.mu > div:nth-child(3) tbody tr:nth-child(2) td').text.strip()
    bpm = soup.select_one('body > div.wiki-contents > div.liquid > div.layout.theme0.btn-default-orange.image-align-bottom > div.main > div.markup.mu > div:nth-child(3) tbody tr:nth-child(3) td').text.strip()
    release_date = soup.select_one('body > div.wiki-contents > div.liquid > div.layout.theme0.btn-default-orange.image-align-bottom > div.main > div.markup.mu > div:nth-child(3) tbody tr:nth-child(4) td').text.strip()
    
    # Creditsの処理
    # h3タグのテキストが「楽曲情報」で始まる場合に対応
    h3_tag = soup.find('h3', string=re.compile(r'楽曲情報.*'))
    if h3_tag:
        # 次のh3タグまでのテキストを取得
        next_h3_tag = h3_tag.find_next('h3')
        credits_raw = ""
        for sibling in h3_tag.find_next_siblings():
            if sibling == next_h3_tag:
                break
            credits_raw += sibling.get_text().strip()  # 改行を挿入せずにテキストを取得

        # 改行コードを統一
        credits_raw = credits_raw.replace('\r\n', '\n').replace('\r', '\n')

        # 各行を分割し、フィルタリング
        lines = credits_raw.split('\n')
        filtered_lines = [line for line in lines if line.strip() and "（CV：" not in line]

        # フィルタリングされた行を結合
        credits = "\n".join(filtered_lines).strip()

        if not credits:
            credits = "情報が見つかりませんでした"
    else:
        credits = "情報が見つかりませんでした"
    
    # DEBUT以降の処理
    debut = regular = pro = master = master_plus = legacy_master_plus = witch = piano = forte = light = trick = None
    rows = soup.select('body > div.wiki-contents > div.liquid > div.layout.theme0.btn-default-orange.image-align-bottom > div.main > div.markup.mu > div.mu__wikidb-list > div > table > tbody > tr')
    for row in rows:
        cols = row.find_all('td')
        difficulty = cols[2].text.strip()
        link = cols[0].find('a')['href']
        if difficulty == 'DEBUT':
            debut = link
        elif difficulty == 'REGULAR':
            regular = link
        elif difficulty == 'PRO':
            pro = link
        elif difficulty == 'MASTER':
            master = link
        elif difficulty == 'MASTER+':
            master_plus = link
        elif difficulty == 'ⓁMASTER+':
            legacy_master_plus = link
        elif difficulty == 'WITCH':
            witch = link
        elif difficulty == 'PIANO':
            piano = link
        elif difficulty == 'FORTE':
            forte = link
        elif difficulty == 'LIGHT':
            light = link
        elif difficulty == 'TRICK':
            trick = link
    
    return {
        'name': name,
        'image': image_data,
        'type': type_,
        'length': length,
        'bpm': bpm,
        'release_date': release_date,
        'credits': credits,
        'debut': debut,
        'regular': regular,
        'pro': pro,
        'master': master,
        'master_plus': master_plus,
        'legacy_master_plus': legacy_master_plus,
        'witch': witch,
        'piano': piano,
        'forte': forte,
        'light': light,
        'trick': trick
    }

def get_random_headers():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
    ]

    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept-Language": "ja-JP,ja;q=0.9"
    }
    return headers

if __name__ == "__main__":
    asyncio.run(main())
