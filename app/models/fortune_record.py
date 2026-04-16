from app.db import get_db_connection

class FortuneRecord:
    @staticmethod
    def create(user_id, fortune_id):
        """
        新增使用者的抽籤紀錄。
        :param user_id: (int) 參照 users 桌的 ID
        :param fortune_id: (int) 參照 fortunes 桌的 ID
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO fortune_records (user_id, fortune_id) VALUES (?, ?)",
                (user_id, fortune_id)
            )
            conn.commit()
            record_id = cursor.lastrowid
            return record_id
        except Exception as e:
            print(f"FortuneRecord.create error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """取得全部抽籤紀錄。"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM fortune_records")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"FortuneRecord.get_all error: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_id(record_id):
        """使用紀錄 ID 取得該筆抽籤明細。"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM fortune_records WHERE id = ?", (record_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            print(f"FortuneRecord.get_by_id error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_user_id(user_id):
        """
        取得特定使用者的抽籤歷史，並 JOIN 取得抽到的籤詩詳細資料。
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT r.*, f.title, f.content, f.interpretation
                FROM fortune_records r
                JOIN fortunes f ON r.fortune_id = f.id
                WHERE r.user_id = ?
                ORDER BY r.created_at DESC
            ''', (user_id,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"FortuneRecord.get_by_user_id error: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def update(record_id, fortune_id):
        """修改某筆抽籤紀錄的籤詩結果。"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE fortune_records SET fortune_id = ? WHERE id = ?",
                (fortune_id, record_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"FortuneRecord.update error: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(record_id):
        """刪除單一抽籤紀錄。"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM fortune_records WHERE id = ?", (record_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"FortuneRecord.delete error: {e}")
            return False
        finally:
            conn.close()
