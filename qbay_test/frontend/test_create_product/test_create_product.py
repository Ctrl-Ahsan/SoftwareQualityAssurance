from os import popen
from pathlib import Path
import subprocess

def test_login():
    stream = popen('python3 -m qbay < expected.in > captured.out')

    current_folder = Path(__file__).parent
    expected_file = open(current_folder.joinpath('expected.out'), 'r')
    captured_file = open(current_folder.joinpath('captured.out'), 'r')
    
    assert expected_file.readlines() == captured_file.readlines()
    stream.close()
    # stream = popen('rm captured.out')
    # stream.close()