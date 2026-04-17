import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-fallback-secret-key'
    # 設定 SQLite database.db 強制位於 instance 目錄下
    DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'database.db')
