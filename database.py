import certifi
import datetime
from utilities import generate_random_hash, is_expired
import pymongo
from datetime import timezone


class TinyURLDatabase:
    def __init__(self, uri):
        # establish connection to mongodb atlas and connects to the database
        client = pymongo.MongoClient(uri, tlsCAFile=certifi.where())
        mydb = client["petiteUrl"]
        self.mycol = mydb["url"]

        # Creates an index just one. If index present, it skips it.
        self.mycol.create_index("hash_number", unique= True)

    def insert(self, url: str, expiration_date, size_hash: int) -> str:

        is_unique = False
        url_hash_value = ""
        while not is_unique:
            url_hash_value = generate_random_hash(size_hash)
            try:
                mydict = {"hash_number": url_hash_value,
                          "url_address": url,
                          "time_stamp": datetime.datetime.now(timezone.utc),
                          "exp_date": expiration_date}

                self.mycol.insert_one(mydict)
                print("Site recorded correctly")
                is_unique = True
            except pymongo.errors.DuplicateKeyError as error:
                print(error)

        return url_hash_value

    def query_url(self, hash_number: str) -> str:
        """
        If the hash value doesn't map to any url, returns a string "Not found",
        if the hash value has an url that has expired, returns "Expired",
        else, returns the url
        :param hash_number: unique hash value that direct to a website
        :return: Not found, Expired, or url
        """
        myquery = {"hash_number": hash_number}
        mydoc = self.mycol.find_one(myquery)

        if mydoc is None:
            return "Not found"

        if is_expired(mydoc['exp_date']):
            return "Expired"

        return mydoc["url_address"]

    def check_use(self):
        pass





