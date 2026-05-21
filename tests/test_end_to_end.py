import subprocess
from pathlib import Path
from error_handling import ErrorCode

def test_valid_program():
    mainPath = Path(__file__).parent.parent / "src" #path to main
    mockdataPath = Path(__file__).parent / "mock_data" #path to the cimple file 
    inputFile = mockdataPath / "valid.cimple"  #The file we want to test
    
    # Run main.py with input file and capture everything
    result = subprocess.run(
        ["python", "main.py", str(inputFile), "output", "-r"],
        capture_output=True,
        text=True,
        timeout=10,
        cwd=mainPath
    )

    outputLines = result.stdout.split("\n")
    
    assert result.returncode == 0
    assert outputLines[0] == "10"
    assert outputLines[1] == "Hello world"
    assert outputLines[2] == "false"

def test_sad_lexer_program():
    mainPath = Path(__file__).parent.parent / "src" #path to main
    mockdataPath = Path(__file__).parent / "mock_data" #path to the cimple file 
    inputFile = mockdataPath / "invalid_lexer.cimple"  #The file we want to test
    
    # Run main.py with input file and capture everything
    result = subprocess.run(
        ["python", "main.py", str(inputFile), "output"],
        capture_output=True,
        text=True,
        timeout=10,
        cwd=mainPath
    )

    assert result.returncode == ErrorCode.LEXER_ERROR.value
    assert result.stdout == ""
    assert "INVALID_CHARACTER" in result.stderr    

def test_sad_parser_program():
    mainPath = Path(__file__).parent.parent / "src" #path to main
    mockdataPath = Path(__file__).parent / "mock_data" #path to the cimple file 
    inputFile = mockdataPath / "invalid_parser.cimple"  #The file we want to test
    
    # Run main.py with input file and capture everything
    result = subprocess.run(
        ["python", "main.py", str(inputFile), "output"],
        capture_output=True,
        text=True,
        timeout=10,
        cwd=mainPath
    )

    assert result.returncode == ErrorCode.PARSER_ERROR.value
    assert result.stdout == ""
    assert "STRUCTURE_ERROR" in result.stderr



def test_sad_typecheck_program():
    mainPath = Path(__file__).parent.parent / "src" #path to main
    mockdataPath = Path(__file__).parent / "mock_data" #path to the cimple file 
    inputFile = mockdataPath / "invalid_typecheck.cimple"  #The file we want to test
    
    # Run main.py with input file and capture everything
    result = subprocess.run(
        ["python", "main.py", str(inputFile), "output"],
        capture_output=True,
        text=True,
        timeout=10,
        cwd=mainPath
    )

    assert result.returncode == ErrorCode.TYPECHECKER_ERROR.value
    assert result.stdout == ""    
    assert "MISSING_RETURN_ERROR" in result.stderr
    assert "UNDEFINED_VARIABLE_ERROR" in result.stderr
    assert "UNDEFINED_FUNCTION_ERROR" in result.stderr
    assert "ALREADY_DECLARED_ERROR" in result.stderr
    assert "CANNOT_ASSIGN" in result.stderr
    assert "INVALID_ARGUMENT_COUNT" in result.stderr
    assert "TYPE_MISMATCH_ERROR" in result.stderr

def test_help():
    mainPath = Path(__file__).parent.parent / "src" #path to main
    
    # Run main.py requesting help
    result = subprocess.run(
        ["python", "main.py", "--help"],
        capture_output=True,
        text=True,
        timeout=10,
        cwd=mainPath
    )

    assert result.returncode == 0
    assert result.stdout.strip().startswith("OBS:")    

def test_keepFlag():
    mainPath = Path(__file__).parent.parent / "src" #path to main
    mockdataPath = Path(__file__).parent / "mock_data" #path to the cimple file 
    inputFile = mockdataPath / "valid.cimple"  #The file we want to test
    # Run main.py requesting help
    result = subprocess.run(
        ["python", "main.py", inputFile, "output" ,"-k", "ending_on.c"],
        capture_output=True,
        text=True,
        timeout=10,
        cwd=mainPath
    )

    cFile = mainPath / "ending_on.c"
    assert result.returncode == 0
    assert cFile.exists()


def test_keepFlag_wrong_extension():
    mainPath = Path(__file__).parent.parent / "src" #path to main
    mockdataPath = Path(__file__).parent / "mock_data" #path to the cimple file 
    inputFile = mockdataPath / "valid.cimple"  #The file we want to test
    # Run main.py requesting help
    result = subprocess.run(
        ["python", "main.py", inputFile, "output","-k", "not_ending_on_dot_c"],
        capture_output=True,
        text=True,
        timeout=10,
        cwd=mainPath
    )

    assert result.returncode == 1
    assert "The c file needs to end with .c" in result.stderr