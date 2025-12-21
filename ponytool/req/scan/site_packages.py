import subprocess
import json
from pathlib import Path


def get_site_packages(python: Path) -> list[Path]:
    cmd = [
        str(python),  # Оборачиваем в строку, чтобы subprocess не ругался
        "-c",
        "import site, json; print(json.dumps(site.getsitepackages()))"
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=True,
    )

    paths = json.loads(result.stdout.strip())
    return [Path(p) for p in paths]