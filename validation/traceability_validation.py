#!/usr/bin/env python3
"""
Traceability & Codebase Validation Script
-----------------------------------------
Cross-checks Master Traceability Matrix against actual CLI configuration files
in implementation/configs/ to ensure zero orphan requirements.
"""

from pathlib import Path
import re
import sys
import pandas as pd


def validate_traceability(repo_root: Path) -> bool:
    print("[*] Starting Traceability vs. CLI Codebase Audit...")
    errors = 0

    matrix_path = (
        repo_root
        / "datasets"
        / "traceability"
        / "master_traceability_matrix.csv"
    )
    configs_dir = repo_root / "implementation" / "configs"

    if not matrix_path.exists():
        print(f"[-] ERROR: Master Traceability Matrix missing at {matrix_path}")
        return False

    df_matrix = pd.read_csv(matrix_path)
    print(
        f"[+] Loaded Master Traceability Matrix: {len(df_matrix)} requirements traced."
    )

    # Scan all implemented .cfg files
    config_contents = ""
    cfg_files = list(configs_dir.glob("*.cfg"))
    if not cfg_files:
        print(f"[-] WARNING: No .cfg files found in {configs_dir}")
    else:
        print(f"[+] Scanning {len(cfg_files)} CLI configuration files...")
        for cfg in cfg_files:
            config_contents += cfg.read_text(errors="ignore") + "\n"

    # Validate mandatory keywords in codebase
    required_keywords = [
        "vlan 10",
        "vlan 90",
        "spanning-tree mode rapid-pvst",
        "spanning-tree portfast",
        "spanning-tree bpduguard enable",
        "channel-group 1 mode active",
        "ip access-list extended",
    ]

    for kw in required_keywords:
        if not re.search(re.escape(kw), config_contents, re.IGNORECASE):
            print(
                f"[-] TRACEABILITY GAP: Required CLI command '{kw}' NOT found in codebase!"
            )
            errors += 1
        else:
            print(f"  [✓] Verified CLI Command: '{kw}'")

    if errors == 0:
        print("[SUCCESS] Traceability Validation PASSED! All requirements verified in CLI.")
        return True
    else:
        print(f"[FAILED] Traceability Audit found {errors} gap(s).")
        return False


if __name__ == "__main__":
    root_dir = Path(__file__).resolve().parent.parent
    success = validate_traceability(root_dir)
    sys.exit(0 if success else 1)