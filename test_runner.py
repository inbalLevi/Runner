import subprocess
from os import path


def test_answer():
    assert call_successful_command(5) == 5
    assert call_successful_command(3) == 3
    assert call_unsuccessful_command(3) == 3
    assert call_unreachable_ping_with_failed_count_n_times(10, 3) == 3
    assert call_unreachable_ping_with_failed_count_n_times(5, 2) == 2
    assert check_logs() == True


def call_successful_command(n):
    """This test calls the script with -c COUNT and a surely successful
    (took ls -l for example). Then checks if we received
    n 'successful' responds"""

    count = 0
    command = ['python3', 'runner.py', 'ls', '-l', '-c', str(n)]
    process = subprocess.Popen(command, stderr=subprocess.PIPE,
                               stdout=subprocess.PIPE)
    out = process.communicate()
    clean_output = str(out).split('\\n')

    # check the first n lines is "google.com is reachable :)
    for line in clean_output:
        if ("The command succeded :)" in line):
            count += 1

    return count


def call_unsuccessful_command(n):
    """This test calls the script with an surely unsuccessful command
    (used "false") and checks if we received n 'failed' responds"""

    count = 0
    command = ['python3', 'runner.py', 'false', '-c', str(n)]
    process = subprocess.Popen(command, stderr=subprocess.PIPE,
                               stdout=subprocess.PIPE)
    out = process.communicate()
    clean_output = str(out).split('\\n')

    for line in clean_output:
        if ("The command failed :(" in line):
            count += 1

    return count


def call_unreachable_ping_with_failed_count_n_times(k, n):
    """This test calls the script with mkdir command, --failed-count
    N and '-c K' flags and checks if we received
    N 'failed' responds instead of k or (k-1) times (in the first run
    it will create the folder"""

    count = 0
    command = ['python3', 'runner.py', 'mkdir', 'example_file',
               '-c', str(k), '--failed-count', str(n)]
    process = subprocess.Popen(command, stderr=subprocess.PIPE,
                               stdout=subprocess.PIPE)
    out = process.communicate()
    clean_output = str(out).split('\\n')

    for line in clean_output:
        if ("The command failed :(" in line):
            count += 1

    return count


def check_logs():
    """This test calls the script with a command that will certainly fail
    if executed several times in a row (took mkdir for example).
    With --sys-trace --call-trace --log-trace and checks if we
    received 3 logs one of each flag command for 'unsuccessful' responds"""

    command = ['python3', 'runner.py', 'mkdir', 'example_file', '-c', '4',
               '--sys-trace', '--call-trace', '--log-trace']
    process = subprocess.Popen(command, stderr=subprocess.PIPE,
                               stdout=subprocess.PIPE)
    process.wait()
    return path.exists("sys_trace.log") and path.exists("sys_call.log") \
           and path.exists("output.log")


test_answer()
