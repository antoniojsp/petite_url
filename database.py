import certifi
import configparser
import datetime
from hash import hash_url
import pymongo
import urllib.request

configurations = configparser.ConfigParser()
configurations.read("credentials.ini")
secret_word = configurations['API']['mundo']


class TinyURLDatabase:
    def __init__(self):
        client = pymongo.MongoClient(f"mongodb+srv://petiteurl:{secret_word}@cluster0.1ra6dk3.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
        mydb = client["tinyurl"]
        self.mycol = mydb["url"]

        # Only works if the unique index is not already set.
        self.mycol.create_index("hash_number", unique= True)

    def insert(self, url: str) -> str:
        response = ""
        url_hash = hash_url(url)
        try:
            self._check_url_alive(url)
            mydict = {"hash_number": url_hash, "url_address": url, "time_stamp": datetime.datetime.now()}
            self.mycol.insert_one(mydict)
            response = f'{url_hash}'
        except pymongo.errors.DuplicateKeyError:
            print("Entry already in database")
            response = f'{url_hash}'
        except urllib.error.HTTPError:
            print("Website dead")
            response = "404"

        return response

    def query_url(self, hash_number: str) -> str:
        myquery = {"hash_number": hash_number}
        mydoc = self.mycol.find_one(myquery)

        if mydoc is None:
            return ""

        return mydoc["url_address"]

    def _check_url_alive(self, url) -> bool:
        return urllib.request.urlopen(url).getcode() == 200
