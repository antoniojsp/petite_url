import certifi
import datetime
import pymongo
from datetime import timezone, datetime
from random import randrange
import os

SIZE_HASH = int(os.environ['size_hash'])


class TinyURLDatabase:
    def __init__(self, uri):
        # establish connection to mongodb atlas and connects to the database
        client = pymongo.MongoClient(uri, tlsCAFile=certifi.where())
        mydb = client["petiteUrl"]
        self.mycol = mydb["url"]

        # Creates an index just one. If index present, it skips it.
        self.mycol.create_index("hash_number", unique= True)

    def insert(self, url: str, expiration_date: str, per_name: str) -> str:
        is_unique = False
        url_hash_value = ""
        # while not is_unique:
        if per_name != "None":
            if not self.check_name(per_name):
                url_hash_value = per_name
            else:
                print("Duplicado")
                return ""
        else:
            while True:
                url_hash_value = self.generate_random_hash()
                if not self.check_name(url_hash_value):
                    break

        mydict = {"hash_number": url_hash_value,
                  "url_address": url,
                  "time_stamp": datetime.now(timezone.utc),
                  "exp_date": expiration_date}

        self.mycol.insert_one(mydict)
        print("Site recorded correctly")


            # except pymongo.errors.DuplicateKeyError as error:
            #     print(error)
            #     break

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

        if self.is_expired(mydoc['exp_date']):
            return "Expired"

        return mydoc["url_address"]

    def check_name(self, hash_number):
        myquery = {"hash_number": hash_number}
        mydoc = self.mycol.find_one(myquery)
        return False if mydoc is None else True

    @staticmethod
    def is_expired(time: str) -> bool:
        if time == "None":
            return False

        adjusted_time_format = time[:-8]
        pattern_time_format = "%Y-%m-%dT%H:%M"
        current_time = datetime.utcnow()
        expiration_date = datetime.strptime(adjusted_time_format, pattern_time_format)
        return current_time > expiration_date

    @staticmethod
    def generate_random_hash() -> str:
        """
        Number of combinations is 62**size
        i.e. if size is 6 then there are combinations 56,800,235,584
        i.e. if size is 7 then there are 3,521,614,606,208 combinations
        """
        hash_result = []
        alphanumeric = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

        for hash_char_position in range(0, SIZE_HASH):
            random_char = randrange(0, 62)
            hash_result.append(alphanumeric[random_char])

        return "".join(hash_result)





