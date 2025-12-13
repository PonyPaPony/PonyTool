from ponytool.utils.shell import run
from ponytool.utils.fs import is_git_repo
from ponytool.utils.ui import info, warn, success


def git_info(args):
    if not is_git_repo():
        warn("Текущая директория не является git-репозиторием")
        return

    # branch
    branch = run(
        ["git", "branch", "--show-current"],
        capture=True
    ).strip()

    info(f"Ветка: {branch or 'detached'}")

    # remote
    remotes = run(
        ["git", "remote", "-v"],
        capture=True
    ).strip()

    if remotes:
        info("Remote:")
        print(remotes)
    else:
        warn("Remote не настроен")

    # status
    status = run(
        ["git", "status", "--porcelain"],
        capture=True
    )

    if not status.strip():
        success("Рабочая директория чистая")
    else:
        warn("Есть незакоммиченные изменения")

    # upstream / ahead-behind
    try:
        ab = run(
            ["git", "rev-list", "--left-right", "--count", "HEAD...@{upstream}"],
            capture=True
        ).strip()
        ahead, behind = ab.split()
        info(f"Upstream: ahead {ahead}, behind {behind}")
    except Exception:
        warn("Upstream не настроен")
