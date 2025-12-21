import sys
from pathlib import Path


def get_python() ->  dict[str, Path | None]:
    python = Path(sys.executable)  # получаем путь к активному venv

    if sys.prefix != sys.base_prefix:
        return {
            "python": python,
            'venv': Path(sys.prefix),
        }
    return {
        "python": python,
        'venv': None
    }