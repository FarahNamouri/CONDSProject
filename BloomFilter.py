#libraries
from BitVector import BitVector
import math
import mmh3
from hashlib import sha256
import hmac,hashlib,io
from hashlib import pbkdf2_hmac
from bitarray import bitarray

class BloomFilter:
    #bit_vector=BitVector(size=0)
    
    def __init__(self, expected_num=0, prob=0):
        self.length=self.calc_length(expected_num, prob)
        self.prob=prob
        self.hash_num=self.optimum_hashes(self.length ,expected_num)
        try:
            self.bit_vector=int(self.length)*bitarray('0')
        except ValueError as exp:
            print(f"An exception of the type {exp} has occured")
    
    @classmethod
    def calc_length(self, n1, n2): 
        pass
    
    @classmethod
    def optimum_hashes(self, n1, n2): 
        pass
    
    def insert(self, data):
        pass

    def verify(self, data):
        pass
    
    def __str__(self):  
        pass
                    