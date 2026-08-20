-- 2) Is the seasonal pattern in exceedance rates real, or driven by origin mix?
SELECT sample_month, COUNT(*) AS n_samples,
ROUND(AVG(exceeds_mrl::int) * 100, 2) AS exceedance_pct
FROM fact_samples
WHERE n_evaluated > 0
GROUP BY sample_month
ORDER BY sample_month;

-- 2.1) Does the pattern survive when origin group is held constant?
SELECT sample_month,origin_group,COUNT(*) AS n_samples,
ROUND(AVG(exceeds_mrl::int) * 100, 2) AS exceedance_pct
FROM fact_samples
WHERE n_evaluated > 0
GROUP BY sample_month, origin_group
ORDER BY sample_month, origin_group;

-- 2.2)  What share of samples come from outside the EU, by month?
SELECT sample_month,COUNT(*) AS n_samples,
ROUND(AVG((origin_group = 'NON_EU')::int) * 100, 2) AS non_eu_share_pct
FROM fact_samples
WHERE n_evaluated > 0
GROUP BY sample_month
ORDER BY sample_month;