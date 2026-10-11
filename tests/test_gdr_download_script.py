import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOWNLOADER = ROOT / "scripts" / "download_gdr_villa.py"


def test_gdr_downloader_help_is_available_without_network_access() -> None:
    result = subprocess.run(
        [sys.executable, str(DOWNLOADER), "--help"],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "clarcor-countercurrent" in result.stdout
    assert "all" in result.stdout
