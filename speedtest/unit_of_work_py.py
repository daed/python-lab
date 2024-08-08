"""unit_of_work.py"""
import time
import math

def calculate_primes(num_limit: int) -> None:
    """
    Calculates prime numbers up to limit.

    Sieve of Eratosthenes: https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
    """
    if num_limit < 2:
        return  # No primes below 2

    # initialize an array to true
    is_prime = [True] * (num_limit + 1)

    is_prime[0] = is_prime[1] = False  # 0 and 1 are not primes

    # optimize by only checking up to the square root, because duh
    for number in range(2, math.isqrt(num_limit+1)):
        if is_prime[number]:
            # no point in checking multiples of numbers that
            # are already known to not be prime
            for multiple in range(number * number, num_limit + 1, number):
                is_prime[multiple] = False
    return is_prime

if __name__ == "__main__":
    LIMIT = 100000
    start_time = time.time()
    calculate_primes(100000)
    end_time = time.time()

    print(f"- elapsed time: {end_time - start_time:.6f}s")