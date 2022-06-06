import certifi
import configparser
import datetime
from utilities import generate_random_hash, expiration_time
import pymongo
import os


class TinyURLDatabase:
    def __init__(self, uri):
        # establish connection to mongodb atlas
        client = pymongo.MongoClient(uri,
                                     tlsCAFile=certifi.where())
        mydb = client["petiteUrl"]
        self.mycol = mydb["url"]

        # Only works if the unique index is not already set.
        self.mycol.create_index("hash_number", unique= True)

    def insert(self, url: str,expiration_date, size_hash:int) -> str:
        url_hash_value = generate_random_hash(size_hash)
        try:
            mydict = {"hash_number": url_hash_value,
                      "url_address": url,
                      "time_stamp": datetime.datetime.now(),
                      "exp_date": expiration_date}
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

        if expiration_time(mydoc['exp_date']):
            print(mydoc['exp_date'])
            return "exp"

        return mydoc["url_address"]



