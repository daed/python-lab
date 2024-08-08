use std::time::Instant;

fn calculate_primes(limit: usize) {
    if limit < 2 {
        return; // No primes below 2
    }

    let mut primes = vec![true; limit + 1];
    primes[0] = false;
    primes[1] = false;

    for i in 2..=((limit as f64).sqrt() as usize) {
        if primes[i] {
            for j in (i * i..=limit).step_by(i) {
                primes[j] = false;
            }
        }
    }
}

#[no_mangle]
pub extern "C" fn unit_of_work(limit: usize) -> f64 {
    let start_time = Instant::now();
    calculate_primes(limit);
    let duration = start_time.elapsed();
    duration.as_secs_f64()
}

fn main() {
    let limit = 1_00_000;  
    let start_time = Instant::now();
    calculate_primes(limit);
    let duration = start_time.elapsed();
    println!("Time taken to calculate primes up to {}: {:?}", limit, duration);
}
