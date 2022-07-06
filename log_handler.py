import os, sys
from datetime import datetime


def open_log_file(logname):
    old_stdout = sys.stdout
    log_folder = os.path.join(os.getcwd(), 'logs')
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    log_file = open(f"{os.path.join(log_folder, logname)}.log","a")
    sys.stdout = log_file
    return old_stdout, log_file


def print_log_msg(*args):
    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+":")
    print(f"\t",end="")
    print(*args)


def close_log_file(old_stdout, log_file):
    sys.stdout = old_stdout
    log_file.close()
    return
