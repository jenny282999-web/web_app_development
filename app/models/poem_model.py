import sqlite3

def get_db_connection():
    """取得資料庫連線"""
    conn = sqlite3.connect('instance/database.db')
    conn.row_factory = sqlite3.Row
    return conn

def create(poem_number, level, content, explanation):
    """新增一筆籤詩記錄"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO poems (poem_number, level, content, explanation) VALUES (?, ?, ?, ?)",
            (poem_number, level, content, explanation)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error creating poem: {e}")
        return None
    finally:
        conn.close()

def get_all():
    """取得所有籤詩記錄"""
    conn = get_db_connection()
    try:
        poems = conn.execute("SELECT * FROM poems").fetchall()
        return poems
    except sqlite3.Error as e:
        print(f"Error getting all poems: {e}")
        return []
    finally:
        conn.close()

def get_by_id(poem_id):
    """取得單筆籤詩記錄"""
    conn = get_db_connection()
    try:
        poem = conn.execute("SELECT * FROM poems WHERE id = ?", (poem_id,)).fetchone()
        return poem
    except sqlite3.Error as e:
        print(f"Error getting poem by ID {poem_id}: {e}")
        return None
    finally:
        conn.close()

def update(poem_id, poem_number, level, content, explanation):
    """更新籤詩記錄"""
    conn = get_db_connection()
    try:
        conn.execute(
            "UPDATE poems SET poem_number = ?, level = ?, content = ?, explanation = ? WHERE id = ?",
            (poem_number, level, content, explanation, poem_id)
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error updating poem {poem_id}: {e}")
        return False
    finally:
        conn.close()

def delete(poem_id):
    """刪除籤詩記錄"""
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM poems WHERE id = ?", (poem_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error deleting poem {poem_id}: {e}")
        return False
    finally:
        conn.close()
