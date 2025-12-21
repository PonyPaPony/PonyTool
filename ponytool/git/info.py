from pathlib import Path

from ponytool.utils.ui import info, success, warning, error
from ponytool.utils.fs import has_git_repo
from ponytool.utils.shell import run_output


def git_info(args):
    if not has_git_repo():
        error("Git-репозиторий не инициализирован")
        return

    # команды вызываются напрямую, чтобы вывод git не искажался
    root = get_root()
    repo = Path(root).name
    state = get_repo_state()
    branch = state["branch"]
    upstream = state["upstream"]
    dirty = state["dirty"]

    if args.short:
        print_short(branch, dirty, upstream)
        return

    print_full(repo, root, branch, upstream, dirty, args.verbose)


def get_repo_state():
    return {
        "branch": get_branch(),
        "upstream": get_upstream(),
        "dirty": is_dirty(),
    }


def get_root() -> str:
    return run_output(
        ['git', 'rev-parse', '--show-toplevel'],
        check=False
    ).strip()

def get_branch() -> str:
    return run_output(
        ['git', 'branch', '--show-current'],
        check=False
    ).strip() or "—"

def get_upstream() -> str:
    out = run_output(
        ['git', 'rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{u}'],
        check=False
    )
    return out.strip() if out else ""

def get_remotes() -> dict[str, str]:
    remotes = run_output(['git', 'remote', '-v'], check=False).strip()
    result = {}

    for line in remotes.splitlines():
        name, url, *_ = line.split()
        result[name] = url

    return result

def is_dirty() -> bool:
    return bool(run_output(
        ['git', 'status', '--porcelain'],
        check=False,
    ).strip())

def print_short(branch, dirty, upstream):
    status = 'dirty' if dirty else 'clean'
    up = upstream or 'no-upstream'
    print(f"{branch} | {status} | {up}")

def print_full(repo, root, branch, upstream, dirty, verbose):
    info(f"Репозиторий: {repo}")
    # verbose нужен только для диагностики, не для обычного вывода
    if verbose:
        info(f"Путь: {root}")

    info(f"Ветка: {branch}")
    print()

    has_a_problem(upstream, dirty)

def has_a_problem(upstream, dirty):
    remotes = get_remotes()
    if remotes:
        info("Remote:")
        for name, url in remotes.items():
            print(f" {name} -> {url}")
    else:
        warning("Remote не настроен")

    print()

    if upstream:
        success(f"Upstream: {upstream}")
    else:
        warning("Upstream не найден")

    if dirty:
        warning("Есть незакоммиченные изменения")
    else:
        success("Рабочая директория чистая")
