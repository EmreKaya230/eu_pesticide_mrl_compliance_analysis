-- Follow-up: chia seeds showed the highest exceedance rate in Q5 (59% PY, 58% BO).
-- These queries check whether it is country specific or product-specific and which substances drive it.

-- 1) Is the pattern specific to one origin?
SELECT s.origin_country, COUNT(*) AS n_samples,
       ROUND(AVG(s.exceeds_mrl::int) * 100, 2) AS exceedance_pct
FROM fact_samples s
JOIN dim_product p ON s.product_code = p.product_code
WHERE p.product_name = 'Chia seeds' AND s.n_evaluated > 0
GROUP BY s.origin_country
ORDER BY n_samples DESC;

-- 2) Which substances cause the exceedances?
SELECT sub.substance_name, COUNT(*) AS n
FROM fact_results r
JOIN dim_product p ON r.product_code = p.product_code
JOIN dim_substance sub ON r.substance_code = sub.substance_code
WHERE p.product_name = 'Chia seeds' AND r.exceeds_mrl = true
GROUP BY sub.substance_name
ORDER BY n DESC;