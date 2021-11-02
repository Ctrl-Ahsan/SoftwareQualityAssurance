from os import popen
from pathlib import Path
import subprocess

def test_login():
    current_folder = Path(__file__).parent
    expected_in = open(current_folder.joinpath('expected.in'), 'r')
    expected_out = open(current_folder.joinpath('expected.out'), 'r').read()
    
    output = subprocess.run(
        ['python3', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
    ).stdout.decode()

    assert output == expected_out