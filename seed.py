from models import db
from app import app

# Create all tables if necessary
db.drop_all()
db.create_all()