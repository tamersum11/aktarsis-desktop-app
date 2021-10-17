import mysql.connector
from datetime import datetime

aktarsis_db = mysql.connector.connect(
    host = "Your Host Name or IP Address",
    user = "Your User Name",
    password = "Your User Password",
    database = "Your Database"
)

aktarsis_cursor = aktarsis_db.cursor()

def selectOperation(coloumns, table):
    global aktarsis_cursor
    sql = "select " + str(coloumns) + " from " + str(table)
    aktarsis_cursor.execute(sql)
    select_list = aktarsis_cursor.fetchall()

    return select_list

def whereOperation(coloumns, table, search_coloumn, search_term):
    global aktarsis_cursor
    sql = "select " + str(coloumns) + " from " + str(table) + " where " + str(search_coloumn) + " = %s"
    value = (str(search_term), )
    aktarsis_cursor.execute(sql, value)
    select_list = aktarsis_cursor.fetchall()

    return select_list

def insertOperation(table, coloumns, add_items):
    global aktarsis_cursor, aktarsis_db
    s_strings = "%s," * len(add_items)
    sql = "insert into " + str(table) + " " + str(coloumns) + " values " + "(" + str(s_strings[:-1]) + ")"
    value = add_items
    aktarsis_cursor.execute(sql, value)
    aktarsis_db.commit()

def updateOperation(table, update_coloumn, id_coloumn, update_item, id_item):
    global aktarsis_cursor, aktarsis_db
    sql = "update " + str(table) + " set " + str(update_coloumn) + " = %s where " + str(id_coloumn) + " = %s"
    value = (str(update_item), str(id_item))
    aktarsis_cursor.execute(sql, value)
    aktarsis_db.commit()

'''
sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
val = ("John", "Highway 21")
mycursor.execute(sql, val)

mydb.commit()

name = "tamer"
surname = "yaz"
email = "tameryaz98@hotmail.com"
password_1 = "1356"
add_user = (name, surname, email, password_1)
insertOperation("kullanicilar", "(ad, soyad, mail, sifre)", add_user)
'''