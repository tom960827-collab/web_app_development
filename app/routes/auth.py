from flask import Blueprint, render_template, request, redirect, url_for, flash, session

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    HTTP GET, POST
    GET：渲染註冊表單頁面 (auth/register.html)
    POST：接收表單資料 (username, password)，檢驗是否重複並雜湊密碼存入 DB，成功則導向登入頁。
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    HTTP GET, POST
    GET：渲染登入表單頁面 (auth/login.html)
    POST：接收表單資料，驗證密碼，設定 User Session，成功導向首頁或 /profile。
    """
    pass

@auth_bp.route('/logout')
def logout():
    """
    HTTP GET
    清除目前的 User Session 狀態，重導向至首頁。
    """
    pass
