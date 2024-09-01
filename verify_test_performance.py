#!usr/bin/env/ pyhton
import math
import mmh3
from hashlib import sha256
import hmac,hashlib,io
from hashlib import pbkdf2_hmac
from bitarray import bitarray
from BloomFilter import BloomFilter
import numpy as np
import random
from wonderwords import RandomSentence,RandomWord
import time
import matplotlib.pyplot as plt

def generate_words(n = 0):
    '''
    Generating words function
    '''
    words=[]
    for i in range(n):
        r = RandomWord()
        words.append(r.word())
    return set(words)

def main():
    print('verify')
    data = generate_words(1000)
    data_list = list(data)
    # optimal sizes chosen
    sizes = [10, 50,75, 100,200,350, 500, 1_000,5_000]
    samples = [
        random.sample(data_list, k=size) for size in sizes
    ]
    # number of runs
    nr_runs = 3
    times = {}
    verify_sample = random.sample(data_list, k=20)
    i = 0
    for sample in samples:
        btree = BloomFilter(sizes[i],0.05)
        i += 1
        for word in sample:
            btree.insert(word)
        times[len(sample)] = 0.0
        for _ in range(nr_runs):
            start_time = time.time_ns()
            for word in verify_sample:
                btree.verify(word)
            end_time = time.time_ns()
            times[len(sample)] += end_time - start_time
        times[len(sample)] /= nr_runs*1_000_000.0
        print(times)

# plotting to see the performance
    plt.plot(times.keys(), times.values());
    plt.savefig('plotverify.png')

if __name__ == "__main__":
    main()
