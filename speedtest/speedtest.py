#!/bin/env python3
"""This program compiles and calls a function in a c++ library."""
import ctypes
import subprocess
import time
import sys
import unit_of_work_py as pymodule
import unit_of_work_cy as cy_module
prime_lib = None


def compile_c_exec():
    gcc_command = [
        'gcc', '-o', 'unit_of_work',  
        '-O3',                        
        'unit_of_work.c'              
    ]
    # Run the gcc command
    result = subprocess.run(
        gcc_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False
    )
    if result.returncode != 0:
        print("Compilation failed:")
        print(result.stderr.decode())
        return False
    print("Compilation successful")
    return True

def compile_c_code():
    """build the 'unit of work' c code"""
    gcc_command = [
        'gcc', '-shared', '-o', 'unit_of_work.so',
        '-fPIC', 'unit_of_work.c'
    ]

    # Run the gcc command
    result = subprocess.run(
        gcc_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False
    )
    if result.returncode != 0:
        print("Compilation failed:")
        print(result.stderr.decode())
        return False
    return True

def py_installer():
    """run pyinstaller against the python script"""
    pyinstaller_command = [
        'pyinstaller', '-y', 'unit_of_work_py.py',
    ]
    result = subprocess.run(
        pyinstaller_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False
    )
    if result.returncode != 0:
        print("Pyinstaller failed:")
        print(result.stderr.decode())
        return False
    return True

def run_pyinstaller_exec():
    """run the pyinstaller executable"""
    result = subprocess.run(
        ['./dist/unit_of_work_py/unit_of_work_py'],
        check=False
    )
    if result.returncode != 0:
        print("Pyinstaller executable failed:")
        print(result.stderr.decode())
        return False
    return True

def load_c_library():
    """load the c library and set the function signature"""
    global prime_lib  # pylint: disable=global-statement
    prime_lib = ctypes.CDLL('./unit_of_work.so')
    prime_lib.calculate_primes.argtypes = [ctypes.c_int]
    prime_lib.calculate_primes.restype = None

if __name__ == "__main__":
    LIMIT = 100000

    # build this for later
    compile_c_exec()
    py_installer()

    # START CALCULATIONS
    print("Calculating prime numbers...")

    print("...with Python module:")
    ## Start the timer
    start_time = time.time()
    pymodule.calculate_primes(LIMIT)
    end_time = time.time()
    ## End the timer
    print(f"- elapsed time: {end_time - start_time:.6f}s")

    # Run the pyinstaller executable (has its own timer)
    print("...with pyinstaller:")
    run_pyinstaller_exec()

    # Run the cython module (has its own timer)
    print("...with cython module")
    cy_module.calculate_primes()

    # Compile the C code
    if compile_c_code():
        load_c_library()

        print("...with C library (python import via ctypes):")
        ## Start the timer
        start_time = time.time()
        prime_lib.calculate_primes(LIMIT)
        end_time = time.time()
        ## End the timer

        print(f"- elapsed time: {end_time - start_time:.6f}s")
    else:
        sys.exit(1)

    print("...with native C executable:")
    ## Don't start a timer, let the executable do it
    subprocess.run(['./unit_of_work', str(LIMIT)], check=False)
