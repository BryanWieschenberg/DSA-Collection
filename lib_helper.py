# range(start, stop, step)
print(list(range(0, 10, 2))) # range(0, 10, 2)

# --- STRINGS ---

# ord() -> Convert char to ASCII, good for normalizing a-z to 0-25
print(ord('a')) # 97
print(ord('l') - ord('a')) # 11

# s.count(x) -> count occurrences of substring/char in O(n)
s = "hello"
print(s.count('l')) # 2

# s.split() -> parsing & recombining strings
s = "hello world"
print(s.split()) # ['hello', 'world']
print(s.split('o')) # ['hell', ' w', 'rld']

# s.join(list) -> recombine list of strings in O(n).
print(' '.join(['hello', 'world'])) # "hello world"
print('o'.join(['hell', ' w', 'rld'])) # "hello world"

# s[::-1] → reverse string in O(n).
s = "hello world"
print(s[::-1]) # "dlrow olleh"

# s.isalpha(), s.isdigit(), etc. → quick checks.
print("hello".isalpha()) # True
print("hello123".isalpha()) # False
print("123".isdigit()) # True
print("123abc".isdigit()) # False
print("helloworld".isalnum()) # True
print("hello world".isalnum()) # False

# .items() -> Unpacks each key-value pair
my_dict = {"a": 1, "b": 2, "c": 3}
for key, value in my_dict.items():
    print(key, value) # a 1
                      # b 2
                      # c 3

# .values() -> Get all values in a dictionary
my_dict = {"a": 1, "b": 2, "c": 3}
print(my_dict.values()) # dict_values([1, 2, 3])

print("1".isdigit())