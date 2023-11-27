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
    DROP TABLE event, event_cancel
    ''')
db_conn.commit()
db_conn.close()