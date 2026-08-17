import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
from jobspy import scrape_jobs

# =====================================================
# PROJECT PATH
# =====================================================
BASE_DIR = Path.cwd()           # Colab: /content
DATA_DIR = BASE_DIR / "research" / "data"

DATA_DIR.mkdir(parents=True, exist_ok=True)

SEARCH_TERMS = [
    "IT Support",
    "IT Helpdesk",
    "IT Operations",
    "Junior Network Engineer",
    "System Administrator Intern",
]

HOURS_OLD = 24 * 14
RESULTS_PER_KEYWORD = 30
SITES = ["linkedin", "indeed", "glassdoor", "google"]


def collect_one_keyword(keyword: str):
    print(f"-> Đang cào dữ liệu cho keyword: {keyword}")

    try:
        df = scrape_jobs(
            site_name=SITES,
            search_term=keyword,
            location="Ho Chi Minh City, Vietnam",
            results_wanted=RESULTS_PER_KEYWORD,
            hours_old=HOURS_OLD,
            country_indeed="vietnam",
        )

        if df.empty:
            print(f"   Không có dữ liệu cho '{keyword}'")
            return None

        df["search_keyword"] = keyword
        print(f"   Thu được {len(df)} JD")

        return df

    except Exception as e:
        print(f"Lỗi với keyword '{keyword}': {e}")
        return None


# =====================================================
# Crawl song song
# =====================================================

if __name__ == "__main__":
    all_jobs = []

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(collect_one_keyword, kw): kw
            for kw in SEARCH_TERMS
        }

        for future in as_completed(futures):
            res = future.result()

            if res is not None:
                all_jobs.append(res)

    # =====================================================
    # Xuất dữ liệu
    # =====================================================

    if all_jobs:
        jobs = pd.concat(all_jobs, ignore_index=True)

        jobs = jobs.drop_duplicates(
            subset=["title", "company"]
        )

        useful_columns = [
            "title",
            "company",
            "location",
            "site",
            "job_url",
            "description",
            "search_keyword",
            "date_posted",
        ]

        useful_columns = [
            c for c in useful_columns if c in jobs.columns
        ]

        jobs = jobs[useful_columns]

        output_path = DATA_DIR / "raw_jobs.csv"

        jobs.to_csv(
            output_path,
            index=False,
            encoding="utf-8-sig",
        )

        print("=" * 60)
        print("HOÀN THÀNH CÀO DATA!")
        print(f"Tổng số JD: {len(jobs)}")
        print(f"Lưu tại: {output_path}")
        print("=" * 60)

    else:
        print("Không thu được dữ liệu.")
