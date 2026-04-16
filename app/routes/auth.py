from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    HTTP GET, POST
    GET：渲染註冊表單頁面 (auth/register.html)
    POST：接收表單資料，檢驗是否重複並雜湊密碼存入 DB，成功則導向登入頁。
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash("請填寫帳號與密碼", "danger")
            return redirect(url_for('auth.register'))
            
        existing_user = User.get_by_username(username)
        if existing_user:
            flash("此帳號已被註冊", "danger")
            return redirect(url_for('auth.register'))
            
        password_hash = generate_password_hash(password)
        User.create(username, password_hash)
        
        flash("註冊成功！請登入", "success")
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    HTTP GET, POST
    GET：渲染登入表單頁面 (auth/login.html)
    POST：接收表單資料，驗證密碼，設定 User Session。
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.get_by_username(username)
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash("登入成功！", "success")
            return redirect(url_for('main.profile'))
        else:
            flash("帳號或密碼錯誤", "danger")
            
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    """
    清除目前的 User Session 狀態，重導向至首頁。
    """
    session.pop('user_id', None)
    session.pop('username', None)
    flash("已成功登出", "success")
    return redirect(url_for('main.index'))
