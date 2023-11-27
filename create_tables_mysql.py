import mysql.connector
import yaml
import os
if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/app_conf.yml"
else:
    print("In Dev Environment")
    app_conf_file = "app_conf.yml"

with open(app_conf_file, 'r') as f:
    app_config = yaml.safe_load(f.read())

db_conn = mysql.connector.connect(
    host=app_config["datastore"]["hostname"], 
    user=app_config["datastore"]["user"],
    password=app_config["datastore"]["password"], 
    database=app_config["datastore"]["db"]
)

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