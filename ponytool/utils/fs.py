import subprocess


def _run_git(cmd: list[str]) -> str:
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return ""

def has_git_repo() -> bool:
    try:
        subprocess.run(
            ['git', 'rev-parse', '--is-inside-work-tree'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        return True
    except subprocess.CalledProcessError:
        # git возвращает ненулевой код, если команда неприменима вне репозитория
        return False

def repo_has_remote() -> bool:
    return bool(_run_git(['git', 'remote']))

def working_tree_has_changes() -> bool:
    return bool(_run_git(['git', 'status', '--porcelain']))
