from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.donation import Donation

payment_bp = Blueprint('payment', __name__, url_prefix='/payment')

@payment_bp.route('/donate', methods=['GET'])
def donate():
    """
    HTTP GET
    渲染香油錢捐獻表單 (payment/donate.html)。
    """
    return render_template('payment/donate.html')

@payment_bp.route('/process', methods=['POST'])
def process():
    """
    HTTP POST
    接收捐獻表單資料 (amount, message)，模擬付款邏輯，
    成功後 Flash 提示訊息，重導向至首頁。
    """
    amount = request.form.get('amount', type=int)
    message = request.form.get('message', '')
    
    if not amount or amount <= 0:
        flash("請輸入正確的金額", "danger")
        return redirect(url_for('payment.donate'))
        
    user_id = session.get('user_id')
    # 建立捐款紀錄並設定為模擬付款成功 (MVP直接建立)
    success_id = Donation.create(user_id, amount, message)
    if success_id:
        # 修改狀態為 success (目前預設 pending，此處手動觸發 update)
        Donation.update(success_id, 'success')
        
    flash("感謝您的熱心捐款，祝您事事順心！", "success")
    return redirect(url_for('main.index'))
