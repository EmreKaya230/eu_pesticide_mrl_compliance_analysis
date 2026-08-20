# Parse EFSA catalogue files (.ecf) into lookup tables

import zipfile
import xml.etree.ElementTree as ET
import pandas as pd
from pathlib import Path
from src.db import get_engine

CATALOGUES = Path(__file__).resolve().parent.parent / "data" / "raw" / "catalogues"


def parse_catalogue(path, code_col, name_col):
    # .ecf is a zip holding one large XML file
    zf = zipfile.ZipFile(path)
    inner = zf.namelist()[0]

    rows = []
    # iterparse reads the file piece by piece instead of loading it all at once
    for event, element in ET.iterparse(zf.open(inner), events=("end",)):
        if element.tag == "term":
            desc = element.find("termDesc")
            if desc is not None:
                rows.append({
                    code_col: desc.findtext("termCode"),
                    name_col: desc.findtext("termExtendedName"),
                })
            element.clear()

    zf.close()
    return pd.DataFrame(rows)


def main():
    engine = get_engine()

    products = parse_catalogue(
        CATALOGUES / "MTX_FULL_12_0.ecf", "product_code", "product_name"
    )
    print("products:", len(products))
    products.to_sql("dim_product", engine, if_exists="append", index=False)

    substances = parse_catalogue(
        CATALOGUES / "PARAM_FULL_10_25.ecf", "substance_code", "substance_name"
    )
    print("substances:", len(substances))
    substances.to_sql("dim_substance", engine, if_exists="append", index=False)

    print("done")


if __name__ == "__main__":
    main()