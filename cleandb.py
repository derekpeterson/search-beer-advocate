import re
import sqlite3 as sqlite

# Just a script for cleaning up the data in reviews.db. Specifically, it:
# - adds an auto-incrementing primary key id column
# - removes pesky punctuation from the names and reviews
# - loads the cleaned data into a new database

reviewsconn = sqlite.connect('raw.db')
c = reviewsconn.cursor()
c.execute("select * from reviews")
reviews = c.fetchall()
reviewsconn.close()

cleanconn = sqlite.connect('reviews.db')
c = cleanconn.cursor()
c.execute("DROP TABLE IF EXISTS reviews")
c.execute("""
	CREATE TABLE reviews(
		name TEXT,
		url TEXT,
		score REAL,
		reviewtext TEXT,
		id INTEGER PRIMARY KEY AUTOINCREMENT
	)
	""")
offending = re.compile(r'[\(\)\'\"\`]')
for rev in reviews:
	insert = (offending.sub('', rev[0]), rev[1], rev[2], offending.sub('', rev[3]), None)
	c.execute("INSERT INTO reviews VALUES (?,?,?,?,?)", insert)

cleanconn.commit()
cleanconn.close()
