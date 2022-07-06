import sys, subprocess, os
import pkg_resources
from log_handler import print_log_msg
from log_handler import open_log_file, close_log_file



def set_env(required, req_env, logfile=sys.stdout):

    old_stdout, log_file = open_log_file(logfile)

    print_log_msg("Setting environment...")

    def install(name):
        subprocess.call(['pip', 'install', name])

    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed

    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', '--upgrade', 'pip'], stdout=subprocess.DEVNULL)

    for missing_pkg in missing:
        try:
            subprocess.check_call([python, '-m', 'pip', 'install', missing_pkg], stdout=subprocess.DEVNULL)
            print("\t\tInstalled", missing_pkg)
        except Exception as e:
            print_log_msg("Unable to install", missing_pkg, "because of error", e)

    for env_var in req_env:
        if os.getenv(env_var) is None:
            try:
                os.environ[env_var] = input(f"Input {env_var}: ")
            except Exception as e:
                print_log_msg("Unable to get environment variable", env_var, "because of error", e)

    print_log_msg("Environment Set.")
    close_log_file(old_stdout, log_file)
