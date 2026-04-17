from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    """
    處理首頁請求。
    直接回傳 index.html 讓使用者查看介紹。
    """
    return render_template('index.html')
