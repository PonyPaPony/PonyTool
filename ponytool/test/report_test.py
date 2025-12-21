import json
from json import JSONDecodeError
from pathlib import Path
from datetime import datetime

REPORT_DIR = Path(".pony")
REPORT_FILE = REPORT_DIR / "tests_report.json"

def save_test_report(passed: bool, failed: int | None = None) -> None:
    REPORT_DIR.mkdir(exist_ok=True)

    data = {
        "last_run": datetime.now().isoformat(timespec="seconds"),
        "passed": passed,
        "failed": failed,
    }

    REPORT_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

def load_test_report() -> dict | None:
    if not REPORT_FILE.exists():
        return None

    try:
        return json.loads(REPORT_FILE.read_text(encoding="utf-8"))
    except JSONDecodeError:
        return None
