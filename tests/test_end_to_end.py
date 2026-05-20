import subprocess
import os
import sys
from pathlib import Path
from error_handling import ErrorCode


def test_valid_program():
    main_path = Path(__file__).parent.parent / "src" #path to main
    mockdata_path = Path(__file__).parent / "mock_data" #path to the cimple file 
    input_file = mockdata_path / "valid.cimple"  #The file we want to test
    
    # Run main.py with input file and capture everything
    result = subprocess.run(
        ["python", "main.py", str(input_file), "output.c"],
        capture_output=True,
        text=True,
        timeout=10,
        cwd=main_path
    )

    outputLines = result.stdout.split("\n")
    
    assert result.returncode == 0
    assert outputLines[0] == "10"
    assert outputLines[1] == "Hello world"
    assert outputLines[2] == "false"

def test_sad_lexer_program():
    main_path = Path(__file__).parent.parent / "src" #path to main
    mockdata_path = Path(__file__).parent / "mock_data" #path to the cimple file 
    input_file = mockdata_path / "invalid_lexer.cimple"  #The file we want to test
    
    # Run main.py with input file and capture everything
    result = subprocess.run(
        ["python", "main.py", str(input_file), "output.c"],
        capture_output=True,
        text=True,
        timeout=10,
        cwd=main_path
    )

    assert result.returncode == ErrorCode.LEXER_ERROR.value
    assert result.stdout == ""    

def test_sad_parser_program():
    main_path = Path(__file__).parent.parent / "src" #path to main
    mockdata_path = Path(__file__).parent / "mock_data" #path to the cimple file 
    input_file = mockdata_path / "invalid_parser.cimple"  #The file we want to test
    
    # Run main.py with input file and capture everything
    result = subprocess.run(
        ["python", "main.py", str(input_file), "output.c"],
        capture_output=True,
        text=True,
        timeout=10,
        cwd=main_path
    )

    assert result.returncode == ErrorCode.PARSER_ERROR.value
    assert result.stdout == ""



def test_sad_typecheck_program():
    main_path = Path(__file__).parent.parent / "src" #path to main
    mockdata_path = Path(__file__).parent / "mock_data" #path to the cimple file 
    input_file = mockdata_path / "invalid_typecheck.cimple"  #The file we want to test
    
    # Run main.py with input file and capture everything
    result = subprocess.run(
        ["python", "main.py", str(input_file), "output.c"],
        capture_output=True,
        text=True,
        timeout=10,
        cwd=main_path
    )

    # Assert the stdout (program output)
    assert result.returncode == ErrorCode.TYPECHECKER_ERROR.value
    assert result.stdout == ""    