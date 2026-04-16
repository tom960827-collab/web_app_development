from app.db import get_db_connection

class Fortune:
    @staticmethod
    def create(category, title, content, interpretation):
        """
        新增一張籤詩資料。
        :param category: (str) 籤詩類別 (如: 觀音靈籤)
        :param title: (str) 籤詩標題 (如: 第一籤)
        :param content: (str) 內容
        :param interpretation: (str) 解白
        :return: (int) 新增完畢的 ID
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO fortunes (category, title, content, interpretation) VALUES (?, ?, ?, ?)",
                (category, title, content, interpretation)
            )
            conn.commit()
            fortune_id = cursor.lastrowid
            return fortune_id
        except Exception as e:
            print(f"Fortune.create error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """取得系統中所有的籤詩。"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM fortunes")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Fortune.get_all error: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_id(fortune_id):
        """利用 ID 取得單張籤詩內容。"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM fortunes WHERE id = ?", (fortune_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            print(f"Fortune.get_by_id error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_random(category):
        """從指定 category 中隨機取走一張籤詩。"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM fortunes WHERE category = ? ORDER BY RANDOM() LIMIT 1", (category,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            print(f"Fortune.get_random error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def update(fortune_id, category, title, content, interpretation):
        """更新單一籤詩的各項欄位內容。"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE fortunes SET category = ?, title = ?, content = ?, interpretation = ? WHERE id = ?",
                (category, title, content, interpretation, fortune_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Fortune.update error: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(fortune_id):
        """利用 ID 刪除籤詩。"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM fortunes WHERE id = ?", (fortune_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Fortune.delete error: {e}")
            return False
        finally:
            conn.close()
