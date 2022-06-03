
from random import randrange



def generate_random_hash(size= int) -> str:
	hash_result = []
	alphanumeric = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

	for i in range(0, size):
		random_char = randrange(0, 62)
		hash_result.append(alphanumeric[random_char])

	return "".join(hash_result)

print(generate_random_hash(7))

