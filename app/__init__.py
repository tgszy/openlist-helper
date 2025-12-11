from flask import Flask
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建Flask应用
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET', 'openlist-importer-2025-final')

# 支持的网盘
DISK_CONFIGS = {
    'AliyundriveOpen': {'name': '阿里云盘'},
    'AliyundriveShare': {'name': '阿里云盘分享'},
    'Quark': {'name': '夸克网盘'},
    '115 Cloud': {'name': '115网盘'},
    '189Cloud': {'name': '天翼云盘'}
}
SUPPORTED_DRIVERS = list(DISK_CONFIGS.keys())

# 导入路由
from app import routes
