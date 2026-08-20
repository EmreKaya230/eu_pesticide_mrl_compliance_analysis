# Load the cleaned dataset into PostgreSQL
# it's my first time using copy I learned this copy method when I am working on this project.
# I used copy because to_sql sends one INSERT per row, which takes more than hours for 32M rows.
# and COPY streams the data in one command instead around 10x faster.
import io
import pandas as pd
from pathlib import Path
from src.db import get_engine

PROCESSED = Path(__file__).resolve().parent.parent / "data" / "processed"

RESULT_COLS = [
    "sample_id", "reporting_country", "origin_country", "origin_group",
    "sample_date", "sample_year", "sample_month",
    "product_code", "substance_code",
    "result_value", "loq", "result_type", "eval_code",
    "evaluated", "exceeds_mrl", "non_compliant",
]


def load_results(df, engine):
    # COPY is much faster than INSERT for large tables
    connection = engine.raw_connection()
    cursor = connection.cursor()

    columns = ", ".join(RESULT_COLS)
    chunk_size = 2_000_000

    # Load in chunks so memory stays low
    for start in range(0, len(df), chunk_size):
        chunk = df.iloc[start:start + chunk_size][RESULT_COLS]

        # Write the chunk to a CSV in memory instead of a file on disk
        buffer = io.StringIO()
        chunk.to_csv(buffer, index=False, header=False, na_rep="\\N")
        buffer.seek(0)

        sql = f"COPY fact_results ({columns}) FROM STDIN WITH CSV NULL '\\N'"
        cursor.copy_expert(sql, buffer)
        connection.commit()

        print("loaded:", start + len(chunk))

    connection.close()


def build_samples(df):
    # One row per sample instead of one row per analysis
    samples = df.groupby("sample_id").agg(
        reporting_country=("reporting_country", "first"),
        origin_country=("origin_country", "first"),
        origin_group=("origin_group", "first"),
        sample_date=("sample_date", "first"),
        sample_year=("sample_year", "first"),
        sample_month=("sample_month", "first"),
        product_code=("product_code", "first"),
        n_analyses=("eval_code", "size"),
        n_evaluated=("evaluated", "sum"),
        exceeds_mrl=("exceeds_mrl", "max"),
        non_compliant=("non_compliant", "max"),
    )
    return samples.reset_index()


def main():
    engine = get_engine()

    df = pd.read_parquet(PROCESSED / "samples_clean.parquet")
    print("rows:", len(df))

    print("loading fact_results...")
    load_results(df, engine)

    print("loading fact_samples...")
    samples = build_samples(df)
    samples.to_sql("fact_samples", engine, if_exists="append", index=False)
    print("samples:", len(samples))

    print("done")


if __name__ == "__main__":
    main()