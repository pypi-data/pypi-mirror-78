from subprocess import check_output

import os


def get_pid(name):
    return check_output(["pidof", name])


def run(args):
    cmd = " ".join(args)
    print("[run]", cmd)
    return os.popen(cmd).read().strip()


def pgrep(pattern):
    """return a list with process IDs which matches the selection criteria"""
    args = ["pgrep", "-f", str(pattern)]
    out = os.popen(" ".join(args)).read().strip()
    result = list(map(int, out.splitlines()))
    return result


def path():
    args = ["echo", "$PATH"]
    out = run(args)
    print(out)


# Kills a process
def kill(pattern):
    """return a list with process IDs which matches the selection criteria"""
    args = ["kill", "-9", str(pattern)]
    out = os.popen(" ".join(args)).read().strip()


def check_and_kill_process(process_path):
    existing_pids = pgrep(process_path)
    print("existing_pids: ", existing_pids)
    if not existing_pids is None:
        for pid in existing_pids:
            print("found pid, killing", pid)
            kill(pid)


def clear_dir(directory):
    args = ["rm", "-rf", directory]
    out = run(args)
    print(out)


def mkdir(directory):
    args = ["mkdir", directory]
    out = run(args)
    print(out)
