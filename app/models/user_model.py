import sqlite3

def get_db_connection():
    """取得資料庫連線"""
    conn = sqlite3.connect('instance/database.db')
    conn.row_factory = sqlite3.Row
    return conn

def create(email, password_hash, username):
    """新增一筆使用者記錄"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (email, password_hash, username) VALUES (?, ?, ?)",
            (email, password_hash, username)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error creating user: {e}")
        return None
    finally:
        conn.close()

def get_all():
    """取得所有使用者記錄"""
    conn = get_db_connection()
    try:
        users = conn.execute("SELECT * FROM users").fetchall()
        return users
    except sqlite3.Error as e:
        print(f"Error getting all users: {e}")
        return []
    finally:
        conn.close()

def get_by_id(user_id):
    """取得單筆使用者記錄"""
    conn = get_db_connection()
    try:
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return user
    except sqlite3.Error as e:
        print(f"Error getting user by ID {user_id}: {e}")
        return None
    finally:
        conn.close()

def get_by_email(email):
    """透過 Email 取得單筆使用者記錄"""
    conn = get_db_connection()
    try:
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        return user
    except sqlite3.Error as e:
        print(f"Error getting user by email {email}: {e}")
        return None
    finally:
        conn.close()

def update(user_id, email, password_hash, username):
    """更新使用者記錄"""
    conn = get_db_connection()
    try:
        conn.execute(
            "UPDATE users SET email = ?, password_hash = ?, username = ? WHERE id = ?",
            (email, password_hash, username, user_id)
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error updating user {user_id}: {e}")
        return False
    finally:
        conn.close()

def delete(user_id):
    """刪除使用者記錄"""
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error deleting user {user_id}: {e}")
        return False
    finally:
        conn.close()
