import os
import sys
import subprocess  # For executing a shell command
import logging
import psutil

file_path = "sys_trace.log"
file_path2 = "sys_call.log"
file_path3 = "output.log"
file_path4 = "p.pcap"
return_codes_dict = {}


def print_details(debug=False):
    """Parameter: a bool variable debug, to check if debug mode is on.
    This function prints a usage message to STDERR explaining how the script
    should be used.
    """
    if debug:
        print('explaining how the script should be used')

    sys.stderr.write("Usage: runner.py 'terminal command' [-c COUNT] ["
                     "--failed-count N] [--sys-trace] [--call-trace] ["
                     "--log-trace] [--debug] [--net-trace]\n")
    sys.stderr.write("\nOptions:\n")
    sys.stderr.write("\t-c COUNT")
    sys.stderr.write("\t\tNumber of times to run the given command\n")
    sys.stderr.write("\t--failed-count N")
    sys.stderr.write("\tNumber of allowed failed command invocation attempts "
                     "before giving\n")
    sys.stderr.write("\t--sys-trace")
    sys.stderr.write("\t\tFor each failed execution, create a log for each "
                     "of the following values, measured during command "
                     "execution:\n")
    sys.stderr.write("\t\t\t\t\tDisk IO\n")
    sys.stderr.write("\t\t\t\t\tMemory\n")
    sys.stderr.write("\t\t\t\t\tProcesses/threads and cpu usage of the "
                     "command\n")
    sys.stderr.write("\t\t\t\t\tNetwork card package counters\n")
    sys.stderr.write("\t--call-trace")
    sys.stderr.write("\t\tFor each failed execution, add also a log with all "
                     "the system calls ran by the command\n")
    sys.stderr.write("\t--log-trace")
    sys.stderr.write("\t\tFor each failed execution, add also the command "
                     "output logs (stdout, stderr)\n")
    sys.stderr.write("\t--debug")
    sys.stderr.write("\t\tDebug mode, show each instruction executed by the "
                     "script\n")
    sys.stderr.write("\t--net-trace")
    sys.stderr.write("\t\tFor each failed execution, create a 'pcap' file "
                     "with the network traffic during the execution\n")


def activate(command, debug=False):
    """param A: command - bash command that the user enters.
    param B: count -  Number of times to run the given command
    param c: debug - a bool variable debug, for check if debug mode is on.
    returns: True or False
    Explanation: The user enters a command and it runs according to the number
    of times it is indicated by the count
    """

    if debug:
        print('The script runs number of times the given command')

    process = subprocess.call(command.split(' '))
    if not return_codes_dict.get(process):
        return_codes_dict[process] = 1
    else:
        return_codes_dict[process] += 1
    return process == 0


def setup_logger(logger_name, log_file, level=logging.INFO):
    """param A: logger_name: logger's name
    param B: log_file: the path file
    param c: level=logging.INFO : this log is from information type
    explanation: To setup as many loggers as you want.
    """
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s : %(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)


def get_sys_calls(command):
    """parameter: command - bash command that the user enters.
    returns: 'strace' output. 'strace' command prints to stderr and therefore
    the function activate 'strace' and catches that output from stderr.
    Explanation: For each failed execution, add also a log with all the system
    calls ran by the command.
    """
    execute = ['strace', '-e', 'trace=all'] + command.split(' ')
    out = subprocess.Popen(execute, stdout=subprocess.DEVNULL,
                           stderr=subprocess.PIPE)
    out.wait()
    if not return_codes_dict.get(out.returncode):
        return_codes_dict[out.returncode] = 1
    else:
        return_codes_dict[out.returncode] += 1
    return out.communicate()


def get_log_trace(command):
    """parameter: command - bash command that the user enters.
    returns: command output prints to stderr and stdout.
    explanation: For each failed execution, add also the command output
    logs (stdout,stderr).
    """
    out = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    out.wait()
    if not return_codes_dict.get(out.returncode):
        return_codes_dict[out.returncode] = 1
    else:
        return_codes_dict[out.returncode] += 1
    out, err = out.communicate()
    return out + err


