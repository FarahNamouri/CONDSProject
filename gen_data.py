#!usr/bin/env/ pyhton
# importing necessary packages
import math
import mmh3
from hashlib import sha256
import hmac,hashlib,io
from hashlib import pbkdf2_hmac
from bitarray import bitarray
from BloomFilter import BloomFilter
import numpy as np
import random
from wonderwords import RandomSentence
import time
import matplotlib.pyplot as plt
import json

# this function generates 2 data files (2 data types): input_data and check_data.

# setting the seed
np.random.seed(0)
random.seed(0)

# declaring the properties
length = 100000
probability = 0.05
max_size = 100
max_value =100000000

def DNA_data_generate(length: int):
    """
    Function to generate the dna sequence
    Args:
    length: int
    Output:
    returns a list of the DNA sequence
    """
    lst=[]
    for i in range(length):
        seq_length = random.randint(1,max_size)
        lst.append(''.join(np.random.choice(('C','G','T','A'), seq_length )))
    return lst

def DNA_data_generate2(length,lst_prior):
    lst=[]
    i=0
    while i != length:
        seq_length = random.randint(1,max_size)
        temp=''.join(np.random.choice(('C','G','T','A'), seq_length ))
        if temp not in (lst_prior):
            lst.append(temp)
            i+=1
    return lst

def gen_sentence_data():
    lst=[]
    for i in range(length):
        s = RandomSentence()
        lst.append(s.sentence())
    return lst

data1=DNA_data_generate(length)
data2=DNA_data_generate2(length, data1)

def DNA_number(length: int):
    """
    Function to generate the nunbers
    Args:
    length: int
    Output:
    returns a list of numbers
    """
    lst=[]
    for i in range(length):
        lst.append(random.randint(1, max_value))
    return lst


def DNA_number2(length,lst_prior):
    lst=[]
    i=0
    while i != length:
        temp=(random.randint(1, max_value))
        if temp not in (lst_prior):
            lst.append(temp)
            i+=1
    return lst

data1=DNA_number(length)
data2=DNA_number2(length, data1)

# input_data inputs data into the Bloom filter
f = open('input_data.txt', 'w')
json.dump(data1, f)
f.close()

# check_data creates a datafile that doesn't have the data that already been in the input
f = open('check_data.txt', 'w')
json.dump(data2, f)
f.close()

f = open('input_data2.txt', 'w')
json.dump(data1, f)
f.close()

f = open('check_data2.txt', 'w')
json.dump(data2, f)
f.close()
