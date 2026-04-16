from flask import Blueprint, render_template, session, redirect, url_for, flash
from app.models.user import User
from app.models.fortune_record import FortuneRecord
from app.models.donation import Donation

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    HTTP GET
    顯示首頁，包含服務介紹與開始抽籤的入口。
    渲染：index.html
    """
    return render_template('index.html')

@main_bp.route('/profile')
def profile():
    """
    HTTP GET
    顯示已登入使用者的個人主頁，包含算命歷史與香油錢紀錄。
    若未登入則重導向至登入頁面(401)。
    渲染：user/profile.html
    """
    user_id = session.get('user_id')
    if not user_id:
        flash("請先登入以查看個人紀錄", 'warning')
        return redirect(url_for('auth.login'))
    
    user = User.get_by_id(user_id)
    fortune_records = FortuneRecord.get_by_user_id(user_id)
    donations = Donation.get_by_user_id(user_id)
    
    return render_template('user/profile.html', user=user, fortune_records=fortune_records, donations=donations)
