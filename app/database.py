import certifi
import datetime
import pymongo
from datetime import timezone, datetime
from random import randrange
import os

SIZE_HASH = int(os.environ['size_hash'])


class PetiteUrlDatabase:
    def __init__(self, uri):
        """
        Connect Mongodb database and select collection
        :param uri: string with the address and password to connect
        """
        client = pymongo.MongoClient(uri, tlsCAFile=certifi.where())
        my_db = client["petiteUrl"]
        self.my_col = my_db["url"]

        # Creates an index just once to make hash_value unique key. If index present, it skips it.
        self.my_col.create_index("hash_value", unique=True)

    def insert(self, url: str, expiration_date: str, custom_hash: str) -> str:
        """
        Inserts the hash_value and the url into the database. It does some validations to check if the
        hash_value is unique

        :param url: address that is going to be stored
        :param expiration_date: if present, it records the date by when the shortened url should expire
        :param custom_hash: if present, personalized the hash_value
        :return: the custom_hash value that has been stored
        """

        mydict = {"hash_value": "",
                  "url_address": url,
                  "time_stamp": datetime.now(timezone.utc),
                  "exp_date": expiration_date,
                  "count": 0}

        url_hash_value = ""
        if custom_hash != "None":
            # revalidates personalized name. JS should check for duplication too.
            if not self.is_hash_duplicated(custom_hash):
                mydict['hash_value'] = custom_hash
                self.my_col.insert_one(mydict)
                print("Custom hash has been recorded")

                return custom_hash
            else:
                raise LookupError("Duplicate: Hash value already in the database")
        else:
            is_random_unique = True
            while is_random_unique:
                # generate hash value and check that its uniqueness (combinations are in the order of 62^7)
                url_hash_value = self.__generate_random_hash()
                mydict['hash_value'] = url_hash_value
                is_random_unique = self.is_hash_duplicated(url_hash_value)

        self.my_col.insert_one(mydict)
        print("Site recorded correctly")

        return url_hash_value

    def is_hash_duplicated(self, hash_value: str) -> bool:
        my_query = {"hash_value": hash_value}
        my_doc = self.my_col.find_one(my_query)
        return False if my_doc is None else True

    def query_url(self, hash_number: str) -> str:
        """
        If the hash value doesn't map to any url, returns a string "Not found",
        if the hash value has an url that has expired, returns "Expired",
        else, returns the url
        :param hash_number: unique hash value that direct to a website
        :return: Not found, Expired, or url
        """
        my_query = {"hash_value": hash_number}
        my_doc = self.my_col.find_one(my_query)

        if my_doc is None or self.__is_page_expired(my_doc['exp_date']):
            return "Not found"

        self.__update_counter(my_doc, my_query)

        return my_doc["url_address"]

    def __update_counter(self, my_doc, my_query:dict):
        new_count = my_doc['count'] + 1
        update_field = {"$set": {"count": new_count}}
        self.my_col.update_one(my_query, update_field)

    @staticmethod
    def __is_page_expired(time: str) -> bool:
        if time == "None":
            return False

        adjusted_time_format = time[:-8]
        pattern_time_format = "%Y-%m-%dT%H:%M"
        current_time = datetime.utcnow()
        expiration_date = datetime.strptime(adjusted_time_format, pattern_time_format)
        return current_time > expiration_date

    @staticmethod
    def __generate_random_hash() -> str:
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




