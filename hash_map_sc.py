# Name: Andrew Sabin
# OSU Email: sabinand@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6 Hash Tables
# Due Date: 12/2/2022
# Description: Creates a hashmap using both chaining and quadratic probing to place, remove, search, and utilize
#               functions of the hashmap to find the mode of a dynamic array list.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)

class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        Places a value and a key in a node within a linked list. To find the specific places in the linked list
        it uses the self._hash_function and hashes the key value, then it finds the value of the hashed key modulo
        divided by the capacity of the hash table where it will place the value in the specific linked list and
        increases the size or amount of items in the table by 1.
        If the value is table load is equal to 1 it increases the capacity of the hash table by 2 times.
        """
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity * 2)
        curr_key = self._hash_function(key)
        curr_bucket = self._buckets.get_at_index(curr_key % self._capacity)
        if curr_bucket.contains(key) is None:
            curr_bucket.insert(key,value)
            self._size += 1
        else:
            curr_bucket.remove(key)
            curr_bucket.insert(key,value)
        return None

    def empty_buckets(self) -> int:
        """
        Checks for the number of empty buckets inside of the hash table by iterating through the buckets and determining
        whether they are empty or not by the length being equal to 0 or not.
        """
        #Returns the number of empty buckets in the hash table.
        num_buckets_empty = 0
        for i in range(0,self._capacity):
            if self._buckets[i].length() == 0:
                num_buckets_empty += 1
        return num_buckets_empty



        pass

    def table_load(self) -> float:
        """
        Gets the current capcacity of the hash table and the current amount of values stored in it or the size.
        We find the value of the load factor by dividing the capacity by the size, where it is returned.
        """
        #Returns the curren hash table load factor.
        curr_cap = self.get_capacity()
        curr_size = self.get_size()
        load_factor = curr_size / curr_cap

        return load_factor

    def clear(self) -> None:
        """
        Clears the original values of the hash table by creating a new hash map and setting the capacity, size, and
        buckets of the original map to the new capacity, size, and buckets of the new map.
        """
        # This method clears the content of the hash map. It does not change the underlying hash table capacity.
        new_hash_map = HashMap(self._capacity, self._hash_function)
        self._capacity = new_hash_map._capacity
        self._buckets = new_hash_map._buckets
        self._size = new_hash_map._size
        return None

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the original table to a new capacity, where the new capacity set is by checking to see if it is a prime
        number and has a load capacity greater than or equal to 1.0. A new hash map is created using the new capacity,
        where the different values of the original hash table are iterated through and rehashed into the new hash map.
        Once finished iterating, the buckets and the capacity of the old hash table are set to the ones of the new
        hash table.
        @new_capacity: the new capacity requested.
        """
        if new_capacity < 1:
            return None
        else:
            if self._is_prime(new_capacity) is False:
                new_capacity = self._next_prime(new_capacity)
            if self._size / new_capacity > 1.0:
                while self._size / new_capacity > 1.0:
                    new_capacity = self._next_prime(new_capacity * 2)
            # previous_table = self._buckets
            previous_cap = self._capacity
            new_hash = HashMap(new_capacity,self._hash_function)
            for i in range (0, previous_cap):
                if self._buckets[i].length() != 0:
                    for node in self._buckets[i]:
                        old_key = node.key
                        old_val = node.value
                        new_hash.put(old_key,old_val)

            self._capacity = new_capacity
            self._buckets = new_hash._buckets

        return None

    def get(self, key: str):
        """
        Finds the key in the hash table by hashing the key value, finding the index of the hashed key modulo divided by
        the capacity, and then if the contains(key) function doesn't return None it returns the value of the found key.
        @key: the key being searched for in the hash table.
        """
        #This method returns the value associated with the given key. If the key is not in the hash map, the method
        #returns none.
        curr_key = self._hash_function(key)
        curr_bucket = self._buckets.get_at_index(curr_key % self._capacity)
        if curr_bucket.length() == 0:
            return None
        else:
            get_node = curr_bucket.contains(key)
            if get_node is not None:
                return get_node.value
            else:
                return None

    def contains_key(self, key: str) -> bool:
        """
        Checks to see if the key is inside of the hash table by finding the index of the linked list the key would be
        stored it, then uses contains() to try and find the value in the linked list. If the value is there it returns
        true, if it doesn't find it there it will return false.
        @key: key being tested whether it is found in the linked list.
        """
        curr_key = self._hash_function(key)
        curr_bucket = self._buckets.get_at_index(curr_key % self._capacity)
        if curr_bucket.length() == 0:
            return False
        else:
            get_node = curr_bucket.contains(key)
            if get_node is None:
                return False
            elif get_node.key == key:
                return True
        return False

    def remove(self, key: str) -> None:
        """
        Searches through the linked list to remove a specific key in the list, where remove() is called and set to
        'removed' variable. If removed is True, the size of the hash table is decreased by 1.
        @key: the key being removed from the list.
        """
        #This method removes the given key and its associated value from the hash map. IF the key is not in the has map,
        #the method does nothing (no exception needs to be raised).
        curr_key = self._hash_function(key)
        curr_bucket = self._buckets.get_at_index(curr_key % self._capacity)
        if curr_bucket.length() == 0:
            return None
        else:
            removed = curr_bucket.remove(key)
            if removed is True:
                self._size -= 1
        return None

    def get_keys_and_values(self) -> DynamicArray:
        """
        Iterates through the hash table to get all the keys and values from each linked list. Each key and value
        pair is put into a tuple and that tuple is appended to the key_n_value dynamic array. After iterating through
        each linked list and putting them into the Dynamic Array, the values are returned in a dynamic array.
        """
        key_n_value = DynamicArray()
        for itr in range(0, self._buckets.length()):
            if self._buckets[itr].length() != 0:
                for node in self._buckets[itr]:
                    key = node.key
                    value = node.value
                    key_n_value.append((key,value))
        #This method returns a dynamic array where each index contains a tuple of a key/value pair stored in the hash
        #map.
        #The orer of keys in the dynamic array does not matter.
        return key_n_value


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Places each value from a dynamic array into a hash map, where the key is the value from the dynamic array and the
    value represents the amount of times the dynamic array value is found in the array.
    Afterwards it then iterates through the hash map and tests to see which key and value pairs match or are larger than
    the current mode and updates the list and current mode to match which is the most frequent item.
    @da: Dynamic Array being looked through.
    @returns: Tuple containing the dynamic array with the most frequent array values and the frequency of those items.
    """
    map = HashMap(da.length(), hash_function_1)
    for itr in range(0, da.length()):
        if map.contains_key(da[itr]) is True:
            map.put(da[itr], map.get(da[itr]) + 1)
        else:
            map.put(da[itr], 1)

    full_list = map.get_keys_and_values()

    frequent_items = DynamicArray()
    current_mode = 0
    for node in range(0, full_list.length()):
        curr_amt = full_list[node][1]
        if curr_amt > current_mode:
            current_mode = curr_amt
            frequent_items = DynamicArray()
            frequent_items.append(full_list[node][0])
        elif current_mode == curr_amt:
            frequent_items.append(full_list[node][0])
    # --Using private variables--
    # for jitr in range(0, map.get_capacity()): # possibly use get_key_and_value() to find each value
    #     if map._buckets[jitr].length() > 0:
    #         for node in map._buckets[jitr]:
    #             if current_mode < node.value:
    #                 current_mode = node.value
    #                 frequent_items = DynamicArray()
    #                 frequent_items.append(node.key)
    #             elif current_mode == node.value:
    #                 frequent_items.append(node.key)
    return (frequent_items,current_mode)






    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap

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
    m = HashMap(53, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
