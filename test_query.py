import sqlite3

con = sqlite3.connect('test_database.db')
cur = con.cursor()

cur.execute("INSERT INTO Movie VALUES ('범죄도시2', '범죄', '2022-05-18', 106)")

con.commit()
con.close()
