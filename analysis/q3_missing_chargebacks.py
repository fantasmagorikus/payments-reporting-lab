from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "q3_missing_chargebacks.csv"


def main() -> None:
    acceptance = pd.read_csv(BASE_DIR / "acceptance.csv")
    chargebacks = pd.read_csv(BASE_DIR / "chargeback.csv")

    acceptance["external_ref"] = acceptance["external_ref"].astype(str)
    chargebacks["external_ref"] = chargebacks["external_ref"].astype(str)

    merged = acceptance.merge(
        chargebacks[["external_ref"]],
        on="external_ref",
        how="left",
        indicator=True,
    )

    missing = merged[merged["_merge"] == "left_only"][
        ["external_ref"]
    ].drop_duplicates()

    print("\nMissing chargebacks:\n")
    print(missing)

    missing.to_csv(OUTPUT, index=False)
    print(f"\nSaved to {OUTPUT.name}")


if __name__ == "__main__":
    main()
