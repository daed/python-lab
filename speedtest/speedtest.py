#!/bin/env python3
"""This program compiles and calls a function in a c++ library."""
import ctypes
import subprocess
import unit_of_work_py as pymodule
import compilation_functions as funcs


def build_required_modules():
    """build the required modules"""
    print("building required modules...")
    print("- pyinstaller:", end="")
    if funcs.py_installer():
        print("\t\t\tSUCCESS")
    else:
        print("\t\t\tFAILED")

    print("- c executable:", end="")
    if funcs.compile_c_exec():
        print("\t\t\tSUCCESS")
    else:
        print("\t\t\tFAILED")

    print("- c shared object:", end="")
    if funcs.compile_c_code():
        print("\t\tSUCCESS")
    else:
        print("\t\tFAILED")

    print("- cython bindings:", end="")
    if funcs.build_cython_module():
        print("\t\tSUCCESS")
    else:
        print("\t\tFAILED")

############### RUN FUNCTIONS ################

def run_cython_module():
    """run the cython module"""
    #print("...with cython module:", end="")
    try:
        import unit_of_work_cy as cy_module  # type: ignore # pylint: disable=import-error disable=import-outside-toplevel
        val = cy_module.calculate_primes()  # type: ignore # pylint: disable=c-extension-no-member
        #print(f"\t\t\t\t{val:.6f}s")
    except Exception as e:
        print(f"{e}")
    return val

def run_pyinstaller_exec():
    """run the pyinstaller executable"""
    #print("...with pyinstaller:", end="")
    result = subprocess.run(
        ['./dist/unit_of_work_py/unit_of_work_py'],
        stdout=subprocess.PIPE,
        check=False
    )
    val = float(result.stdout.decode().strip())
    #print(f"\t\t\t\t{val:.6f}s")
    if result.returncode != 0:
        print("Pyinstaller executable failed:")
        print(result.stderr.decode())
        return False
    return val

def run_c_executable():
    """run the c executable"""
    #print("...with native C executable:", end="")
    ## Don't start a timer, let the executable do it
    p = subprocess.run(['./unit_of_work', str(LIMIT)], stdout=subprocess.PIPE, check=False)
    val = float(p.stdout.decode().strip())
    #print(f"\t\t\t{val:.6f}s")
    return val

def run_c_library():
    """load the c library and set the function signature"""
    # this loads the c library and sets the function signature
    prime_lib = ctypes.CDLL('./unit_of_work.so')
    prime_lib.unit_of_work.argtypes = [ctypes.c_int]
    prime_lib.unit_of_work.restype = ctypes.c_double

    #print("...with C library (python import via ctypes):", end="")
    val = prime_lib.unit_of_work(LIMIT)
    #print(f"\t{val:.6f}s")
    return val

def run_python_module():
    """run the python module"""
    #print("...with Python module:", end="")
    elapsed = pymodule.calculate_primes(LIMIT)
    #print(f"\t\t\t\t{elapsed:.6f}s")
    return elapsed

############### MAIN ################

if __name__ == "__main__":
    LIMIT = 100000

    build_required_modules()

    # START CALCULATIONS
    print("calculating prime numbers up to 100,000...")
    
    stats = {
        "python": [],
        "pyinstaller": [],
        "cython": [],
        "c_library": [],
        "c_executable": []
    }
    for i in range(100):
        print(f"\rrunning iteration {i+1}", end="", flush=True)
        stats["python"].append(run_python_module())
        stats["pyinstaller"].append(run_pyinstaller_exec())
        stats["cython"].append(run_cython_module())
        stats["c_library"].append(run_c_library())
        stats["c_executable"].append(run_c_executable())
    print("\n")
    for i in stats:
        stat = stats[i]
        print(f"{i}: {(20 - len(i)) * ' '}avg {sum(stat)/len(stat):.6f}s high {max(stat):.6f}s low {min(stat):.6f}s")
