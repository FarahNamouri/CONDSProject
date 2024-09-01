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
    
    # methods
    def calc_length(self, n1: int, n2: float) -> int: 
        '''
        calculating size of array given the number of elements (n1) and the false positive probability (n2)
        
        parameters:
        n1 (int): number of elements in the bloom filter
        n2 (float): false positive probability

        returns
        size of a bloom filter (int)
        '''
        return int(-(n1 * math.log(n2)) / (math.log(2) ** 2))

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
    
    # Question 7
    def compute_fpr(self, entered_n: int) -> float:
        '''
        calculating the value of the false positive rate
        
        parameters:
        entered_n (int): number of the entered/inserted items in a bloom filter

        returns
        false positive rate (float)
        '''
        return (1 - (1 - 1/self.length) ** (self.hash_num * entered_n)) ** self.hash_num

    def plot_fpr(self, values_n):
        '''
        plotting the false positive rate as a function of the number of words inserted in the bloom filter
        
        parameters:
        values_n (integers' list): the values of numbers of items to be sorted in the bloom filter

        returns
        plot (graph)
        '''
        plt.figure(figsize=(10,5))
        # list that will contain the false positive rates
        fp_rates= []
        for entered_n in values_n:
            # computing the false positive rate for each enetered item (entered_n)
            fp_rate = self.compute_fpr(entered_n)
            fp_rates.append(fp_rate)

        plt.plot(values_n, fp_rates,marker='o')
        plt.title("False Positive rate of the number of words inserted in the bloom filter")
        plt.xlabel('Number of Inserted Items (n)')
        plt.ylabel('False Positive Rate')
        plt.grid(True)
        plt.show()
        
    # Question 8
    def compute_cr(self, items_number, bits_number = 32):
        '''
        calculating the compression rate (CR) of a bloom filter as a function of the expected number of elements and the rate of false positives 
        
        parameters:
        items_number (int): number of items to be sorted in bloom filter
        bits_number (int): number of bits per element (default = 32)

        returns:
        Compression rate of bloom filter (float)
        '''
        # calculating again the bloom filter's size
        m = self.calc_length(items_number, self.prob)
        
        # computing the size of a normal (traditional) data structure
        old_length = items_number * bits_number
        
        # calculating the compression rate
        comp_rate = (old_length / m) * math.exp(-items_number / m)
        return comp_rate
     
    def plot_cr(self, items_number, bits_number =32):
        """
        plotting the compression rate of a bloomfilter as a function of the expected number of elements and the rate of false positives.

        parameters:
        items_number (list of int): values for the number of items expected to be stored in the filter
        bits_number (int): the number of bits per element in a data structure (by default 32)

        returns
        plot (graph)
        """
    
        plt.figure(figsize=(10, 6))
        compression_rates = []

        for n in items_number:
            compression_rate = self.compute_cr(n, bits_number)
            compression_rates.append(compression_rate)

        plt.plot(items_number, compression_rates, marker='o')

        # naming and labeling the plot
        plt.title('Compression Rate of Bloom Filter vs Number of Items')
        plt.xlabel('Number of Items in the bloom filter')
        plt.ylabel('Compression Rate')
        plt.grid(True)
        plt.show()
    
# testing for creating the bloom filter
n = 1000  
p = 0.05  
bfilter=BloomFilter(n,p)

# false positive rate and its plot (question 7)
n_expected = 10000  
fp_probability_desired = 0.01    
bloom_filter = BloomFilter(n_expected, fp_probability_desired)
result_fpr = bfilter.compute_fpr(5)
print(f'The false positive rate is {result_fpr}.')
values_n = [100, 1000, 5000, 10000, 20000, 50000, 100000] 
bloom_filter.plot_fpr(values_n)

# calculating the compression rate and its plot (question 8)
result = bfilter.compute_cr(100,32)
print(f'The compression rate is {result}.')
n_first = 10000  
p_wanted = 0.05 
bloom_filter =BloomFilter(n_first, p_wanted)
n_values = [100, 500, 1000, 5000, 10000, 20000, 50000, 100000]  
bloom_filter.plot_cr(n_values)
