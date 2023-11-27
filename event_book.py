from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class Event(Base):
    """ Event """

    __tablename__ = "event"

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, nullable=False)
    name = Column(String(250), nullable=False)
    venue = Column(String(250), nullable=False)
    date = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)
    attendees = Column(Integer, nullable=False)
    trace_id = Column(String(250), nullable=False)

    def __init__(self, event_id, name, venue, date, duration, attendees, trace_id):
        """ Initializes an event booking """
        self.event_id = event_id
        self.name = name
        self.venue = venue
        self.date = date
        self.date_created = datetime.datetime.now()
        self.duration = duration
        self.attendees = attendees
        self.trace_id = trace_id

    def to_dict(self):
        """ Dictionary Representation of an event reading """
        dict = {}
        dict['id'] = self.id
        dict['event_id'] = self.event_id
        dict['name'] = self.name
        dict['venue'] = self.venue
        dict['date'] = self.date
        dict['date_created'] = self.date_created
        dict['duration'] = self.duration
        dict['attendees'] = self.attendees
        dict['trace_id'] = self.trace_id

        return dict
