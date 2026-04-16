from flask import Blueprint, render_template, request, redirect, url_for, flash, session

payment_bp = Blueprint('payment', __name__, url_prefix='/payment')

@payment_bp.route('/donate', methods=['GET'])
def donate():
    """
    HTTP GET
    渲染香油錢捐獻表單 (payment/donate.html)。
    若為登入狀態可自動預填資料。
    """
    pass

@payment_bp.route('/process', methods=['POST'])
def process():
    """
    HTTP POST
    接收捐獻表單資料 (amount, message)，模擬付款邏輯，
    並將狀態 'success' 寫入資料庫的 donations 中。
    成功後 Flash 提示訊息，重導向至首頁。
    """
    pass
