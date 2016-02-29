import math

# Refactoring:
# 1. Rename variable f as meaningful boolean vector name: isPrime[]
# 2. Extract method for initializing the boolean vector
# 3. Extract method for Erotosthenes sieve process
# 4. Extract method for counting the number of primes up to N
# 4. Extract method for enumerating the primes up to N
# 5. Simplify the enumeratePrimes method
# 6. Delete the unnecessary method countPrimes
# 6. Rename variables

def calc(number):

    if number < 2: 
        return []
    
    number = number + 1

    isPrime = initialize(number)

    isPrime = eratoSieve(isPrime)

#     primeCount = countPrimes(isPrime)

    primes = enumeratePrimes(isPrime)
    return primes


def initialize(number):
    isPrime = [True] * number
    isPrime[0] = False
    isPrime[1] = False
    return isPrime

def eratoSieve(isPrime):
    N = len(isPrime)
    baseLimit = int(math.sqrt(N) + 1)
    for base in range(2, baseLimit):
        if isPrime[base]:
            for multiple in range(2 * base, N, base):
                isPrime[multiple] = False   
    return isPrime

def enumeratePrimes(isPrime):
    primes = []
    N = len(isPrime)
    for num in range(0, N):
        if isPrime[num]:
            primes.append(num)    
    return primes

# def countPrimes(isPrime):
#     count = 0
#     N = len(isPrime)
#     for num in range(0, N):
#         if isPrime[num]:
#             count = count + 1    
#     return count