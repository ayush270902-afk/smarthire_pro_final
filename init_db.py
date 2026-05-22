
import sqlite3
con = sqlite3.connect("database.db")
c = con.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)")
c.execute("INSERT OR IGNORE INTO users VALUES(1,'admin','admin','HR')")
c.execute("INSERT OR IGNORE INTO users VALUES(2,'interviewer','interviewer','Interviewer')")

c.execute("CREATE TABLE IF NOT EXISTS jobs(id INTEGER PRIMARY KEY, title TEXT, dept TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS candidates(id INTEGER PRIMARY KEY, name TEXT, skill TEXT, status TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS interviews(id INTEGER PRIMARY KEY, name TEXT, date TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS offers(id INTEGER PRIMARY KEY, name TEXT, role TEXT, status TEXT)")

con.commit()
con.close()
