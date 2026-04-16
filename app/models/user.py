from app.db import get_db_connection

class User:
    @staticmethod
    def create(username, password_hash):
        """
        新增一位使用者記錄。
        :param username: (str) 帳號名稱
        :param password_hash: (str) 雜湊後的密碼
        :return: (int) 新增成功後的使用者 ID，若失敗回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            conn.commit()
            user_id = cursor.lastrowid
            return user_id
        except Exception as e:
            print(f"User.create error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """
        取得所有使用者紀錄。
        :return: (list of dict) 取出的每一列轉為字典
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"User.get_all error: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_id(user_id):
        """
        透過使用者 ID 取得單筆資料。
        :param user_id: (int) 會員 ID
        :return: (dict) 會員資料，找不到則回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            print(f"User.get_by_id error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_username(username):
        """
        透過 username 取得單筆資料 (用於登入與註冊驗證)。
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            print(f"User.get_by_username error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def update(user_id, password_hash):
        """
        更新使用者的密碼。
        :param user_id: (int) 會員 ID
        :param password_hash: (str) 修改後的雜湊密碼
        :return: (bool) 成功與否
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET password_hash = ? WHERE id = ?",
                (password_hash, user_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"User.update error: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(user_id):
        """
        刪除使用者。
        :param user_id: (int) 會員 ID
        :return: (bool) 成功與否
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"User.delete error: {e}")
            return False
        finally:
            conn.close()
