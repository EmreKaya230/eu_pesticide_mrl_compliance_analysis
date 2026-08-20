-- 3) How have exceedance rates changed over time?
SELECT
    reporting_country,
    sample_year,
    COUNT(*) AS n_samples,
    ROUND(AVG(exceeds_mrl::int) * 100, 2) AS exceedance_pct
FROM fact_samples
WHERE n_evaluated > 0
  AND sample_year >= 2022
GROUP BY reporting_country, sample_year
ORDER BY reporting_country, sample_year;

-- I used  sample_year >= 2022 because starts at before 2022 , other countries are started at after 2022.
-- 3.1)Did France's evaluation coverage change over time?
SELECT
    reporting_country,
    sample_year,
    COUNT(*) AS n_samples,
    ROUND(AVG((n_evaluated = 0)::int) * 100, 2) AS pct_never_evaluated
FROM fact_samples
GROUP BY reporting_country, sample_year
ORDER BY reporting_country, sample_year;
