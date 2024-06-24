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
from wonderwords import RandomSentence
import time
import matplotlib.pyplot as plt



np.random.seed(0)
random.seed(0)

length=50
probability=0.05
max_size=25

def DNA_data_generate(length):
    lst=[]
    for i in range(length):
        seq_length = random.randint(1,max_size)
        lst.append(''.join(np.random.choice(('C','G','T','A'), seq_length )))
    return lst

def DNA_data_generate2(length,lst_prior):
    lst=[]
    for i in range(length):
        seq_length = random.randint(1,max_size)
        temp=''.join(np.random.choice(('C','G','T','A'), seq_length ))
        if temp not in (lst_prior):
            lst.append(temp)
    return lst


def test(data1,data2):
    
    lst1=data1
    lst2=data2

    bl=BloomFilter(length,probability)
    print('Size of Bloom Filter:', int(bl.length))
    print('Optimal number of Hahes for the Bloom Filter:', int(bl.hash_num))

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


def gen_sentence_data():
    lst=[]
    for i in range(length):
        s = RandomSentence()
        lst.append(s.sentence())
    
    return lst


    

data1=DNA_data_generate(length)
data2=DNA_data_generate2(length, data1)


test(data1,data2)
