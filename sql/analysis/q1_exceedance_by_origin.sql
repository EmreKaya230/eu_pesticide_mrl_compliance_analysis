-- 1) Which countries of origin have the highest MRL exceedance rate?
SELECT origin_country,COUNT(*) AS n_samples,
ROUND(AVG(exceeds_mrl::int) * 100, 2) AS exceedance_pct
FROM fact_samples
WHERE n_evaluated > 0
GROUP BY origin_country
HAVING COUNT(*) >= 200
ORDER BY exceedance_pct DESC;