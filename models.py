from pony.orm import Database, PrimaryKey, Required, Optional, Set
from datetime import date as Date   

db = Database()

class Event(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    description = Optional(str)
    date = Required(Date)           
    capacity = Required(int)
    registrations = Set('Registration')

class Registration(db.Entity):
    id = PrimaryKey(int, auto=True)
    attendee_name = Required(str)
    attendee_email = Required(str)
    event = Required(Event)

def bind_and_generate(filename='database.sqlite'):
    db.bind(provider='sqlite', filename=filename, create_db=True)
    db.generate_mapping(create_tables=True)
