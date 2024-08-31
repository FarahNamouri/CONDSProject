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
    
    def calc_length(self, n1: int, n2: float) -> int: 
        '''
        calculating size of array given the number of elements (n1) and the false positive probability (n2)
        '''
        return int(-(n1 * math.log(n2)) / (math.log(2) ** 2))
        
    # Question 8
    def compute_cr(self, items_number, bits_number = 32):
        '''
        calculating the compression rate (CR)
        
        Parameters:
        items_number (int): number of items to be sorted in bloom filter
        FP_proba (float): wanted False Positive probability
        bits_number (int): number of bits per element
        m: size of bloom filter

        Returns:
        Compression rate of bloom filter (float)
        '''
        # calculating again the bloom filter's size
        m = self.calc_length(items_number, self.prob)
        
        # computing the size of a normal (traditional) data structure
        old_length = items_number * bits_number
        
        # calculating the compression rate
        comp_rate = (old_length / m) * math.exp(-items_number / m)
        return comp_rate
     
    def plot_cr(self, items_number, bits_number=32):
        """
        plotting the compression rate of a bloomfilter as a function of the expected number of elements and the rate of false positives.

        Parameters:
        n_values (list of int): values for the number of items expected to be stored in the filter
        FP_values (list of float): false positive probabilities values
        b (int): the number of bits per element in a data structure (by default 32)

        Returns
        plot (graph)
        """
    
        plt.figure(figsize=(10, 6))
        compression_rates = []

        for n in items_number:
            # Calculate the compression rate for each combination of n and p
            compression_rate = self.compute_cr(n, bits_number)
            compression_rates.append(compression_rate)

            # Plot compression rate as a function of n for a given p
        plt.plot(items_number, compression_rates, marker='o')

        # Labeling the plot
        plt.title('Compression Rate of Bloom Filter vs Number of Items')
        plt.xlabel('Number of Items (n)')
        plt.ylabel('Compression Rate')
        plt.grid(True)

        # Display the plot
        plt.show()
    

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

# testing for creating the bloom filter
n = 1000  
p = 0.05  
bfilter=BloomFilter(n,p)

#testing for calculating the compression rate 
result = bfilter.compute_cr(100,32)
print(f'The compression rate is {result}.')

n_first = 10000  
p_wanted = 0.05   
bloom_filter = BloomFilter(n_first, p_wanted)

n_values = [100, 500, 1000, 5000, 10000, 20000, 50000, 100000]  # Example values for n (number of items)

bloom_filter.plot_cr(n_values)
