import sqlite3

conn = sqlite3.connect('readings.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE event
          (id INTEGER PRIMARY KEY ASC, 
           event_id INTEGER NOT NULL,
           name VARCHAR(250) NOT NULL,
           venue VARCHAR(250) NOT NULL,
           date VARCHAR(100) NOT NULL,
           duration INTEGER NOT NULL,
           attendees INTEGER NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

c.execute('''
          CREATE TABLE event_cancel
          (id INTEGER PRIMARY KEY ASC, 
           cancel_id INTEGER NOT NULL,
           name VARCHAR(250) NOT NULL,
           venue VARCHAR(250) NOT NULL,
           date VARCHAR(100) NOT NULL,
           reason VARCHAR(250) NOT NULL,
           refund_price FLOAT NOT NULL,
           attendees INTEGER NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

conn.commit()
conn.close()
