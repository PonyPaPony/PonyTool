import sys
from pathlib import Path

COMMON_VENV_NAMES = [
    '.venv',
    'venv',
    'env'
]


def find_active_venv() -> Path | None:
    return Path(sys.prefix) if sys.prefix != sys.base_prefix else None


def find_local_venv(root: Path) -> Path | None:
    for name in COMMON_VENV_NAMES:
        candidate = root / name
        cfg_file = candidate / 'pyvenv.cfg'  # Папок venv может быть много, но мы ищем именно ту где есть pyvenv.cfg
        if candidate.exists() and cfg_file.exists():
            return candidate
    return None


def search_parents(root: Path) -> Path | None:
    for parent in [root, *root.parents]:
        for name in COMMON_VENV_NAMES:
            candidate = parent / name
            if (candidate / 'pyvenv.cfg').exists():
                return candidate
    return None


def find_venv(root: Path | None = None) -> Path | None:
    return (
            find_active_venv()
            or find_local_venv(root or Path.cwd())
            or search_parents(root or Path.cwd())
    )
