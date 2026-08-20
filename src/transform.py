"""Read raw SSD2 archives and write one cleaned parquet file per year/country."""

import zipfile
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"

COLS = [
    "sampId_A",                    # sample identifier
    "sampCountry",                 # country that took the sample
    "origCountry",                 # country of origin of the product
    "sampY", "sampM", "sampD",     # sampling date
    "sampMatCode.base.building",   # product code (FoodEx2)
    "paramCode.base.param",        # pesticide substance code
    "resVal",                      # measured value
    "resLOQ",                      # limit of quantification
    "resType",                     # LOQ = not detected, VAL = value reported
    "evalCode",                    # evaluation result (MRL exceedance)
]


def read_archive(zip_path: Path) -> pd.DataFrame:
    """Read the single CSV inside an SSD2 archive."""
    with zipfile.ZipFile(zip_path) as zf:
        inner = zf.namelist()[0]
        with zf.open(inner) as f:
            return pd.read_csv(f, usecols=COLS,
                               engine="pyarrow", dtype_backend="pyarrow")


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)

    for zip_path in sorted(RAW.glob("*/*.ZIP")):
        if not zipfile.is_zipfile(zip_path):
            print(f"  SKIP (corrupt) {zip_path.name}")
            continue

        out = PROCESSED / f"{zip_path.stem}.parquet"
        if out.exists():
            print(f"  skip           {out.name}")
            continue

        df = read_archive(zip_path)
        # EFSA uses "N_A" as a placeholder for missing values
        df = df.replace("N_A", None)
        df.to_parquet(out, index=False)
        print(f"  wrote          {out.name}  ({len(df):,} rows)")


if __name__ == "__main__":
    main()