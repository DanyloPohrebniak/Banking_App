import sqlite3

import security


con = sqlite3.connect("bank.db")

cur = con.cursor()


def init_db():
    '''Initialize Database'''
    cur.execute("DROP TABLE IF EXISTS customers")

    cur.execute('''CREATE TABLE customers (
                        ID             INTEGER PRIMARY KEY AUTOINCREMENT    NOT NULL,
                        NAME           TEXT UNIQUE                          NOT NULL,
                        BALANCE        REAL                                 NOT NULL,
                        PASSWORD_HASH  TEXT                                 NOT NULL,
                        MFA_CODE       TEXT                                 NOT NULL
                    )''')

    print("Table created successfully")

    users = [
        ('Alisa', 2000, security.hash_password("1234qq"), 123456),
        ('Danya', 5000, security.hash_password("1234qw"), 111111)
    ]

    cur.executemany("INSERT INTO customers (NAME, BALANCE, PASSWORD_HASH, MFA_CODE) VALUES ( ?, ?, ?, ?)", users)


# init_db()

con.commit()
con.close()


def get_db():
    con = sqlite3.connect('bank.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM customers")
    result = cur.fetchall()
    con.close()
    return result


def get_user_by_name(name):
    con = sqlite3.connect('bank.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM customers WHERE NAME = ?", (name,))
    result = cur.fetchone()
    con.close()
    return result


def get_user_balance_by_name(name):
    con = sqlite3.connect('bank.db')
    cur = con.cursor()
    cur.execute("SELECT BALANCE FROM customers WHERE NAME = ?", (name,))
    result = cur.fetchone()
    con.close()
    return result[0] if result else 0.0


def get_user_balance_by_id(id):
    con = sqlite3.connect('bank.db')
    cur = con.cursor()
    cur.execute("SELECT BALANCE FROM customers WHERE ID = ?", (id,))
    result = cur.fetchone()
    con.close()
    return result[0] if result else 0.0


def update_balance(id, new_balance):
    con = sqlite3.connect('bank.db')
    cur = con.cursor()
    cur.execute("UPDATE customers SET BALANCE = ? WHERE ID = ?", (new_balance, id))
    con.commit()
    con.close()


def add_customer(name, password, mfa_code):
    con = sqlite3.connect("bank.db")
    cur = con.cursor()

    try:
        cur.execute("INSERT INTO customers (NAME, BALANCE, PASSWORD_HASH, MFA_CODE) VALUES (?, ?, ?, ?)", 
                    (name, 0.0, password, mfa_code))
        con.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        con.close()
