from app.db import get_db

class Donation:
    @staticmethod
    def create(user_id, amount, message):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO donations (user_id, amount, message) VALUES (?, ?, ?)",
            (user_id, amount, message)
        )
        conn.commit()
        donation_id = cursor.lastrowid
        conn.close()
        return donation_id

    @staticmethod
    def get_all():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM donations")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(donation_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM donations WHERE id = ?", (donation_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def get_by_user_id(user_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM donations WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def update(donation_id, status):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE donations SET status = ? WHERE id = ?",
            (status, donation_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(donation_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM donations WHERE id = ?", (donation_id,))
        conn.commit()
        conn.close()
