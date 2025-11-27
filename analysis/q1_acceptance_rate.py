from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "q1_acceptance_rate.csv"


def main() -> None:
    df = pd.read_csv(BASE_DIR / "acceptance.csv")

    # Normalize timestamps for monthly aggregation
    df["date_time"] = pd.to_datetime(df["date_time"])
    df["month"] = df["date_time"].dt.to_period("M").dt.to_timestamp()

    monthly = df.groupby("month")["state"].agg(
        total="count",
        accepted=lambda x: (x == "ACCEPTED").sum(),
    ).reset_index()

    monthly["acceptance_rate"] = (
        monthly["accepted"] / monthly["total"] * 100
    ).round(2)

    print("\nAcceptance rate by month:\n")
    print(monthly)

    monthly.to_csv(OUTPUT, index=False)
    print(f"\nSaved to {OUTPUT.name}")


if __name__ == "__main__":
    main()
