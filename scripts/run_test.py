# scripts/run_test.py
import sys
import os
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lib.test_loader import load_testcases
from lib.test_runner import run_testcase, run_incident_group


def _run_mode_default() -> str:
    return os.getenv("TESTSUITE_RUN_MODE", "incident").strip().lower()


def _env_enable_judge_default() -> bool:
    return os.getenv("TESTSUITE_ENABLE_JUDGE", "true").strip().lower() == "true"


def _group_by_incident(testcases: list[dict]) -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for tc in testcases:
        meta = (tc.get("input", {}).get("meta") or {})
        incident_id = meta.get("incident_id", "UNKNOWN")
        groups[incident_id].append(tc)
    return groups


def _stable_sort_incident_group(group: list[dict]) -> list[dict]:
    return sorted(group, key=lambda x: x.get("test_id", ""))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Starte LLM-Tests (JSON oder CSV).")
    parser.add_argument("testfile", help="Pfad zur Testdatei (.json oder .csv)")
    parser.add_argument("--case", help="Optional: testcase_id filtern", default=None)
    parser.add_argument("--incident", help="Optional: incident_id filtern (CSV)", default=None)
    parser.add_argument(
        "--mode",
        help="Run mode: testcase oder incident (default aus TESTSUITE_RUN_MODE)",
        default=None,
        choices=["testcase", "incident"],
    )
    parser.add_argument(
        "--no-judge",
        help="Deaktiviert Judge für diesen Lauf (überschreibt TESTSUITE_ENABLE_JUDGE).",
        action="store_true",
    )
    args = parser.parse_args()

    run_mode = (args.mode or _run_mode_default()).lower()

    enable_judge = False if args.no_judge else _env_enable_judge_default()

    print(f"[RUN] mode={run_mode} | enable_judge={enable_judge} "
          f"(env TESTSUITE_ENABLE_JUDGE={os.getenv('TESTSUITE_ENABLE_JUDGE')}, --no-judge={args.no_judge})")

    testcases = load_testcases(args.testfile)

    # -------- filters --------
    if args.case:
        testcases = [tc for tc in testcases if tc.get("test_id") == args.case]

    if args.incident:
        testcases = [
            tc for tc in testcases
            if (tc.get("input", {}).get("meta", {}).get("incident_id") == args.incident)
        ]

    if not testcases:
        raise SystemExit("[ERROR] Keine Testcases nach Filter übrig.")

    # -------- execution --------
    if run_mode == "testcase":
        for tc in testcases:
            run_testcase(tc, enable_judge=enable_judge)
        raise SystemExit(0)

    groups = _group_by_incident(testcases)

    for incident_id in sorted(groups.keys()):
        group = _stable_sort_incident_group(groups[incident_id])
        run_incident_group(group, enable_judge=enable_judge)
