CREATE TABLE dim_product(
    product_code  TEXT PRIMARY KEY ,
    product_name TEXT
);

CREATE TABLE dim_substance(
    substance_code TEXT PRIMARY KEY,
    substance_name TEXT
);

CREATE TABLE fact_results(
    sample_id TEXT,
    reporting_country TEXT,
    origin_country TEXT,
    origin_group TEXT,
    product_code TEXT,
    substance_code TEXT,
    result_type TEXT,
    eval_code TEXT,
    sample_date DATE,
    sample_year SMALLINT,
    sample_month SMALLINT,
    result_value FLOAT,
    loq FLOAT,
    evaluated BOOLEAN,
    exceeds_mrl BOOLEAN,
    non_compliant BOOLEAN

);

CREATE TABLE fact_samples(
    sample_id TEXT PRIMARY KEY,
    reporting_country TEXT,
    origin_country TEXT,
    origin_group TEXT,
    product_code TEXT,
    sample_date DATE,
    sample_year INTEGER,
    sample_month INTEGER,
    n_analyses INTEGER,
    n_evaluated INTEGER,
    exceeds_mrl BOOLEAN,
    non_compliant BOOLEAN
);
