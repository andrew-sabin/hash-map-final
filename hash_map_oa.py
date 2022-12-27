# Name: Andrew Sabin
# OSU Email: sabinand@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6 Hash Tables
# Due Date: 12/2/2022
# Description: Creates a hashmap using both chaining and quadratic probing to place, remove, search, and utilize
#               functions of the hashmap to find the mode of a dynamic array list.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Places the keys and values into the array as a HashEntry object after the key is hashed by the selected hash
        function. If the index has a key different from the original hashed key value it will search for a new
        index by using value of the hashed key + j^2, where j increases by 1 each time an index is not none in the
        while loop.
        If the key exists in the array it will have the value replaced. If the bucket has a tomb_stone value equal true
        it will have its key/value pair replaced.
        When a new value is placed into the hash_table it increases the hash table size by 1.
        @key: key of the pair being placed into the hash table.
        @value: the value of the pair being placed into the table.
        """
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)
        new_entry = HashEntry(key, value)
        j = 0
        curr_key = self._hash_function(key)
        curr_bucket = self._buckets.get_at_index((curr_key + (j ** 2)) % self._capacity)
        while curr_bucket is not None:
            if new_entry.key == curr_bucket.key:
                curr_bucket.value = value
                break
            j += 1
            curr_bucket = self._buckets.get_at_index((curr_key + (j ** 2)) % self._capacity)
        if curr_bucket is None or curr_bucket.is_tombstone is True:
            self._buckets.set_at_index(((curr_key + (j ** 2)) % self._capacity), new_entry)
            self._size += 1

        return None

    def table_load(self) -> float:
        """
        Calculates the table load by grabbing the size of the hash table and dividing it by the capacity of the table
        and then returns it.
        """
        #This method returns the curen thash talbe load factor.
        current_load = self.get_size() / self.get_capacity()
        return current_load

    def empty_buckets(self) -> int:
        """
        Checks to see the number of empty buckets in the array by iterating through the table and counting how many
        indexs have an empty array.
        @return: returns the amount of empty spaces in the array.
        """
        #This method return sthe number of buckets in the hash table.
        buckets_empty = 0
        for i in range (0, self.get_capacity()):
            if self._buckets[i] is None:
                buckets_empty += 1
        return buckets_empty

    def resize_table(self, new_capacity: int) -> None:
        """
        Increases the capacity of the hash table by the new capacity. If the new capacity is smaller or equal
        to the size of the hash map, the amount of items, then the function will return none.
        The new capacity will be set to the nearest prime number. Once the new hash map has been created, the table
        will iterate through the original hash map and rehash each value into the new map.
        Once finished the original hash map will have its capacity and buckets values replaced by the ones from the new
        hash map.
        @new_capacity: the new capacity of the hash map.
        """
        if new_capacity <= self._size:
            return None
        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)
        new_table = HashMap(new_capacity, self._hash_function)
        for i in range(0, self._capacity):
            if self._buckets[i] is not None and self._buckets[i].is_tombstone is False:
                old_key = self._buckets[i].key
                old_val = self._buckets[i].value
                # new_hash = HashEntry(old_key,old_val)
                new_table.put(old_key,old_val)
        self._capacity = new_table._capacity
        self._buckets = new_table._buckets




        return None

    def get(self, key: str) -> object:
        """
        Finds the value of a key looked for in the hash map. If not found in the original index, the value will be
        searched for until either the key is found or the index is empty or a tombstone. If the key has been
        found the value will be returned. If the index is empty or a tombstone it will retur none.
        @key: the key being searched for in the hash map.
        @return: returns either the value of the key/value pair or None.
        """
        #This method returns the value associated with the given key.
        #f the key is not in the hash map, the method returns None.
        j = 0
        curr_key = self._hash_function(key)
        curr_bucket = self._buckets.get_at_index((curr_key + (j ** 2)) % self._capacity)
        while curr_bucket is not None and curr_bucket.key != key:
            j += 1
            curr_bucket = self._buckets.get_at_index((curr_key + (j ** 2)) % self._capacity)
        if curr_bucket is None or curr_bucket.is_tombstone is True:
            return None
        else:
            return curr_bucket.value
        # pass

    def contains_key(self, key: str) -> bool:
        """
        Searches through the index and checks to see if the value is found within the hash map. If it has been found the
        index will return true. Otherwise, the value is returned false.
        @key: the key being searched for in the hash map
        @return: boolean value representing if the key has been found.
        """
        #This method returns True if the given key is in the hash map, otherwise it returns False.
        #An empty hash map does not contain any keys.
        j = 0
        curr_key = self._hash_function(key)
        curr_bucket = self._buckets.get_at_index((curr_key + (j ** 2)) % self._capacity)
        while curr_bucket is not None and curr_bucket.key != key:
            j += 1
            curr_bucket = self._buckets.get_at_index((curr_key + (j ** 2)) % self._capacity)
        if curr_bucket is None or curr_bucket.is_tombstone is True:
            return False
        else:
            return True
        pass

    def remove(self, key: str) -> None:
        """
        Searches for the key in the hash map, where if it has been found the key/value pair has its is_tombstone value
        set to True and the size of the map is decremented by 1. If nothing is found the function returns None.
        @key: the key being looked for in the hash map.
        """
        j = 0
        curr_key = self._hash_function(key)
        curr_bucket = self._buckets.get_at_index((curr_key + (j ** 2)) % self._capacity)
        while curr_bucket is not None and curr_bucket.key != key:
            j += 1
            curr_bucket = self._buckets.get_at_index((curr_key + (j ** 2)) % self._capacity)
        if curr_bucket is not None and curr_bucket.is_tombstone is False:
            self._size -= 1
            curr_bucket.is_tombstone = True
        return None

    def clear(self) -> None:
        """
        Clears the array by creating a new hash map, setting its capacity and hash_function to equal the original hash.
        Then the original hash map buckets are replaced by the new hash map buckets, and the _size value is set back
        to 0.
        """
        #This method clears the contents of the hash map. It does not change the underlying hash table capacity.
        new_hash = HashMap(self._capacity, self._hash_function)
        self._buckets = new_hash._buckets
        self._size = 0

        return None

    def get_keys_and_values(self) -> DynamicArray:
        """
        Iterates through the original array and places all non-tombstone key and value pairs into a dynamic array which
        is returned at the end of iteration.
        @return: key_and_values dynamic array that contains all of the active key/value pairs in the hash map.
        """
        #This method returns a dynamic array where each index contains a tuple of a key/value pair stored in the hash
        #map.
        #
        #The order of the keys in teh dynamic array does not matter.
        keys_and_values = DynamicArray()
        for i in range(0,self._capacity):
            curr_bucket = self._buckets[i]
            if curr_bucket is not None and curr_bucket.is_tombstone is not True:
                keys_and_values.append((self._buckets[i].key,self._buckets[i].value))

        return keys_and_values

    def __iter__(self):
        """
        Sets the index of the iterator the end of the hash map, starting at 0. Returns itself after each iteration.
        """

        self._index = 0
        return self
        # pass

    def __next__(self):
        """
        Iterates through each index of the hash map. If the index is either None or has is_tombstone set to True, the
        iterator will move up to the next index in the hash table.
        @return: returns the key/value pair also known as a combo.
        """
        #This method will return the next item in the hash map, based on the current location of the iterator.
        #Implement this method in a similar way to the example in the Exploration: Encapsulation and Iterators.
        #
        #It will need to only iterate over active items.
        try:
            combo = self._buckets[self._index]
            while combo is None or combo.is_tombstone is True:
                self._index += 1
                combo = self._buckets[self._index]
        except DynamicArrayException:
            raise StopIteration
        self._index += 1
        return combo


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
