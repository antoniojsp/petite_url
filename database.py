import certifi
import configparser
import datetime
from utilities import generate_random_hash
import pymongo

# read credentials for secrets
configurations = configparser.ConfigParser()
configurations.read("credentials.ini")
url_connection_mongodb = configurations['API']['PetiteUrl']
SIZE_HASH = 7


class TinyURLDatabase:
    def __init__(self):
        # establish connection to mongodb atlas
        client = pymongo.MongoClient(url_connection_mongodb, tlsCAFile=certifi.where())
        mydb = client["petiteUrl"]
        self.mycol = mydb["url"]

        # Only works if the unique index is not already set.
        self.mycol.create_index("hash_number", unique= True)

    def insert(self, url: str) -> str:
        url_hash_value = generate_random_hash(SIZE_HASH)
        try:
            mydict = {"hash_number": url_hash_value, "url_address": url, "time_stamp": datetime.datetime.now()}
            self.mycol.insert_one(mydict)
            print("Site recorded correctly")
        except pymongo.errors.DuplicateKeyError as error:
            print(error)

        return url_hash_value

    def query_url(self, hash_number: str) -> str:
        myquery = {"hash_number": hash_number}
        mydoc = self.mycol.find_one(myquery)

        if mydoc is None:
            return ""

        return mydoc["url_address"]



