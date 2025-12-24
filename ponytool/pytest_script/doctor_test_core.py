import importlib.util
from pathlib import Path

BASE_FOLDER_NAMES = ['tests', 'test']

def _pytest_installed() -> bool:
    return importlib.util.find_spec("pytest") is not None

def _tests_dir_exists() -> Path | None:
    for name in BASE_FOLDER_NAMES:
        path = Path.cwd() / name
        if path.is_dir():
            return path
    return None

def _tests_found(test_dir: Path) -> bool:
    return any(test_dir.glob("test_*.py"))

def _pytest_cache_exists() -> bool:
    return (Path.cwd() / ".pytest_cache").exists()


def run_doctor_for_tests():
    tests_dir = _tests_dir_exists()

    return {
        "pytest_installed": _pytest_installed(),
        "tests_dir": tests_dir,
        "tests_found": _tests_found(tests_dir) if tests_dir else False,
        "pytest_cache": _pytest_cache_exists(),
    }
