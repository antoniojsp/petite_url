from app.database import PetiteUrlDatabase
from app.config import Config
import os

db = PetiteUrlDatabase(os.environ['URI'])
my_info = Config().dict()
