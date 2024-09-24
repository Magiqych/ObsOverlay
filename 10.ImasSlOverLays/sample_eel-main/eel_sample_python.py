# Python Version: 3.8
import base64
import os
import platform
import random
import sys
import time
import eel
import threading  # threadingモジュールをインポート
from database import search_song_by_name  # search_song_by_nameメソッドをインポート


# Use latest version of Eel from parent directory
sys.path.insert(1, '../../')

@eel.expose  # Expose function to JavaScript
def say_hello_py(x):
    """Print message from JavaScript on app initialization, then call a JS function."""
    print('Hello from %s' % x)  # noqa T001
    eel.say_hello_js('Python {from within say_hello_py()}!')


@eel.expose
def expand_user(folder):
    """Return the full path to display in the UI."""
    return '{}/*'.format(os.path.expanduser(folder))


@eel.expose
def pick_file(folder):
    """Return a random file from the specified folder."""
    folder = os.path.expanduser(folder)
    if os.path.isdir(folder):
        listFiles = [_f for _f in os.listdir(folder) if not os.path.isdir(os.path.join(folder, _f))]
        if len(listFiles) == 0:
            return 'No Files found in {}'.format(folder)
        return random.choice(listFiles)
    else:
        return '{} is not a valid folder'.format(folder)

@eel.expose
def receive_message(messagebody):
    print("Received message:", messagebody)

def start_eel(develop):
    if True:
        directory = 'src'
        app = None
        page = {'port': 3000}
    else:
        directory = 'build'
        app = 'chrome-app'
        page = 'index.html'
    #eel.init(directory, ['.tsx', '.ts', '.jsx', '.js', '.html'])
    eel.init(directory, allowed_extensions=['.tsx', '.ts', '.jsx', '.js', '.html', '.css', '.json', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.woff', '.woff2', '.ttf', '.eot'])

    eel_kwargs = dict(
        host='localhost',
        port=8080,
        size=(1280, 800),
    )
    try:
        eel.start(page, app=None, **eel_kwargs, block=False)
        eel.sleep(3)
    except EnvironmentError:
        raise

    while True:
        try:
            message = search_song_by_name("とどけ！アイドル")
        except Exception as e:
            message = str(e)
        
        if message and len(message) > 0:
            # 画像データをBase64エンコード
            image_data = message[0][1]  # 画像のバイナリデータを取得
            encoded_string = base64.b64encode(image_data).decode('utf-8')
            
            messagebody = {
                'name': message[0][0],
                'image': f"data:image/png;base64,{encoded_string}"
            }
            eel.receive_message(messagebody)  # JavaScript関数を呼び出してメッセージを送信
        time.sleep(100000)

if __name__ == '__main__':
    import sys
    start_eel(develop=len(sys.argv) == 2)