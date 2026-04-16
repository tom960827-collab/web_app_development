from flask import Blueprint, render_template, request, redirect, url_for, session

fortune_bp = Blueprint('fortune', __name__, url_prefix='/fortune')

@fortune_bp.route('/draw', methods=['GET', 'POST'])
def draw():
    """
    HTTP GET, POST
    GET：渲染準備抽籤的頁面 (fortune/draw.html)
    POST：根據類別隨機抽出籤詩。若有登入則記錄在 DB，然後導向到該次抽出的籤詩結果頁。
    """
    pass

@fortune_bp.route('/result/<int:id>')
def result(id):
    """
    HTTP GET
    根據 ID 取得單筆抽籤結果。
    渲染：fortune/result.html
    如果找不到該籤詩則回傳 404。
    """
    pass
