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


#prepare for Question 7 and Question 8

# setting the seed
np.random.seed(0)
random.seed(0)

# declaring the properties
length = 100000
probability = 0.05
max_size = 100

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
