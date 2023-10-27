
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


