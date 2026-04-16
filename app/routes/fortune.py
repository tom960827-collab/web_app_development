from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.fortune import Fortune
from app.models.fortune_record import FortuneRecord

fortune_bp = Blueprint('fortune', __name__, url_prefix='/fortune')

@fortune_bp.route('/draw', methods=['GET', 'POST'])
def draw():
    """
    HTTP GET, POST
    GET：渲染準備抽籤的頁面 (fortune/draw.html)
    POST：根據類別隨機抽出籤詩。若有登入則記錄在 DB，然後導向到結果頁。
    """
    if request.method == 'POST':
        category = request.form.get('category', '觀音靈籤')
        result_fortune = Fortune.get_random(category)
        
        if not result_fortune:
            flash("目前圖庫中沒有可用的籤詩", "warning")
            return redirect(url_for('fortune.draw'))
            
        # 若已登入，存入歷史紀錄
        user_id = session.get('user_id')
        if user_id:
            FortuneRecord.create(user_id, result_fortune['id'])
            
        return redirect(url_for('fortune.result', id=result_fortune['id']))
        
    return render_template('fortune/draw.html')

@fortune_bp.route('/result/<int:id>')
def result(id):
    """
    HTTP GET
    根據 ID 取得單筆抽籤結果。
    如果找不到該籤詩則回傳 404 表單
    """
    fortune_data = Fortune.get_by_id(id)
    if not fortune_data:
        return "找不到該籤詩", 404
        
    return render_template('fortune/result.html', fortune=fortune_data)
