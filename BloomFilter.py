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
        #print(self.length)
    
    @classmethod
    def calc_length(self, n1, n2): 
        n = (-(n1*math.log(n2))/(math.log(2))**2) 
        return n
    
    @classmethod
    def optimum_hashes(self, n1, n2): 
        n=((n1/n2)*math.log(2))
        return int(n)
    
    def insert(self, data):
        if self.verify(data)==False:
            position_pointer=0
            for i in range(self.hash_num):
                if i%2==0:
                    position_pointer=int(mmh3.hash128(data, i,False)%int(self.length))
                    self.bit_vector[position_pointer]=True
                else:
                    #position_pointer=int(sha256(data.encode('utf-8')).hexdigest()),16)%self.length
                    position_pointer=int(pbkdf2_hmac('sha256', data.encode('utf-8'), str(i).encode('utf-8') * 2, 500_000).hex(),16)%int(self.length)
                    self.bit_vector[position_pointer]=True
            print('The Input definatly did not already exists, hence it has been added')
        else:
            print('The Input probably already exists')

    def verify(self, data):
        position_pointer=0
        for i in range(self.hash_num):
            if i%2==0:
                position_pointer=int(mmh3.hash128(data, i,False)%int(self.length))
                
                if self.bit_vector[position_pointer]==1:
                    pass
                else:
                    return False
            else:
                position_pointer=int(pbkdf2_hmac('sha256', data.encode('utf-8'), str(i).encode('utf-8') * 2, 500_000).hex(),16)%int(self.length)
                if self.bit_vector[position_pointer]==1:
                    pass
                else:
                    return False
        return True
    
    def __str__(self):  
        return "The bloom filter in string form is % s" % (self.bit_vector) 
                    
