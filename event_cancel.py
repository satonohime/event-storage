from sqlalchemy import Column, Integer, Float, String, DateTime
from base import Base
import datetime


class EventCancel(Base):
    """ Event Cancel """

    __tablename__ = "event_cancel"

    id = Column(Integer, primary_key=True)
    cancel_id = Column(Integer, nullable=False)
    name = Column(String(250), nullable=False)
    venue = Column(String(250), nullable=False)
    date = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)
    reason = Column(String(250), nullable=False)
    refund_price = Column(Float, nullable=False)
    attendees = Column(Integer, nullable=False)
    trace_id = Column(String(250), nullable=False)

    def __init__(self, cancel_id, name, venue, date, refund_price, reason, attendees, trace_id):
        """ Initializes an event cancellation """
        self.cancel_id = cancel_id
        self.name = name
        self.venue = venue
        self.date = date
        self.date_created = datetime.datetime.now()
        self.reason = reason
        self.refund_price = refund_price
        self.attendees = attendees
        self.trace_id = trace_id

    def to_dict(self):
        """ Dictionary Representation of an event cancellation """
        dict = {}
        dict['id'] = self.id
        dict['cancel_id'] = self.cancel_id
        dict['name'] = self.name
        dict['venue'] = self.venue
        dict['date'] = self.date
        dict['date_created'] = self.date_created
        dict['reason'] = self.reason
        dict['refund_price'] = self.refund_price
        dict['attendees'] = self.attendees
        dict['trace_id'] = self.trace_id

        return dict
