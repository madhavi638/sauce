# main.py
"""
Entry point for running TC-83 tests programmatically.

Usage:
    python main.py

Equivalent CLI command:
    pytest tests/test_tc83_valid_login.py \
        -v \
        --html=reports/pytest_script.html \
        --self-contained-html \
        --tb=short \
        -s
"""

import subprocess
import sys


if __name__ == "__main__":
    result = subprocess.run(
        [
            sys.executable, "-m", "pytest",
            "tests/test_tc83_valid_login.py",
            "-v",
            "--html=reports/pytest_script.html",
            "--self-contained-html",
            "--tb=short",
            "-s",
        ],
        capture_output=False,
    )
    sys.exit(result.returncode)
