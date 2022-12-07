import sqlite3

conn = sqlite3.connect('info.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS data(id INTEGER PRIMARY KEY, name text, gender text, role text, birthday text)')
conn.commit()
conn.close()

def add(name, gender,role, birthday):
    conn = sqlite3.connect('info.db')
    cur = conn.cursor()
    if name != "" or gender != "" or role != "" or birthday != "":
        cur.execute("SELECT * FROM data WHERE name = ?", (name, ))
        data = cur.fetchall()
        print(len(data))
        if len(data)==0:
            cur.execute('INSERT INTO data VALUES (NULL,?,?,?,?)', (name, gender, role, birthday))
        else:
            return
    conn.commit()
    conn.close()
    print('Successfully added')

def get_all():
    conn = sqlite3.connect('info.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM data ORDER BY name ASC')
    data = cur.fetchall()
    conn.commit()
    conn.close()
    return data

def search(name):
    conn = sqlite3.connect('info.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM data WHERE name LIKE '%' || ? || '%' ORDER BY name ASC", (name,))
    data = cur.fetchall()
    conn.commit()
    conn.close()
    return data

def get_gender(gender):
    conn = sqlite3.connect('info.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM data WHERE gender = ? ORDER BY name ASC", (gender,))
    data = cur.fetchall()
    conn.commit()
    conn.close()
    return data


def get_status(pledge):
    conn = sqlite3.connect('info.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM data WHERE role = ? ORDER BY name ASC", (pledge,))
    data = cur.fetchall()
    conn.commit()
    conn.close()
    return data

def delete_item(name):
    conn = sqlite3.connect('info.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM data WHERE name = ?", (name,))
    data = cur.fetchall()
    conn.commit()
    conn.close()

def update(name, gender,role, birthday,ids):
    conn = sqlite3.connect('info.db')
    cur = conn.cursor()
    if name != "" or gender != "" != "" or role != "" or birthday != "":
        cur.execute("""UPDATE data
            SET name = ?,
                gender = ?,
                role = ?,
                birthday = ?
                WHERE id = ?""",(name, gender, role, birthday,ids))
    cur.execute("SELECT * FROM data WHERE id = ?", (ids, ))
    data = cur.fetchall()
    conn.commit()
    conn.close()
    print('Successfully update')
    print(data)

def sel_id(name):
    conn = sqlite3.connect('info.db')
    cur = conn.cursor()
    cur.execute("SELECT id FROM data WHERE name = ?", (name,))
    data = cur.fetchall()
    conn.commit()
    conn.close()
    return data
