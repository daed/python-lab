#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>  // Added this line for malloc and free
#include <time.h>

void calculate_primes(int limit) {
    /* 
    Calculates prime numbers up to limit.

    Sieve of Eratosthenes: https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
    */
    if (limit < 2) return; // No primes below 2

    bool *is_prime = malloc((limit + 1) * sizeof(bool));
    if (is_prime == NULL) {
        perror("Failed to allocate memory");
        return;
    }

    for (int i = 0; i <= limit; i++) {
        is_prime[i] = true;
    }

    is_prime[0] = is_prime[1] = false; // 0 and 1 are never prime

    for (int number = 2; number * number <= limit; number++) {
        if (is_prime[number]) {
            for (int multiple = number * number; multiple <= limit; multiple += number) {
                is_prime[multiple] = false;
            }
        }
    }

    free(is_prime); // Don't forget to free the allocated memory
}

void unit_of_work(int limit) {
    clock_t start_time = clock();
    calculate_primes(limit);
    clock_t end_time = clock();
    double elapsed_time = (double)(end_time - start_time) / CLOCKS_PER_SEC;
    printf("- elapsed time: %fs\n", elapsed_time);
}

int main() {
    int limit = 100000; // You can adjust the limit here
    unit_of_work(limit);
    printf("finished\n");
    return 0;
}
