import sqlite3

def get_db_connection():
    """取得資料庫連線"""
    conn = sqlite3.connect('instance/database.db')
    conn.row_factory = sqlite3.Row
    return conn

def create(user_id, poem_id):
    """新增一筆占卜記錄"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO records (user_id, poem_id) VALUES (?, ?)",
            (user_id, poem_id)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error creating record: {e}")
        return None
    finally:
        conn.close()

def get_all():
    """取得所有占卜記錄"""
    conn = get_db_connection()
    try:
        records = conn.execute("SELECT * FROM records").fetchall()
        return records
    except sqlite3.Error as e:
        print(f"Error getting all records: {e}")
        return []
    finally:
        conn.close()

def get_by_id(record_id):
    """取得單筆占卜記錄"""
    conn = get_db_connection()
    try:
        record = conn.execute("SELECT * FROM records WHERE id = ?", (record_id,)).fetchone()
        return record
    except sqlite3.Error as e:
        print(f"Error getting record by ID {record_id}: {e}")
        return None
    finally:
        conn.close()

def get_by_user_id(user_id):
    """取得特定使用者的所有占卜紀錄 (並 JOIN poems 表)"""
    conn = get_db_connection()
    try:
        records = conn.execute(
            """
            SELECT r.id, r.created_at, p.poem_number, p.level, p.content 
            FROM records r 
            JOIN poems p ON r.poem_id = p.id 
            WHERE r.user_id = ? 
            ORDER BY r.created_at DESC
            """, 
            (user_id,)
        ).fetchall()
        return records
    except sqlite3.Error as e:
        print(f"Error getting records by user_id {user_id}: {e}")
        return []
    finally:
        conn.close()

def update(record_id, user_id, poem_id):
    """更新占卜記錄 (實務上較少用到)"""
    conn = get_db_connection()
    try:
        conn.execute(
            "UPDATE records SET user_id = ?, poem_id = ? WHERE id = ?",
            (user_id, poem_id, record_id)
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error updating record {record_id}: {e}")
        return False
    finally:
        conn.close()

def delete(record_id):
    """刪除占卜記錄"""
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM records WHERE id = ?", (record_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error deleting record {record_id}: {e}")
        return False
    finally:
        conn.close()
