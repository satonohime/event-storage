import mysql.connector
db_conn = mysql.connector.connect(host="vm1-3855-a01031389.westus.cloudapp.azure.com", user="user",
password="password", database="events")
db_cursor = db_conn.cursor()
db_cursor.execute('''
    DROP TABLE event, event_cancel
    ''')
db_conn.commit()
db_conn.close()