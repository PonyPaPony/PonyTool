import subprocess

def run(cmd, check=True) -> None:
    subprocess.run(cmd, check=check)

def run_output(cmd, check=True) -> str:
    return subprocess.check_output(
        cmd,
        text=True,
        stderr=subprocess.STDOUT,
    ).strip()

def check(cmd) -> bool:
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False
