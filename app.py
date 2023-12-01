import connexion
from connexion import NoContent
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from event_cancel import EventCancel
from event_book import Event
import json
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread
import mysql.connector
import pymysql
import yaml
import logging
import logging.config
import datetime
from sqlalchemy import and_
import time
import os

if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/app_conf.yml"
    log_conf_file = "/config/log_conf.yml"
else:
    print("In Dev Environment")
    app_conf_file = "app_conf.yml"
    log_conf_file = "log_conf.yml"

with open(app_conf_file, 'r') as f:
    app_config = yaml.safe_load(f.read())

# External Logging Configuration
with open(log_conf_file, 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

logger.info("App Conf File: %s" % app_conf_file)
logger.info("Log Conf File: %s" % log_conf_file)

db_string = "mysql+pymysql://{user}:{password}@{hostname}:{port}/{db}".format(
    user = app_config['datastore']['user'],
    password = app_config['datastore']['password'],
    hostname = app_config['datastore']['hostname'],
    port = app_config['datastore']['port'],
    db = app_config['datastore']['db']
)

DB_ENGINE = create_engine(db_string)
#DB_ENGINE = create_engine("sqlite:///readings.sqlite")
#Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def book(body):
    """ Receives an event booking """

    session = DB_SESSION()

    eb = Event(body['event_id'],
                body['name'],
                body['venue'],
                body['date'],
                body['duration'],
                body['attendees'],
                body['trace_id'])

    session.add(eb)

    session.commit()
    session.close()

    event_name = 'event_book'
    logger.debug(f"Stored event {event_name} with a trace id of {body['trace_id']}")

def cancel(body):
    """ Receives an event cancellation """
    
    session = DB_SESSION()

    ec = EventCancel(body['cancel_id'],
                   body['name'],
                   body['venue'],
                   body['date'],
                   body['refund_price'],
                   body['reason'],
                   body['attendees'],
                   body['trace_id'])

    session.add(ec)

    session.commit()
    session.close()

    event_name = 'event_cancel'
    logger.debug(f"Stored event {event_name} with a trace id of {body['trace_id']}")

def get_bookings(start_timestamp, end_timestamp):
    logger.info(f'Conecting to DB, Hostname:{app_config["datastore"]["hostname"]}, Port:{app_config["datastore"]["port"]}')
    session = DB_SESSION()

    start_timestamp_datetime = datetime.datetime.strptime(start_timestamp, "%Y-%m-%dT%H:%M:%SZ")
    end_timestamp_datetime = datetime.datetime.strptime(end_timestamp, "%Y-%m-%dT%H:%M:%SZ")
    bookings = session.query(Event).filter(Event.date_created >= start_timestamp_datetime, Event.date_created < end_timestamp_datetime)

    res_list = []
    for booking in bookings:
        res_list.append(booking.to_dict())

    session.close()
    logger.info(f'Query for Events between {start_timestamp_datetime} and {end_timestamp_datetime} returns {len(res_list)} results')
    return res_list, 200

def get_cancels(start_timestamp, end_timestamp):
    logger.info(f'Conecting to DB, Hostname:{app_config["datastore"]["hostname"]}, Port:{app_config["datastore"]["port"]}')
    session = DB_SESSION()

    start_timestamp_datetime = datetime.datetime.strptime(start_timestamp, "%Y-%m-%dT%H:%M:%SZ")
    end_timestamp_datetime = datetime.datetime.strptime(end_timestamp, "%Y-%m-%dT%H:%M:%SZ")
    cancels = session.query(EventCancel).filter(EventCancel.date_created >= start_timestamp_datetime, EventCancel.date_created < end_timestamp_datetime)

    res_list = []
    for cancel in cancels:
        res_list.append(cancel.to_dict())

    session.close()
    logger.info(f'Query for Event Cancellations between {start_timestamp_datetime} and {end_timestamp_datetime} returns {len(res_list)} results')
    return res_list, 200

def process_messages():
    logger.info("Demo")
    
    """ Process event messages """
    hostname = "%s:%d" % (app_config["events"]["hostname"],
    app_config["events"]["port"])
    for curr_retry in range(app_config["events"]["max_retry"]):
        try:
            logger.info(f'Attempting to connect to Kafka, retry count: {curr_retry}')
            client = KafkaClient(hosts=hostname)
            topic = client.topics[str.encode(app_config["events"]["topic"])]
            break
        except Exception as e:
            logger.error(f'Kafka connection failed: {str(e)}')
            time.sleep(app_config["events"]["sleep_time"])
    else:
        logger.error(f'Failed to connect to Kafka after {app_config["events"]["max_retry"]} retries')
    # Create a consume on a consumer group, that only reads new messages
    # (uncommitted messages) when the service re-starts (i.e., it doesn't
    # read all the old messages from the history in the message queue).
    consumer = topic.get_simple_consumer(consumer_group=b'event_group',
                                         reset_offset_on_start=False,
                                         auto_offset_reset=OffsetType.LATEST)
    # This is blocking - it will wait for a new message
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info("Message: %s" % msg)
        payload = msg["payload"]
        if msg["type"] == "Event": # Change this to your event type
            # Store the event1 (i.e., the payload) to the DB
            logger.debug(f'Payload: {payload}')
            book(payload)
        elif msg["type"] == "EventCancel": # Change this to your event type
            # Store the event2 (i.e., the payload) to the DB
            logger.debug(f'Payload: {payload}')
            cancel(payload)
        # Commit the new message as being read
        consumer.commit_offsets()

def health():
    return 200

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api(
    "openapi.yml",
    base_path="/storage",
    strict_validation=True,
    validate_responses=True
)

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    print("hello world")
    app.run(port=8090)
