import logging

# Configure hashtable logging
logger = logging.getLogger(__name__)


class HashTable:
    """
    A class representing a Hash Table
    """

    def __init__(self, load_factor=0.7, bucket_increment=32):
        """
        Initializes a new instance of the HashTable
        """
        self.__count = 0
        self.__increment = bucket_increment
        self.__buckets = [HashTableBucket() for _ in range(self.__increment)]
        self.load_factor = load_factor

    def __iter__(self):
        pairs = [entry for bucket in self.__buckets for entry in bucket.entries]
        return pairs.__iter__()

    def __contains__(self, key):
        bucket = self.__get_bucket(self.__buckets, key)
        return key in bucket

    def __len__(self):
        return self.__count

    def __getitem__(self, key):
        bucket = self.__get_bucket(self.__buckets, key)
        return bucket[key]

    def __setitem__(self, key, value):
        bucket = self.__get_bucket(self.__buckets, key)
        if key in bucket:
            if value is None:
                del bucket[key]
                self.__count -= 1
            else:  # This is a replace
                bucket[key] = value
        elif value is not None:
            bucket[key] = value
            self.__count += 1
            self.__check_load_factor()

    def __delitem__(self, key):
        bucket = self.__get_bucket(self.__buckets, key)
        if key in bucket:
            del bucket[key]
            self.__count -= 1

    @property
    def keys(self):
        return {key for bucket in self.__buckets for key in bucket.keys}

    @property
    def values(self):
        return [value for bucket in self.__buckets for value in bucket.values]

    @staticmethod
    def __get_bucket(buckets, key):
        index = abs(hash(key) % len(buckets))
        logger.debug(f'HashTable bucket index for "{key}" = {index}')
        return buckets[index]

    def __check_load_factor(self):
        max_count = len(self.__buckets) // self.load_factor
        if self.__count > max_count:
            increase = len(self.__buckets) + self.__increment
            logger.info(f'Rehashing buckets from {len(self.__buckets)} to {increase}')
            new_buckets = [HashTableBucket() for _ in range(increase)]
            for old_bucket in self.__buckets:
                for entry in old_bucket.entries:
                    new_bucket = self.__get_bucket(new_buckets, entry[0])
                    new_bucket[entry[0]] = entry[1]
            self.__buckets = new_buckets


class HashTableBucket:
    """
    A class representing a Bucket in the HashTable
    """

    def __init__(self):
        """
        Initializes a new instance of a HashTable Bucket
        """
        self.entries = list()

    def __contains__(self, key):
        index = self.__index_of(key)
        return index is not None

    def __delitem__(self, key):
        index = self.__index_of(key)
        if index is None:
            return
        logger.debug(f'removing value with key: "{key}"')
        self.entries.pop(index)

    def __getitem__(self, key):
        for entry in self.entries:
            if entry[0] == key:
                return entry[1]
        return None

    def __setitem__(self, key, value):
        index = self.__index_of(key)
        if index is None:
            if value is None:
                return
            if len(self.entries) > 0:
                logger.debug(f'collision with key: "{key}" in {self.keys}')
            self.entries.append((key, value))
        else:
            if value is None:
                self.entries.pop(index)
                return
            logger.debug(f'replacing value for key "{key}"')
            self.entries[index] = (key, value)

    @property
    def keys(self):
        return [entry[0] for entry in self.entries]

    @property
    def values(self):
        return [entry[1] for entry in self.entries]

    def __index_of(self, key):
        for index, entry in enumerate(self.entries):
            if entry[0] == key:
                return index
        return None
