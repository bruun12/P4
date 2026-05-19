import subprocess
import os
import sys
from pathlib import Path


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
    
    # Assert the stdout (program output)
    assert result == "1"

