from flask import Blueprint, render_template, redirect, url_for, session, request

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    HTTP GET
    顯示首頁，包含服務介紹與開始抽籤的入口。
    渲染：index.html
    """
    pass

@main_bp.route('/profile')
def profile():
    """
    HTTP GET
    顯示已登入使用者的個人主頁，包含算命歷史與香油錢紀錄。
    若未登入則重導向至登入頁面(401)。
    渲染：user/profile.html
    """
    pass
