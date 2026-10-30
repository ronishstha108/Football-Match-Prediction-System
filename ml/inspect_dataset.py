"""
ml/inspect_dataset.py
---------------------
Phase 2: Dataset Inspection Script

This script inspects the downloaded La Liga match CSV files:
1. Loads each season file and displays its shape (rows, columns).
2. Verifies the presence of key columns needed for match prediction.
3. Checks the distribution of the target variable (FTR: Full Time Result).
4. Detects missing values in essential columns.
"""

import os
import glob
import pandas as pd

def inspect_datasets():
    # Path to dataset folder
    dataset_dir = os.path.join(os.path.dirname(__file__), "..", "dataset")
    csv_files = sorted(glob.glob(os.path.join(dataset_dir, "SP1_*.csv")))

    print("=" * 65)
    print("PHASE 2: DATASET INSPECTION REPORT")
    print("=" * 65)
    print(f"Found {len(csv_files)} season files in dataset folder.\n")

    if not csv_files:
        print("[ERROR] No CSV files found matching SP1_*.csv!")
        return

    # Key columns required for our 16 statistical features and target
    required_cols = [
        "Date", "HomeTeam", "AwayTeam", 
        "FTHG", "FTAG", "FTR",          # Goals & Result
        "HS", "AS",                     # Shots
        "HST", "AST",                   # Shots on Target
        "HC", "AC",                     # Corners
        "HF", "AF"                      # Fouls
    ]

    total_rows = 0
    dfs = []

    for file_path in csv_files:
        file_name = os.path.basename(file_path)
        try:
            # Read CSV using pandas
            df = pd.read_csv(file_path)
            dfs.append(df)
            total_rows += len(df)

            print(f"File: {file_name}")
            print(f"  - Matches (rows): {len(df)}")
            print(f"  - Total raw columns: {len(df.columns)}")

            # Check if all required columns exist in this file
            missing_in_file = [col for col in required_cols if col not in df.columns]
            if missing_in_file:
                print(f"  - [WARNING] Missing required columns: {missing_in_file}")
            else:
                print("  - All required match stat columns are PRESENT.")
            print()
        except Exception as e:
            print(f"  - [ERROR] Could not read {file_name}: {e}")

    # Combine all seasons for overall analysis
    all_data = pd.concat(dfs, ignore_index=True)
    print("-" * 65)
    print(f"TOTAL MATCHES COMBINED ACROSS 5 SEASONS: {total_rows}")
    print("-" * 65)

    # 1. Target variable distribution (FTR)
    print("\n1. TARGET VARIABLE DISTRIBUTION ('FTR'):")
    if "FTR" in all_data.columns:
        # Drop any nulls if matches are unfinished
        ftr_counts = all_data["FTR"].dropna().value_counts()
        ftr_percent = (all_data["FTR"].dropna().value_counts(normalize=True) * 100).round(2)
        summary_ftr = pd.DataFrame({"Count": ftr_counts, "Percentage (%)": ftr_percent})
        print(summary_ftr)
        print("\nNote: 'H' = Home Win, 'D' = Draw, 'A' = Away Win")
    else:
        print("[ERROR] 'FTR' column not found!")

    # 2. Check missing values in required columns
    print("\n2. MISSING VALUES IN REQUIRED COLUMNS:")
    existing_required = [col for col in required_cols if col in all_data.columns]
    missing_summary = all_data[existing_required].isnull().sum()
    print(missing_summary)

    # 3. Preview first 5 rows of key columns
    print("\n3. SAMPLE DATA (First 5 matches):")
    sample_cols = ["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR", "HS", "AS", "HST", "AST"]
    present_sample_cols = [c for c in sample_cols if c in all_data.columns]
    print(all_data[present_sample_cols].head())

    print("\n" + "=" * 65)
    print("INSPECTION COMPLETE")
    print("=" * 65)

if __name__ == "__main__":
    inspect_datasets()
