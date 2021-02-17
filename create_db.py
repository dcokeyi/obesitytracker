import sqlite3 as sql

# now we establish our connection
conn = sql.connect('history.db')

#create database 'history' database
conn.execute('CREATE TABLE results (date TEXT, name TEXT, gender TEXT,age TEXT,history TEXT, favc TEXT, fcvc TEXT, ncp TEXT, caec TEXT, smoke TEXT, ch2o TEXT, scc TEXT, faf TEXT, tue TEXT, calc TEXT, mtrans TEXT, value TEXT)')  
print("Table created successfully")
conn.close()  # close connection because we will be reconnecting to history



