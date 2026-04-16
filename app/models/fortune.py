from app.db import get_db

class Fortune:
    @staticmethod
    def create(category, title, content, interpretation):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO fortunes (category, title, content, interpretation) VALUES (?, ?, ?, ?)",
            (category, title, content, interpretation)
        )
        conn.commit()
        fortune_id = cursor.lastrowid
        conn.close()
        return fortune_id

    @staticmethod
    def get_all():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM fortunes")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(fortune_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM fortunes WHERE id = ?", (fortune_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def get_random(category):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM fortunes WHERE category = ? ORDER BY RANDOM() LIMIT 1", (category,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def update(fortune_id, category, title, content, interpretation):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE fortunes SET category = ?, title = ?, content = ?, interpretation = ? WHERE id = ?",
            (category, title, content, interpretation, fortune_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(fortune_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM fortunes WHERE id = ?", (fortune_id,))
        conn.commit()
        conn.close()
