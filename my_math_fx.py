"""
A script which goes through and finds prime numbers within the specified range.
"""

import math
import random

import math

def check_prime(a_number: int) -> bool:
    """
    Checks whether a_number is prime by testing divisibility against known primes.
    Only primes less than or equal to the square root of a_number are considered.
    """

    
    if a_number == 1:
        return False
    
    primes = make_primes(int(math.sqrt(a_number)) + 1)  # Generate primes only up to sqrt(a_number)

    for a_prime in primes:
        if a_number % a_prime == 0:
            return False

    return True

def make_primes(max_value: int) -> list[int]:
    """
    Generates a list of prime numbers up to max_value using the Sieve of Eratosthenes.
    """
    if max_value < 2:
        return []
    
    sieve = [True] * (max_value + 1)
    sieve[0] = sieve[1] = False  # 0 and 1 are not prime
    
    for start in range(2, int(math.sqrt(max_value)) + 1):
        if sieve[start]:
            for multiple in range(start * start, max_value + 1, start):
                sieve[multiple] = False

    return [num for num, is_prime in enumerate(sieve) if is_prime]


def get_primes(min: int, max: int) -> list[int]:
    """Returns the list of prime numbers within a certain range"""
    all_primes = make_primes(max)
    prime_chunk = []  # mem icky! we could just have pointers, but this is Python which means easy solutions
    
    for prime in all_primes:
        if prime >= min:
            prime_chunk.append(prime)
    
    return prime_chunk

def get_random_primes(min: int, max: int, amount: int) -> list[int]:
    """Returns a list of 'amount' random unique primes within the range of (min, max)"""
    primes = get_primes(min, max)

    if not primes:  # list is empty
        raise ValueError(f"No primes between min:{min} and max:{max}")
    elif len(primes) < amount:
        raise ValueError(f"You want {amount} primes but there are not enough primes from {min} to {max}")
    
    random_primes = []
    chosen_indices = set()  # set of already chosen primes
    while len(random_primes) != amount:
        random_index = random.randint(0, len(primes) - 1)
        
        if random_index not in chosen_indices:  # ensures uniqueness
            random_primes.append(primes[random_index])
            chosen_indices.add(random_index)
    
    return random_primes

def mod_exp(a: int, b: int, m: int) -> int:
    """Computes (a^b) % m using modular exponentiation."""
    result = 1
    a = a % m  # Reduce 'a' modulo 'm' first
    
    while b > 0:
        if b % 2 == 1:  # If 'b' is odd, multiply the result by 'a'
            result = (result * a) % m
        a = (a * a) % m  # Square 'a' and take modulo 'm'
        b //= 2  # Divide 'b' by 2
    
    return result

def bezout_coefficients(a: int, b: int) -> tuple[int, int]:
    """
    Computes the Bézout coefficients (s, t) such that:
        s * a + t * b = gcd(a, b)
    Using the forward pass with s_ij updates (without the backward pass).
    """
    s0, s1 = 1, 0  # Coefficients for 'a'
    t0, t1 = 0, 1  # Coefficients for 'b'
    
    while b != 0:
        q = a // b  # Quotient
        a, b = b, a % b  # Remainder update
        s0, s1 = s1, s0 - q * s1  # Update s coefficients
        t0, t1 = t1, t0 - q * t1  # Update t coefficients
    
    return (s0, t0)  # Bezout coefficients

def gcd(a: int, b: int) -> int:
    """Computes the greatest common divisor (GCD) of a and b using recursion."""
    return a if b == 0 else gcd(b, a % b)

def are_coprime(a: int, b: int) -> bool:
    """Returns True if a and b are coprime (i.e., gcd(a, b) == 1), otherwise False."""
    return gcd(a, b) == 1

def euler_toitent_two_prime(p : int, q :int) -> int:
    return (p-1)*(q-1)

def find_coprimes(num: int) -> list[int]:
    """finds all the coprimes to a specific number excludes itself"""
    the_coprimes = []
    for n in range(1, num): #exludes itself
        if gcd( n, num) == 1:
            the_coprimes.append(n)

    return the_coprimes


def get_a_coprime(a_num : int) -> int:
    """randomly gives a number that is coprime to a_num"""
    
    coprimes = find_coprimes(a_num)
    index = random.randint(0, len(coprimes)-1 ) #minus one cux inclusive
    return coprimes[index]


