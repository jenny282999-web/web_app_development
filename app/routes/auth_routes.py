from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import user_model

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET'])
def register_page():
    """渲染註冊頁面 (auth/register.html)"""
    return render_template('auth/register.html')

@auth_bp.route('/register', methods=['POST'])
def handle_register():
    """
    接收註冊表單:
    1. 驗證欄位是否空白
    2. 將密碼做 Hash 加密
    3. 存入 db (使用 user_model.create)
    4. 成功後 redirect 到登入頁
    """
    email = request.form.get('email')
    password = request.form.get('password')
    username = request.form.get('username')

    if not email or not password or not username:
        flash('請填寫所有必填欄位', 'error')
        return redirect(url_for('auth.register_page'))

    # 檢查 email 是否已存在 (這裡先查詢一下)
    existing_user = user_model.get_by_email(email)
    if existing_user:
        flash('Email 已經被註冊過！', 'error')
        return redirect(url_for('auth.register_page'))

    password_hash = generate_password_hash(password)
    user_id = user_model.create(email, password_hash, username)

    if user_id:
        flash('註冊成功！請登入', 'success')
        return redirect(url_for('auth.login_page'))
    else:
        flash('註冊失敗，系統發生錯誤', 'error')
        return redirect(url_for('auth.register_page'))

@auth_bp.route('/login', methods=['GET'])
def login_page():
    """渲染登入頁面 (auth/login.html)"""
    return render_template('auth/login.html')

@auth_bp.route('/login', methods=['POST'])
def handle_login():
    """
    接收登入表單:
    1. 從 db 取出對應 email 帳號
    2. 比對 Hash 密碼
    3. 若成功將 user_id 寫進 session 並 redirect('/profile')
    4. 若失敗閃退 flash 錯誤並回登入頁
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        flash('信箱與密碼欄位不能為空', 'error')
        return redirect(url_for('auth.login_page'))

    user = user_model.get_by_email(email)

    if user and check_password_hash(user['password_hash'], password):
        session['user_id'] = user['id']
        session['username'] = user['username']
        flash('登入成功！歡迎回來', 'success')
        return redirect(url_for('profile.profile_page'))
    else:
        flash('信箱或密碼錯誤', 'error')
        return redirect(url_for('auth.login_page'))

@auth_bp.route('/logout', methods=['GET'])
def handle_logout():
    """
    清除 session 裡的登入資料，導向到首頁。
    """
    session.clear()
    flash('您已經成功登出', 'success')
    return redirect(url_for('main.index'))
