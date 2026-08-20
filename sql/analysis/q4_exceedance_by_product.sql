--4) Which products carry the highest MRL exceedance rate?
SELECT p.product_name,COUNT(*) AS n_samples,
ROUND(AVG(s.exceeds_mrl::int) * 100, 2) AS exceedance_pct
FROM fact_samples s
JOIN dim_product p ON s.product_code = p.product_code
WHERE s.n_evaluated > 0
GROUP BY p.product_name
HAVING COUNT(*) >= 200
ORDER BY exceedance_pct DESC
LIMIT 20;