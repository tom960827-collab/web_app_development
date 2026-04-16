from app.db import get_db

class FortuneRecord:
    @staticmethod
    def create(user_id, fortune_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO fortune_records (user_id, fortune_id) VALUES (?, ?)",
            (user_id, fortune_id)
        )
        conn.commit()
        record_id = cursor.lastrowid
        conn.close()
        return record_id

    @staticmethod
    def get_all():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM fortune_records")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(record_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM fortune_records WHERE id = ?", (record_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def get_by_user_id(user_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT r.*, f.title, f.content, f.interpretation
            FROM fortune_records r
            JOIN fortunes f ON r.fortune_id = f.id
            WHERE r.user_id = ?
            ORDER BY r.created_at DESC
        ''', (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def update(record_id, fortune_id):
        conn = get_db()
        cursor = conn.cursor()
        # 實務上很少修改抽籤紀錄，但為符合 CRUD 規範仍實作
        cursor.execute(
            "UPDATE fortune_records SET fortune_id = ? WHERE id = ?",
            (fortune_id, record_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(record_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM fortune_records WHERE id = ?", (record_id,))
        conn.commit()
        conn.close()
