
import logging
import subprocess


def run_process(cmd, with_shell=False):
    '''
    run a process and wait for it to complete
    '''
    try:
        proc = subprocess.Popen(cmd, shell=with_shell)
        proc.communicate()
        print(proc.stdout)
        print(proc.stderr)
        print(proc.returncode)
        return proc.returncode
    except Exception as e:
        logging.error(e)
        raise Exception("Could not run Command [{0}]".format(cmd))
        return 1

