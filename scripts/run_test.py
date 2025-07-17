# scripts/run_test.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lib.test_runner import run_test_from_file

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Starte einen Gemini-Test.")
    parser.add_argument("testfile", help="Pfad zur Testdatei (JSON)")
    args = parser.parse_args()

    run_test_from_file(args.testfile)
