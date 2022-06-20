from app.database import PetiteUrlDatabase
import os

db = PetiteUrlDatabase(os.environ['URI'])