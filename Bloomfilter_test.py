#libraries
from BitVector import BitVector
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

length=20
probability=0.05
max_size=5

def generate_number(length):
    lst=[]
    for i in range(length):
        lst.append(random.randrange(1,100000))
    return lst

def generate_number2(length,lst_prior):
    lst=[]
    for i in range(length):
        temp=(random.randrange(1,100000))
        if temp not in (lst_prior):
            lst.append(temp)
    return lst

num1=(generate_number(length))

num2=(generate_number2(length,num1))

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
            false_count+=1
    if count2==len(lst2):
        print('Non-present Data passed')
    else:
        print("The False Positives have been printed above and they are: ",false_count)

test(num1,num2)

def gen_sentence_data(length):
    lst=[]
    for i in range(length):
        s = RandomSentence()
        lst.append(s.sentence())
    return lst