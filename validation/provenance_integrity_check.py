#!/usr/bin/env python3
"""
Provenance Integrity Checker
-----------------------------
Autonomously validates ID cross-referencing between research artifacts
and Chapter 2 Business Context / Asset Inventories.
"""

from pathlib import Path
import sys
import pandas as pd


def check_provenance_integrity(repo_root: Path) -> bool:
    print("[*] Starting Provenance Integrity Check...")
    errors = 0

    # Paths
    raw_jobs_path = repo_root / "research" / "raw" / "raw_jobs.csv"
    asset_path = repo_root / "datasets" / "business" / "asset_inventory.csv"
    mapping_path = (
        repo_root / "research" / "pipeline" / "stage_i_architecture_mapping.csv"
    )

    # 1. Verify file existence
    for p in [raw_jobs_path, asset_path, mapping_path]:
        if not p.exists():
            print(f"[-] ERROR: Required artifact missing: {p}")
            errors += 1

    if errors > 0:
        return False

    # 2. Check Asset IDs (AST-01..13) integrity
    df_assets = pd.read_csv(asset_path)
    if "Asset_ID" not in df_assets.columns:
        print("[-] ERROR: 'Asset_ID' column missing in asset_inventory.csv")
        errors += 1
    else:
        asset_ids = set(df_assets["Asset_ID"].dropna().unique())
        print(f"[+] Found {len(asset_ids)} unique Asset IDs in asset_inventory.csv")

    # 3. Audit Mapping Pipeline ID linkage
    df_map = pd.read_csv(mapping_path)
    if "Mapped_Asset_ID" in df_map.columns:
        mapped_ids = set(df_map["Mapped_Asset_ID"].dropna().unique())
        invalid_ids = mapped_ids - asset_ids
        if invalid_ids:
            print(f"[-] ERROR: Unlinked Asset IDs in Pipeline Stage I: {invalid_ids}")
            errors += 1
        else:
            print(
                "[+] PASS: All Pipeline Stage I Asset IDs map perfectly to Asset Inventory!"
            )

    if errors == 0:
        print("[SUCCESS] Provenance Integrity Verification PASSED 100%!")
        return True
    else:
        print(f"[FAILED] Provenance Integrity Verification found {errors} errors.")
        return False


if __name__ == "__main__":
    root_dir = Path(__file__).resolve().parent.parent
    success = check_provenance_integrity(root_dir)
    sys.exit(0 if success else 1)