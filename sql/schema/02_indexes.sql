-- Created after loading:
-- building indexes during insert slows the load down

CREATE INDEX idx_results_sample ON fact_results (sample_id);
CREATE INDEX idx_results_origin ON fact_results (origin_country);
CREATE INDEX idx_results_year ON fact_results (sample_year);
CREATE INDEX idx_results_product ON fact_results (product_code);

CREATE INDEX idx_samples_origin ON fact_samples (origin_country);
CREATE INDEX idx_samples_year ON fact_samples (sample_year);
CREATE INDEX idx_samples_product ON fact_samples (product_code);