import mysql.connector
db_conn = mysql.connector.connect(host="vm1-3855-a01031389.westus.cloudapp.azure.com", user="user",
password="password", database="events")
db_cursor = db_conn.cursor()
db_cursor.execute('''
    CREATE TABLE event
    (id INT NOT NULL AUTO_INCREMENT, 
     event_id INT NOT NULL,
     name VARCHAR(250) NOT NULL,
     venue VARCHAR(250) NOT NULL,
     date VARCHAR(100) NOT NULL,
     duration INT NOT NULL,
     attendees INT NOT NULL,
     date_created VARCHAR(100) NOT NULL,
     trace_id VARCHAR(250) NOT NULL,
     CONSTRAINT event_book_pk PRIMARY KEY (id))
    ''')
db_cursor.execute('''
    CREATE TABLE event_cancel
    (id INT NOT NULL AUTO_INCREMENT, 
     cancel_id INT NOT NULL,
     name VARCHAR(250) NOT NULL,
     venue VARCHAR(250) NOT NULL,
     date VARCHAR(100) NOT NULL,
     reason VARCHAR(250) NOT NULL,
     refund_price FLOAT NOT NULL,
     attendees INT NOT NULL,
     date_created VARCHAR(100) NOT NULL,
     trace_id VARCHAR(250) NOT NULL,
     CONSTRAINT event_cancel_pk PRIMARY KEY (id))
    ''')
db_conn.commit()
db_conn.close()