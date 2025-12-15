from pathlib import Path
import ast

EXCLUDE_DIRS = {
    "venv",
    ".venv",
    "__pycache__",
    ".git",
}

def collect_imports(project_root: Path) -> set[str]:
    imports = set()

    for py_file in iter_python_files(project_root):
        imports |= extract_imports_from_file(py_file)

    return imports

def iter_python_files(root: Path):
    for path in root.rglob("*.py"):
        if is_excluded(path):
            continue
        yield path

def is_excluded(path: Path) -> bool:
    return any(part in EXCLUDE_DIRS for part in path.parts)

def extract_imports_from_file(path: Path) -> set[str]:
    result = set()

    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except Exception:
        return result  # битый файл — пропускаем

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                result.add(alias.name.split(".")[0])

        elif isinstance(node, ast.ImportFrom):
            # relative imports (from . / from ..) игнорируем — это локальный код
            if node.module:
                result.add(node.module.split(".")[0])

    return result
