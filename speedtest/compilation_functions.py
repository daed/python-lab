import subprocess

def compile_c_exec():
    """build the 'unit of work' c code.  this is a standalone executable"""
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
        print(result.stderr.decode())
        return False
    return True

def compile_c_code():
    """build the 'unit of work' c code.  this is a c library"""
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
        print(result.stderr.decode())
        return False
    return True

def build_cython_module():
    """build the cython module"""
    cython_command = [
        "python", "setup_cy.py", "build_ext", "--inplace"
    ]
    result = subprocess.run(
        cython_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False
    )
    if result.returncode != 0:
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
        print(result.stderr.decode())
        return False
    return True

