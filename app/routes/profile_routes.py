from flask import Blueprint, render_template, session, redirect, url_for
from app.models import user_model, record_model, donation_model

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

@profile_bp.route('/', methods=['GET'])
def index():
    """
    渲染會員中心頁面:
    1. 如果沒有登入狀態，重導向至 /auth/login
    2. 使用 user_id 向資料庫拉取使用者的基本資訊
    3. 拉取歷史占卜列表
    4. 渲染 profile/index.html
    """
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login_page'))
        
    user = user_model.get_by_id(user_id)
    records = record_model.get_by_user_id(user_id)
    donations = donation_model.get_by_user_id(user_id)
    
    total_donation = sum(d['amount'] for d in donations) if donations else 0
    
    return render_template('profile/index.html', 
                           user=user, 
                           divination_records=records, 
                           donation_records=donations,
                           user_total_donation=total_donation)
