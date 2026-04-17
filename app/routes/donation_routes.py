from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import donation_model, user_model

donation_bp = Blueprint('donation', __name__, url_prefix='/donation')

@donation_bp.route('/', methods=['GET'])
def index():
    """渲染添香油錢表單 (donation/index.html)"""
    user = None
    if session.get('user_id'):
        user = user_model.get_by_id(session['user_id'])
    return render_template('donation/index.html', user=user)

@donation_bp.route('/pay', methods=['POST'])
def pay():
    """
    處理模擬金流:
    1. 取得表單金額
    2. 用 donation_model 建立交易紀錄，若有 user_id 也一起綁定
    3. 產生 flash 感謝訊息並導回 /profile 或首頁
    """
    amount = request.form.get('custom_amount')
    if not amount:
        amount = request.form.get('amount')
    
    amount = int(amount) if amount else 100
    user_id = session.get('user_id')
    
    import uuid
    transaction_id = str(uuid.uuid4())
    
    donation_model.create(amount=amount, transaction_id=transaction_id, payment_status='PAID', user_id=user_id)
    
    flash('感謝您的香油錢，神明會保佑您！', 'success')
    if user_id:
        return redirect(url_for('profile.index'))
    return redirect(url_for('main.index'))
