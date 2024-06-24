#libraries
from BitVector import BitVector
import math
import mmh3
from hashlib import sha256
import hmac,hashlib,io
from hashlib import pbkdf2_hmac
from bitarray import bitarray

class BloomFilter:
    '''
    Bloom Filter Class
    '''
    def __init__(self, expected_num=0, prob=0):
        '''
        expected_num: Number of words stored in the bloom filter
        prob: False Positives probability
        '''
        self.length=self.calc_length(expected_num, prob)
        self.prob=prob
        self.hash_num=self.optimum_hashes(self.length ,expected_num)
        self.C=self.compute_cr(self.length, expected_num)
        try:
            self.bit_vector=int(self.length)*bitarray('0')
        except ValueError as exp:
            print(f"An exception of the type {exp} has occured")
    
    @classmethod
    def calc_length(self, n1, n2): 
        '''
        calculating size of array
        '''
        n = (-(n1*math.log(n2))/(math.log(2))**2) 
        return n
        
    # Question 8
    @classmethod
    def compute_cr(self,m,expected_num):
        '''
        calculating the compression rate (CR)
        '''
        return m/expected_num
    
    @classmethod
    def optimum_hashes(self, n1, n2):
        '''
        calculating number of hash functions to use
        '''
        n=((n1/n2)*math.log(2))
        return int(n)
    
    def insert(self, data):
        '''
        adding item to the bloom filter
        '''
        if type(data) is int:
            data=str(data)
        if self.verify(data)==False:
            position_pointer=0
            for i in range(self.hash_num):
                if i%2==0:
                    position_pointer=int(mmh3.hash128(data, i,False)%int(self.length))
                    self.bit_vector[position_pointer]=True
                else:
                    position_pointer=int(pbkdf2_hmac('sha256', data.encode('utf-8'), str(i).encode('utf-8') * 2, 500_000).hex(),16)%int(self.length)
                    self.bit_vector[position_pointer]=True
            print('The Input definatly did not already exists, hence it has been added')
        else:
            print('The Input probably already exists')

    def verify(self, data):
        '''
        verifying if an element is in the bloom filter
        '''
        if type(data) is int:
            data=str(data)
        position_verify=[None]*int(self.length)
        position_pointer=0
        for i in range(self.hash_num):
            if i%2==0:
                position_pointer=int(mmh3.hash128(data, i,False)%int(self.length))
                
                if self.bit_vector[position_pointer]==1:
                    pass
                else:
                    return False
            else:
                #position_pointer=int(sha256(data.encode('utf-8')).hexdigest()),16)%self.length
                position_pointer=int(pbkdf2_hmac('sha256', data.encode('utf-8'), str(i).encode('utf-8') * 2, 500_000).hex(),16)%int(self.length)
                if self.bit_vector[position_pointer]==1:
                    pass
                else:
                    return False
        return True
    
    def __str__(self):  
        return "The bloom filter in string form is % s" % (self.bit_vector)

#Question.no.7
def fp_bloomfilter(expec, p, adding, max_adds, length_test):
    bloom_filter_test = BloomFilter(expec, p)
    added_items = 0
    
    words_in_BF = [str(i) for i in range(max_adds)]
    words_not_in_BF = [str(i) for i in range(max_adds, max_adds + length_test)]
    
    "adding words and calculating FPR"
    fp_rates = []
    for word in words_in_BF:
        bloom_filter_test.insert(word)
        added_items += 1
        if added_items % adding== 0:
            fp = 0
            for word_test in words_not_in_BF:
                if bloom_filter_test.verify(word_test):
                    fp += 1
            fp_rate = fp / length_test
            fp_rates.append((added_items, fp_rate))
    return fp_rates

#testing
expec = 4 
p = 0.01  
adding = 6  
max_adds = 6  
length_test = 8 

fp_rates = fp_bloomfilter(expec, p, adding, max_adds, length_test)
for count, rate in fp_rates:
    print(f"The number of the added items is {count}, the FP rate is {rate:.4f}")
