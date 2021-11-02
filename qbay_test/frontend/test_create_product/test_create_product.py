from os import popen
from pathlib import Path
import subprocess

# get expected input/output file
current_folder = Path(__file__).parent


# read expected in/out
expected_in = open(current_folder.joinpath(
    'test_create_product.in'))
expected_out = open(current_folder.joinpath(
    'test_create_product.out')).read()

print(f'Expected: {expected_out}')


def test_login():
    """capsys -- object created by pytest to 
    capture stdout and stderr"""

    # pip the input
    output = subprocess.run(
        ['python3', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
    ).stdout.decode()

    print(f'OUTPUTS: {output}')
    assert output.strip() == expected_out.strip()