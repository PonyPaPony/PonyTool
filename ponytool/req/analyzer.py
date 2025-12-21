from pathlib import Path
from ponytool.req.packages import (
    match_packages,
    find_unmatched_imports,
    find_unused_packages,
)


def analyze(
        imports: dict[str, set[Path]],
        installed: dict[str, str],
) -> dict[str, object]:
    matched = match_packages(imports, installed)

    matched_names = set(matched.keys())

    unmatched = find_unmatched_imports(
        imports=set(imports.keys()),
        matched_packages=matched_names,
    )

    unused = find_unused_packages(
        installed=installed,
        matched_packages=matched_names,
    )

    return {
        "matched": matched,
        "unmatched_imports": unmatched,
        "unused_packages": unused,
    }
