from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "q2_declined_countries.csv"


def main() -> None:
    df = pd.read_csv(BASE_DIR / "acceptance.csv")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    declined = df[df["state"] == "DECLINED"]
    totals = declined.groupby("country")["amount"].sum().reset_index()

    high = totals[totals["amount"] > 25_000_000].sort_values(
        "amount", ascending=False
    )

    print("\nCountries with more than 25M declined:\n")
    print(high)

    high.to_csv(OUTPUT, index=False)
    print(f"\nSaved to {OUTPUT.name}")


if __name__ == "__main__":
    main()
