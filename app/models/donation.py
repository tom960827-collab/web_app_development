from app.db import get_db_connection

class Donation:
    @staticmethod
    def create(user_id, amount, message):
        """
        新增香油錢捐獻紀錄。
        :param user_id: (int|None) 使用者 ID，無登入則為 None
        :param amount: (int) 捐獻金額
        :param message: (str) 祈福語/留言
        :return: (int) 新增成功後的捐獻 ID
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO donations (user_id, amount, message) VALUES (?, ?, ?)",
                (user_id, amount, message)
            )
            conn.commit()
            donation_id = cursor.lastrowid
            return donation_id
        except Exception as e:
            print(f"Donation.create error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """取得所有香油錢捐獻紀錄。"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM donations")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Donation.get_all error: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_id(donation_id):
        """依據 ID 取得單筆捐獻紀錄。"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM donations WHERE id = ?", (donation_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            print(f"Donation.get_by_id error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_user_id(user_id):
        """取得特定使用者的所有捐獻紀錄，按時間依序排列。"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM donations WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Donation.get_by_user_id error: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def update(donation_id, status):
        """
        修改捐獻紀錄狀態。
        :param donation_id: (int) 訂單 ID
        :param status: (str) 交易狀態，例如 'success' 或 'failed'
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE donations SET status = ? WHERE id = ?",
                (status, donation_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Donation.update error: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(donation_id):
        """刪除單筆捐獻紀錄。"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM donations WHERE id = ?", (donation_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Donation.delete error: {e}")
            return False
        finally:
            conn.close()
