from os import popen
from pathlib import Path
import subprocess

def test_login():
    stream = popen('python3 -m qbay < expected.in > captured.out')
    tmp = popen('pwd')
    print(tmp.read())
    tmp.close()
    expected_file = open('/qbay_test/frontend/test_create_product/expected.out', 'r')
    captured_file = open('/qbay_test/frontend/test_create_product/captured.out', 'r')
    
    assert expected_file.readlines() == captured_file.readlines()
    stream.close()
    # stream = popen('rm captured.out')
    # stream.close()