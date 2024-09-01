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
from gen_data import DNA_data_generate,DNA_data_generate2

#prepare for Question 7 and Question 8

# setting the seed
np.random.seed(0)
random.seed(0)

# declaring the properties
length = 5
probability = 0.05
max_size = 2


# test function 
def test(data1,data2):
    lst1=data1
    lst2=data2
    bl=BloomFilter(length,probability)
    print('Size of Bloom Filter:', int(bl.length))
    print('Optimal number of hahes for the Bloom Filter:', int(bl.hash_num))

    for i in range(length):
        bl.insert(lst1[i])
    print('Bloom Filter created')

    #test
    count1=0
    count2=0
    false_count=0
    for i in range(len(lst1)):
        if bl.verify(lst1[i])==True:
            count1+=1
    if count1==len(lst1):
        print('Present Data passed')
            
    for i in range(len(lst2)):
        if bl.verify(lst2[i])==False:
            count2+=1
        else:
            print('False Positive: ', lst2[i], bl.bit_vector)
    if count2==len(lst2):
        print('Non-present Data passed')


#data1=DNA_data_generate(length)
#data2=DNA_data_generate2(length, data1)

with open("input_data.txt", 'r') as file:
    data = file.read().strip()
    data_list = eval(data) 

data1=data_list

print(data1)

with open("check_data.txt", 'r') as file:
    data = file.read().strip()
    data_list = eval(data) 

data2=data_list

print(data2)

# calling test function
test(data1,data2)
