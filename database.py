
def creat_table():
    import sqlite3
    conn = sqlite3.connect('mim_bot.db')
    curr = conn.cursor()

    curr.execute("""
    CREATE TABLE IF NOT EXISTS user(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id varchar (255),
        username varchar (255),
        full_name varchar (255)
    )
    """)
    conn.commit()
    conn.close()


async def insert_into(user_id, username, full_name):
    import sqlite3
    conn = sqlite3.connect('mim_bot.db')
    curr = conn.cursor()

    curr.execute("""
    INSERT INTO user (user_id, username, full_name) VALUES (?,?,?)
    
    """, [user_id, username, full_name])
    conn.commit()
    conn.close()


def check_user(user_id):
    import sqlite3
    conn = sqlite3.connect('mim_bot.db')
    curr = conn.cursor()

    user = curr.execute(f"""
    SELECT user_id from user where user_id = {str(user_id)}
    """).fetchone()

    if user is None:
        return False

    elif len(user):
        return True





