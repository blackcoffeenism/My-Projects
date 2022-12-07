import sqlite3

def create_data(): #create database for glass count and date today
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE if not EXISTS data(num int, date text)")
    conn.commit()
    conn.close()

def add(count,date): #Inserting count and date to database
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO data VALUES(:num, :date)",{'num':count,'date':date})
    conn.commit()
    conn.close()

def get_total_today(date): #Getting the total counts of glass of water today
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT num FROM data WHERE date = ?",(date,))
    total = cursor.fetchall()
    conn.commit()
    conn.close()
    overall = 0
    for i in range(len(total)):
        overall += int(total[i][0])
    return overall

def user_data(): #Creating database for name and age
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE if not EXISTS user(name text, age int)")
    conn.commit()
    conn.close()

def insert_user(name, age): #Inserting name and age on database
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user VALUES(:name, :age)",{'name':name,'age':age})
    conn.commit()
    conn.close()

def get_user_age(): #Selecting the age from database
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM user")
    ages = cursor.fetchall()
    conn.commit()
    conn.close()
    return ages
def get_user_name(): #selecting the name of user from database
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM user")
    name = cursor.fetchall()
    if name == []:
        name = "User"
    conn.commit()
    conn.close()
    return str(name[-1][0])
        
    
