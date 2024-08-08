# unit_of_work_cy.pyx
import time
from libc.math cimport sqrt

def calculate_primes() -> list:
    """
    Calculates prime numbers up to limit.

    Sieve of Eratosthenes: https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
    """
    cdef bint is_prime[100000]
    cdef int number, multiple
    cdef double start_time, end_time
    start_time = time.time()

    # Initialize an array to true
    for i in range(100000):
        is_prime[i] = True

    is_prime[0] = is_prime[1] = False  # 0 and 1 are not primes

    # Optimize by only checking up to the square root
    for number in range(2, int(sqrt(100000)) + 1):
        if is_prime[number]:
            # No point in checking multiples of numbers that
            # are already known to not be prime
            for multiple in range(number * number, 100000, number):
                is_prime[multiple] = False


    end_time = time.time()
    print(f"- elapsed time: {end_time - start_time:.6f}s")
    return [i for i in range(100000) if is_prime[i]]