def print_summary(return_codes_dict):
    """param : a dict of return codes with number of time received.
    explanation: Print a summary of the command return codes (how many
    times each return code happened), even if/when the script was
    interrupted (via ctrl+c or ‘kill’) in addition,returns the most
    frequent return code when exiting
    """

    if not len(return_codes_dict):
        print("No return codes have been received during the script")
        return

    values = list(return_codes_dict.values())
    common_return_code_times = max(values)

    keys = list(return_codes_dict.keys())

    for key in keys:
        if (return_codes_dict[key] == common_return_code_times):
            common_return_code = key
            break

    print("---Summary---")
    for key in keys:
        print("The return code " + str(key) + " was received " +
              str(return_codes_dict[key]) + " times during the executions")

    print("---")
    print("The most frequent return code is " + str(common_return_code)
          + " with " +
          str(common_return_code_times) + " times received")


def main():
    args = sys.argv
    command = args[1]

    attempts = 1  # default
    allowed_fails = attempts  # can fail as number of attempts
    num_of_fails = 0
    count = 0
    t = 0
    debug = False

    # check for "DEBUG" mode
    if '--debug' in args:
        debug = True
        print('Debug ON')

    # check num of wanted command attempts by user
    if '-c' in args:
        idx = args.index('-c')
        attempts = int(args[idx + 1])
        allowed_fails = attempts  # can fail as number of attempts

    # check for "HELP"
    if '--help' in args:
        print_details(debug)

    # check if user allows a certain number of fails
    if '--failed-count' in args:
        # get num of allowed fails from user
        idx = args.index('--failed-count')
        allowed_fails = int(args[idx + 1])
        if debug:
            print('The script prints number of allowed failed command '
                  'invocation attempts before giving up')

    # run the command by num of attempts and allowed fails
    # if the command fails, create logs by user's request
    while (num_of_fails < allowed_fails and count < attempts):

        if not activate(command, debug):
            num_of_fails += 1
            print("The command failed :(")
            if '--sys-trace' in args:

                # create log file
                Path_To_log = os.path.abspath(file_path)
                setup_logger('sys_trace', Path_To_log)
                log1 = logging.getLogger('sys_trace')

                # write to log
                log1.info(psutil.cpu_percent())
                log1.info(psutil.virtual_memory())
                log1.info(psutil.disk_io_counters())
                log1.info(psutil.net_io_counters())

                if debug and t < 1:
                    print(
                        'The script creates a sys_trace log for each of the'
                        'following values, measured during command execution:'
                        'Disk IO, Memory,Processes/threads and cpu usage of '
                        'the command,Network card package counters')

            if '--call-trace' in args:
                # create log file
                Path_To_log2 = os.path.abspath(file_path2)
                setup_logger('sys_call', Path_To_log2)
                log2 = logging.getLogger('sys_call')

                # write to log
                log2.info(get_sys_calls(command))

                if debug and t < 1:
                    print(
                        'The script creates a sys_call log with all the system'
                        'calls ran by the command')

            if '--log-trace' in args:
                # create log file
                Path_To_log3 = os.path.abspath(file_path3)
                setup_logger('output', Path_To_log3)
                log3 = logging.getLogger('output')

                # write to log
                log3.info(get_log_trace(command))

                if debug and t < 1:
                    print(
                        'the script adds the command output logs (stdout,'
                        'stderr)')

            if '--net-trace' in args:
                # For each failed execution, create a ‘pcap’ file with the
                # network traffic during the execution with the command:tcpdump
                execute = ['tcpdump', '-i', 'any', '-c' '10',
                           '-nn', '-v',
                           '-w', 'trrafic_network.pcap']
                pcap_process = subprocess.Popen(execute,
                                                stdout=subprocess.DEVNULL,
                                                stderr=subprocess.PIPE)

                pcap_process.wait()
                if not return_codes_dict.get(pcap_process.returncode):
                    return_codes_dict[pcap_process.returncode] = 1
                else:
                    return_codes_dict[pcap_process.returncode] += 1

                if debug and t < 1:
                    print(
                        'The script creates a ‘pcap` file with the '
                        'network traffic during the execution')

        else:
            print("The command succeded :)")
        t += 1
        count += 1

    print_summary(return_codes_dict)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        # print summary of return codes when ctrl+c is activated
        print_summary(return_codes_dict)
