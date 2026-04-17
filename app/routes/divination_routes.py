from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import random
from app.models import poem_model, record_model

divination_bp = Blueprint('divination', __name__, url_prefix='/divination')

@divination_bp.route('/', methods=['GET'])
def index():
    """渲染測算大廳頁面 (divination/index.html)"""
    return render_template('divination/index.html')

@divination_bp.route('/draw', methods=['GET'])
def draw():
    """渲染搖籤求籤的操作頁面 (divination/draw.html)"""
    return render_template('divination/draw.html')

@divination_bp.route('/result', methods=['POST', 'GET'])
def result():
    """
    求籤流程結算:
    1. 亂數從 poem_model 中抽出一首籤詩
    2. 若有登入(session)，把籤詩紀錄存進 record_model
    3. 丟資料去渲染結果頁 (divination/result.html)
    """
    poems = poem_model.get_all()
    if not poems:
        poem = {'id': 1, 'type': '大吉', 'content': '海闊天空，一切順利', 'explanation': '此籤大吉，心想事成。'}
    else:
        poem = random.choice(poems)
        
    user_id = session.get('user_id')
    if user_id and request.method == 'POST':
        record_model.create(user_id, poem['id'])
        
    return render_template('divination/result.html', poem=poem)
