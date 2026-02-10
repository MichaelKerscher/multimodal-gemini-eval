# scripts/run_test.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lib.test_loader import load_testcases
from lib.test_runner import run_testcase  # NEW function (siehe unten)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Starte LLM-Tests (JSON oder CSV).")
    parser.add_argument("testfile", help="Pfad zur Testdatei (.json oder .csv)")
    parser.add_argument("--case", help="Optional: testcase_id filtern", default=None)
    parser.add_argument("--incident", help="Optional: incident_id filtern (CSV)", default=None)
    args = parser.parse_args()

    testcases = load_testcases(args.testfile)

    if args.case:
        testcases = [tc for tc in testcases if tc.get("test_id") == args.case]

    if args.incident:
        testcases = [
            tc for tc in testcases
            if (tc.get("input", {}).get("meta", {}).get("incident_id") == args.incident)
        ]

    if not testcases:
        raise SystemExit("[ERROR] Keine Testcases nach Filter übrig.")

    for tc in testcases:
        run_testcase(tc)
