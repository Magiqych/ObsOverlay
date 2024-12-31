# backendディレクトリを作成
mkdir backend
cd backend

# appディレクトリとそのサブディレクトリを作成
mkdir app
cd app
mkdir api
mkdir api\endpoints
mkdir core
mkdir models
mkdir schemas
mkdir db

# 空の__init__.pyファイルを作成
New-Item -Path .\__init__.py -ItemType File
New-Item -Path .\api\__init__.py -ItemType File
New-Item -Path .\api\endpoints\__init__.py -ItemType File
New-Item -Path .\core\__init__.py -ItemType File
New-Item -Path .\models\__init__.py -ItemType File
New-Item -Path .\schemas\__init__.py -ItemType File
New-Item -Path .\db\__init__.py -ItemType File

# main.py, config.py, example.py, base.pyファイルを作成
New-Item -Path .\main.py -ItemType File
New-Item -Path .\api\endpoints\example.py -ItemType File
New-Item -Path .\core\config.py -ItemType File
New-Item -Path .\models\example.py -ItemType File
New-Item -Path .\schemas\example.py -ItemType File
New-Item -Path .\db\base.py -ItemType File

# backendディレクトリに戻り、.envファイルを作成
cd ..
New-Item -Path .\.env -ItemType File