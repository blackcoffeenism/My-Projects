import sqlite3

def data():
    con = sqlite3.connect('vaccination_status.db')
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS vaccination_status(id INTEGER PRIMARY KEY, firstname text, surname text,brgyID integer, vaccination text, drug text)')
    con.commit()
    con.close()

def add_data(firstname, surname,brgyID, vaccination, drug):
    con = sqlite3.connect('vaccination_status.db')
    cur = con.cursor()
    if firstname != "" or surname != "" or vaccination != "" or drug != "":
        cur.execute('INSERT INTO vaccination_status VALUES (NULL,?,?,?,?,?)', (firstname, surname,brgyID, vaccination, drug))
    con.commit()
    con.close()

def search(name):
    con = sqlite3.connect('vaccination_status.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM vaccination_status WHERE firstname like ?", (name,))
    rows = cur.fetchall()
    cur.execute("SELECT * FROM vaccination_status WHERE surname like ?", (name,))
    rows1 = cur.fetchall()
    cur.execute("SELECT * FROM vaccination_status WHERE brgyID like ?", (name,))
    rows2 = cur.fetchall()
    con.close()
    return rows+rows1+rows2

def view_all():
    con = sqlite3.connect('vaccination_status.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM vaccination_status')
    rows = cur.fetchall()
    con.close()
    return rows

def vaccinated_only():
    con = sqlite3.connect('vaccination_status.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM vaccination_status WHERE vaccination == 'Vaccinated'")
    rows = cur.fetchall()
    con.close()
    return rows
def not_vaccinated_only():
    con = sqlite3.connect('vaccination_status.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM vaccination_status WHERE vaccination == 'Not Vaccinated'")
    rows = cur.fetchall()
    con.close()
    return rows

def moderna():
    con = sqlite3.connect('vaccination_status.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM vaccination_status WHERE drug == 'Moderna'")
    rows = cur.fetchall()
    con.close()
    return rows

def pficer():
    con = sqlite3.connect('vaccination_status.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM vaccination_status WHERE drug like 'Pficer'")
    rows = cur.fetchall()
    con.close()
    return rows

def sinovac():
    con = sqlite3.connect('vaccination_status.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM vaccination_status WHERE drug like 'Sinovac'")
    rows = cur.fetchall()
    con.close()
    return rows

def sinopharm():
    con = sqlite3.connect('vaccination_status.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM vaccination_status WHERE drug like 'Sinopharm'")
    rows = cur.fetchall()
    con.close()
    return rows

def aztracenica():
    con = sqlite3.connect('vaccination_status.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM vaccination_status WHERE drug like 'Aztracenica'")
    rows = cur.fetchall()
    con.close()
    return rows

def sputnik():
    con = sqlite3.connect('vaccination_status.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM vaccination_status WHERE drug like 'Sputnik'")
    rows = cur.fetchall()
    con.close()
    return rows

def check(ID):
    con = sqlite3.connect('vaccination_status.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM vaccination_status WHERE brgyID = ?",(ID,))
    rows = cur.fetchall()
    con.close()
    return rows

def update_data(firstname,surname,brgyID,vaccination,drug):
    con = sqlite3.connect('vaccination_status.db')
    cur = con.cursor()
    cur.execute("""UPDATE vaccination_status
        SET firstname = ?,
            surname = ?,
            vaccination = ?,
            drug = ?
            WHERE brgyID = ?""",(firstname,surname,vaccination,drug,brgyID))
    con.commit()
def check_vaccination(ID):
    con = sqlite3.connect('vaccination_status.db')
    cur = con.cursor()
    cur.execute("SELECT vaccination FROM vaccination_status WHERE brgyID = ?",(ID,))
    rows = cur.fetchall()
    con.close()
    return rows
def check_drug(ID):
    con = sqlite3.connect('vaccination_status.db')
    cur = con.cursor()
    cur.execute("SELECT drug FROM vaccination_status WHERE brgyID = ?",(ID,))
    rows = cur.fetchall()
    con.close()
    return rows

def delete_data(ID):
    con = sqlite3.connect('vaccination_status.db')
    cur = con.cursor()
    cur.execute("DELETE FROM vaccination_status WHERE brgyID = ?",(ID,))
    rows = cur.fetchall()
    con.commit()
    con.close()
