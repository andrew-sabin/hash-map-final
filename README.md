# hash-map-final
Created Two Hashmaps, where one utilizes Open Addressing while the other utilizes Chaining. Assisted with professor Randy Scovil's help.

## a6_include
Provides the necessary DynamicArray, SLNode, Linked List, Linked List Iterator, and Hash Entry classes required for both the Open Addressing and Chaining hashmaps.

Also provides the necessary hash functions. Where the hash_function1 gives us the total unicode value of all the letters made of the string put into the hash function.
Hash function 2 takes the index of a letter and multiplies it by the unicode of the letter, adding it to the total value of the hash.


## Open Addressing (hash_map_oa)
Open Addressing uses just a DynamicArray with the hashmap, where in the case of collisions we use different slots to store different values stored in the array. 

Each value will be placed into the array based on the hash functions provided in the a6_include. If the index has been filled, the put() function will continue to find a space that has either not been filled or has a tomb_stone value set.

Delete() function will turn the specific key into a tomb_stone object within the index of where the key value was located in the array.

The array will resize itself to double its initial size after checking to see if the amount of values stored in the array divided by the size of the array is larger than 0.5.

Open Addressing also contains an iterator and next private function so that the program can iterate through the hashmap.

## Chaining (hash_map_sc)
Chaining uses linked lists in a combination of an array to keep track of different values being placed in the dynamic array. With each value being placed into the dynamic array, they are then also added to the head of the linked list.

Deleting a value from the hashmap will result in the value's next item being connected to the previous item within the linked list.

Similar to the Open Addressing hashmap, the array will be resized depending on if the number of items in the array divided by the amount of items is larger than 0.5.

The Chaining hashmap also has a get mode function, where it creates a separate hash map that contains each value and how many times it was found in the initial hashmap. Then it iterates through the new hash map to find the mode value, or the most frequent value of a chaining hashmap.

## Further reading
To understand both hashmap types, please look at the comments above each function when clicking on them. Will provide figures and videos to explain how each hashmap functions.
