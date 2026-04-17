import sqlite3

def get_db_connection():
    """取得資料庫連線"""
    conn = sqlite3.connect('instance/database.db')
    conn.row_factory = sqlite3.Row
    return conn

def create(amount, transaction_id, payment_status, user_id=None):
    """新增一筆香油錢捐獻記錄"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO donations (user_id, amount, transaction_id, payment_status) VALUES (?, ?, ?, ?)",
            (user_id, amount, transaction_id, payment_status)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error creating donation: {e}")
        return None
    finally:
        conn.close()

def get_all():
    """取得所有香油錢捐獻記錄"""
    conn = get_db_connection()
    try:
        donations = conn.execute("SELECT * FROM donations").fetchall()
        return donations
    except sqlite3.Error as e:
        print(f"Error getting all donations: {e}")
        return []
    finally:
        conn.close()

def get_by_id(donation_id):
    """取得單筆香油錢捐獻記錄"""
    conn = get_db_connection()
    try:
        donation = conn.execute("SELECT * FROM donations WHERE id = ?", (donation_id,)).fetchone()
        return donation
    except sqlite3.Error as e:
        print(f"Error getting donation by ID {donation_id}: {e}")
        return None
    finally:
        conn.close()

def update(donation_id, user_id, amount, transaction_id, payment_status):
    """更新香油錢捐獻記錄"""
    conn = get_db_connection()
    try:
        conn.execute(
            "UPDATE donations SET user_id = ?, amount = ?, transaction_id = ?, payment_status = ? WHERE id = ?",
            (user_id, amount, transaction_id, payment_status, donation_id)
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error updating donation {donation_id}: {e}")
        return False
    finally:
        conn.close()

def update_status(transaction_id, payment_status):
    """依據訂單編號更新付款狀態"""
    conn = get_db_connection()
    try:
        conn.execute(
            "UPDATE donations SET payment_status = ? WHERE transaction_id = ?",
            (payment_status, transaction_id)
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error updating donation status for transaction {transaction_id}: {e}")
        return False
    finally:
        conn.close()

def delete(donation_id):
    """刪除香油錢捐獻記錄"""
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM donations WHERE id = ?", (donation_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error deleting donation {donation_id}: {e}")
        return False
    finally:
        conn.close()

def get_by_user_id(user_id):
    """取得特定使用者的香油錢記錄"""
    conn = get_db_connection()
    try:
        donations = conn.execute("SELECT * FROM donations WHERE user_id = ? ORDER BY created_at DESC", (user_id,)).fetchall()
        return donations
    except sqlite3.Error as e:
        print(f"Error getting donations by user_id {user_id}: {e}")
        return []
    finally:
        conn.close()

