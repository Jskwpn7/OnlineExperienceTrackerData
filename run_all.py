"""One-command refresh: rebuild the whole OET explorer from raw/.
Run after adding a new wave's files to raw/ (and the refreshed merged file):
    python run_all.py
Chains the data pipeline then regenerates OET_explorer.html.
"""
import subprocess, sys, os

STEPS = [
    "oet_build_estimates.py",   # core Q7/Q8/Q32 (merged 4-9)
    "oet_backfill_w12.py",      # append waves 1-2
    "oet_followups.py",         # Tier 1-2 follow-ups
    "oet_followups2.py",        # Q14/Q22-29/attitudes
    "build_explorer.py",        # rebuild OET_explorer.html
]

os.chdir(os.path.dirname(os.path.abspath(__file__)))
for step in STEPS:
    print(f"\n=== running {step} ===", flush=True)
    r = subprocess.run([sys.executable, step])
    if r.returncode != 0:
        sys.exit(f"FAILED at {step}")
print("\nAll steps complete — OET_explorer.html rebuilt.")
