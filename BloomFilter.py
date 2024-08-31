# importing necessary libraries
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
    def __init__(self, expected_num: int, prob: float):
        '''
        expected_num: Number of words stored in the bloom filter
        prob: False Positives probability
        '''
        self.length = self.calc_length(expected_num, prob)
        self.prob = prob
        self.hash_num = self.optimum_hashes(self.length ,expected_num) # number of hashes
        self.C = self.compute_cr(self.length, expected_num)
        try:
            self.bit_vector = int(self.length) * bitarray('0')
        except ValueError as exp:
            print(f"An exception of the type {exp} has occured.")
    
    @classmethod
    def calc_length(self, n1: int, n2: float): 
        '''
        calculating size of array given the number of elements (n1) and the false positive probability (n2)
        '''
        n = (-(n1 * math.log(n2)) / (math.log(2)) ** 2) 
        return int(n)
        
    # Question 8
    @classmethod
    def compute_cr(self, items_number, FP_proba, bits_number = 32):
        '''
        calculating the compression rate (CR)
        
        Parameters:
        items_number (int): number of items to be sorted in bloom filter
        FP_proba (float): wanted False Positive probability
        bits_number (int): number of bits per element

        Returns:
        Compression rate of bloom filter (float)
        '''
        # computing the size of the bloom filter
        size_bloom_filter = self.calc_length(items_number, FP_proba)
        # computing the size of a normal (traditional) data structure
        old_length = items_number * bits_number
        # calculating the compression rate
        comp_rate = old_length / size_bloom_filter
        return comp_rate
    
    @classmethod
    def optimum_hashes(self, item1, item2):
        '''
        calculating number of hash functions to use
        '''
        hash_number=((item1/item2)*math.log(2))
        return int(hash_number)
    
    def insert(self, data):
        '''
        adding an item to the bloom filter
        '''
        # verify if the type of data is integer or string
        if type(data) is int:
            data = str(data)
        if self.verify(data) == False:
            # initializitng a position pointer to 0
            position_pointer = 0
            for i in range(self.hash_num):
                if i%2 == 0:
                    # setting a certain bit in the array bit vector of bloom filter based on the hash of the input
                    position_pointer = int(mmh3.hash128(data, i, False) % int(self.length))
                    self.bit_vector[position_pointer] = True
                else:
                    # secure hashing and calculating posistion in the bit_vector array
                    position_pointer = int(pbkdf2_hmac('sha256', data.encode('utf-8'), str(i).encode('utf-8') * 2, 500_000).hex(), 16)%int(self.length)
                    self.bit_vector[position_pointer] = True
            print('The Input did not exist already, hence it has been added.')
        else:
            print('The Input probably already exists.')

    def verify(self, data):
        '''
        verifying whether an element is in the bloom filter
        '''
        if type(data) is int:
            data = str(data)
        position_verify = [None] * int(self.length)
        position_pointer = 0
        for i in range(self.hash_num):
            if i%2 == 0:
                position_pointer = int(mmh3.hash128(data, i, False)%int(self.length))   
                if self.bit_vector[position_pointer] == 1:
                    pass
                else:
                    return False
            else:
                position_pointer = int(pbkdf2_hmac('sha256', data.encode('utf-8'), str(i).encode('utf-8') * 2, 500_000).hex(),16)%int(self.length)
                if self.bit_vector[position_pointer] == 1:
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


# testing for creating the bloom filter
n = 1000  
p = 0.01  
bfilter=BloomFilter(n,p)

# testing for calculating the compression rate (basic case)
result = bfilter.compute_cr(100,0.05,32)
print(f'The compression rate is {result}.')
