import hashlib
import math
import random
import string
from functools import partial
from typing import Any, List, Callable


class BloomFilter:
    """
    Simple bloom filter realisation with bytearray
    """

    def __init__(self, size: int, hash_functions: List[Callable]):
        self.size = size
        self.hash_functions = hash_functions
        self.bit_array = bytearray(size)

    def _get_hash_indices(self, value: Any) -> List[int]:
        indices = []
        for hf in self.hash_functions:
            hash_value = hf(value)
            # print(hash_value)

            if hash_value <= 0:
                print('Warning: negative hash function (possible hash overflow) {}'.format(hash_value))

            bit_index = hash_value % self.size
            indices.append(bit_index)

        return indices

    def add_item(self, value: Any) -> None:
        indices = self._get_hash_indices(value)
        for ind in indices:
            self.bit_array[ind] = 1

    def __contains__(self, value: Any) -> bool:
        indices = self._get_hash_indices(value)
        for ind in indices:
            if self.bit_array[ind] == 0:
                return False

        return True


def _get_bloom_filter_accuracy(m, hash_functions, words):
    bl = BloomFilter(m, hash_functions)

    N = len(words)
    item_count = 0
    for j in range(N):
        w = words[j]

        if w not in bl:
            bl.add_item(w)
            item_count += 1

    accuracy = item_count / N

    return accuracy


def _test_simple_bloom_filter_count_unique_values(words, size):
    # Define simple hash function
    # (dont forget to set PYTHONHASHSEED from console for reproduce purposes)
    def default_hash(value):
        return hash(value) & ((1 << 64) - 1)  # get the first 64 bits of the hash

    accuracy = _get_bloom_filter_accuracy(size, [default_hash], words)

    print('Simple hash accuracy: ', accuracy)
    print()


def _test_hashlib_bloom_filter_count_unique_values(words, size):
    # Define simple hash function (deterministic!)
    def sha1_hash(value, salt):
        hasher = hashlib.sha1()
        hasher.update(salt.encode())
        hasher.update(value.encode())
        return int(hasher.hexdigest()[:8], 16)

    # Define family of the same functions with different salt
    hash_functions = []
    N_HASH_FUNCTIONS = 10
    for i in range(N_HASH_FUNCTIONS):
        hash_functions.append(partial(sha1_hash, salt=str(random.randint(0, 2e32 - 1))))

    N = len(words)
    actual = []
    for hash_functions_count in range(1, N_HASH_FUNCTIONS + 1):
        accuracy = _get_bloom_filter_accuracy(size, hash_functions[:hash_functions_count], words)
        actual.append(accuracy)
        print('SHA-1 x {} accuracy: {}'.format(hash_functions_count, accuracy))

    assert actual == [0.892, 0.942, 0.953, 0.965, 0.958, 0.949, 0.94, 0.934, 0.913, 0.898]
    print()

    # Optimal parameters
    FP_RATE = 0.05
    optimal_size = math.ceil(- N * math.log(FP_RATE) / ((math.log(2)) ** 2))
    optimal_hash_functions_count = math.ceil(optimal_size / N * math.log(2))
    print('Optimal parameters for {} FP error \nBit Array size: {} \nHash functions count: {} '.format(
        FP_RATE, optimal_size, optimal_hash_functions_count
    ))

    accuracy = _get_bloom_filter_accuracy(optimal_size, hash_functions[:optimal_hash_functions_count], words)
    print('SHA-1 x {} accuracy: {}'.format(optimal_hash_functions_count, accuracy))
    assert accuracy > 1 - FP_RATE
    assert accuracy == 0.984

    print()


def _test_bloom_filter_count_unique_values():
    """Count unique values"""
    RANDOM_SEED = 42
    random.seed(RANDOM_SEED)

    # Generate data
    words = []
    N = 1000
    WORD_BOUNDS = (3, 20)

    while len(words) < N:
        word_length = random.randint(*WORD_BOUNDS)
        random_word = ''.join(random.choice(string.ascii_lowercase) for _ in range(word_length))

        if random_word not in words:
            words.append(random_word)

    # Set bit array size (bigger = better accuracy, slower, more memory)
    size = 4096  # ~ 4 KiloByte, check with __sizeof__() function
    print(bytearray(size).__sizeof__())

    print('Bloom Filter test \nData size: {} \nBit Array size: {}'.format(N, size))
    print()
    _test_simple_bloom_filter_count_unique_values(words, size)
    _test_hashlib_bloom_filter_count_unique_values(words, size)


if __name__ == "__main__":
    _test_bloom_filter_count_unique_values()
