"""Download EFSA pesticide residue monitoring data (SSD2) from Zenodo."""

import requests
from pathlib import Path

RAW = Path(__file__).resolve().parent.parent / "data" / "raw"

COUNTRY_RECORDS = {
    "ES": 20036085,
    "DE": 11043863,
    "FR": 15398969,
}

YEARS = range(2022, 2025)


def list_versions(record_id: int) -> list[dict]:
    """Return all published versions of a Zenodo record."""
    r = requests.get(
        f"https://zenodo.org/api/records/{record_id}/versions",
        params={"size": 20},
        timeout=60,
    )
    r.raise_for_status()
    return r.json()["hits"]["hits"]


def download_ssd2(country: str, record_id: int) -> None:
    """Download one SSD2 archive per year for a given reporting country."""
    out = RAW / country.lower()
    out.mkdir(parents=True, exist_ok=True)

    wanted = {f"MOPER_ALL_DATA_SSD2_{y}_{country}.ZIP" for y in YEARS}
    seen = set()

    versions = list_versions(record_id)
    print(f"--- {country}: {len(versions)} versions found")

    for version in versions:
        for f in version.get("files", []):
            name = f["key"]
            if name not in wanted or name in seen:
                continue
            seen.add(name)

            dest = out / name
            if dest.exists():
                print(f"  skip     {name}")
                continue

            print(f"  download {name} ({f['size'] / 1e6:.1f} MB)")
            with requests.get(f["links"]["self"], stream=True, timeout=300) as r:
                r.raise_for_status()
                with dest.open("wb") as fh:
                    for chunk in r.iter_content(1 << 20):
                        fh.write(chunk)

    missing = sorted(wanted - seen)
    if missing:
        print(f"  NOT FOUND: {missing}")


if __name__ == "__main__":
    for code, rid in COUNTRY_RECORDS.items():
        download_ssd2(code, rid)