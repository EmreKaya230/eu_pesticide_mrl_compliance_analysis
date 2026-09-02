# EU Pesticide MRL Compliance Analysis

## Tableau Dashboard

(tableau_dashboard.png)


I started with a big question: does what we eat affect our health in the long
run? That question is too big for public data. You would need to measure what
each person actually eats, not country totals.

So I made it smaller and asked something the data can answer: how often do
pesticide residues in European food go over the legal limit, and does it change
by product and by country of origin?

The data comes from EFSA, the EU food safety agency. Every year, member states
test food samples for pesticide residues and report the results. EFSA publishes
the raw data on Zenodo REST API.

**Note:** this project measures regulatory non compliance, not health risk. An
MRL (Maximum Residue Level) is a legal limit based on good farming practice, not
a safety limit. A sample can go over the MRL and still be safe to eat.

**Stack:** Python · PostgreSQL ·API · Tableau




**[Interactive dashboard on Tableau Public →](https://public.tableau.com/views/EUPesticideMRLCompliance_1/EUPesticideMRLCompliance?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)**

---

## The questions

**Q1. Which origin countries have the highest exceedance rate?**
Helps decide where to focus supplier checks.

**Q2. Is there a seasonal pattern?**
Helps decide how to spread quality control budget across the year.

**Q3. How have exceedance rates changed over time?**
Helps decide whether things are getting better or worse.

**Q4. Which products have the highest exceedance rate?**
Helps decide which categories need extra sampling.

**Q5. Which product–origin combinations are riskiest?**
The most actionable question: what to check, and from where.

---

## Data

| | |
|---|---|
| Source | EFSA pesticide residue monitoring (Zenodo, CC-BY 4.0) |
| Countries | Spain (2020–2024), Germany (2022–2024), France (2022–2024) |
| Format | SSD2, the standard EFSA reporting model |
| Size | 32.4 million analysis rows, 103,820 samples |

One sample is tested for around 300 different pesticides, so the number of rows
is much larger than the number of samples. All rates in this project are
calculated per sample, not per row.

Pre 2019 files use an older format with different columns. They were left out to
avoid mapping errors.

---

## How it works

```
Zenodo API  ──►  extract.py   download the raw archives
                     │
                     ▼
                transform.py  read, clean, save as parquet
                     │
                     ▼
                  load.py     load into PostgreSQL (COPY)
                     │
                     ▼
              sql/analysis/   the five questions
                     │
                     ▼
                  Tableau     dashboard
```

### Tables

- `fact_results` - one row per analysis (32.4M)
- `fact_samples` -  one row per sample (103,820), pre-aggregated so the dashboard
  stays fast
- `dim_product` - product codes to names (from the EFSA FoodEx2 catalogue)
- `dim_substance` - pesticide codes to names (from the EFSA PARAM catalogue)

---

## What I found
All findings below are also available as an
[interactive dashboard](https://public.tableau.com/views/EUPesticideMRLCompliance_1/EUPesticideMRLCompliance?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)
### Origin matters much more than season

At first the data looks seasonal: about 4.7% in January and 3.3% in September.
But if you split by origin the two groups look very different. EU samples stay
flat around 1.6% all year. Non-EU samples are much higher, between 7.5% and
10.6%, and they move up and down without a clear seasonal shape.

The winter peak comes from what gets tested, not from the season. In December
non-EU samples are about 31% of all testing, in September only 18%. Europe tests
its own produce in summer and switches to imports in winter, so the average
follows the mix.

So the answer to Q2 is: plan controls by origin, not by month.

### Highest-risk origins

| Origin | Samples | Exceedance |
|---|---|---|
| Sri Lanka | 318 | 28.6% |
| Vietnam | 732 | 21.7% |
| Pakistan | 228 | 21.5% |
| Thailand | 248 | 13.7% |
| India | 2,371 | 12.1% |

EU average is 3.6%.

### Highest-risk products

Tropical fruit leads: pitaya 28.6%, passionfruit 21.2%, papaya 20.7%.

Tea and dried products also score high (9–14%). This makes sense drying
concentrates whatever residue was on the fresh leaf.

French beans stand out because of volume: 2,036 samples at 7.1%. Most other
high-rate products only have a few hundred samples.

### Chia seeds: the clearest single finding

Chia seeds have the highest rate of any product origin combination (59% from
Paraguay, 58% from Bolivia). The same pattern shows up in two separate countries,
so it is not a one-country problem.

Looking at which substances caused it: **119 of 123 exceedances are copper
compounds**. Paraquat appears 3 times, haloxyfop once.

Copper is an approved fungicide and is allowed even in organic farming. So this
is not a banned-pesticide story it is more likely that the MRL for copper on
chia is set at a level that normal production regularly exceeds. This is a good
example of why MRL exceedance and health risk are not the same thing.

### Trends

| Country | 2022 | 2023 | 2024 |
|---|---|---|---|
| Germany | 4.64% | 3.44% | 2.35% |
| France | 3.71% | 3.49% | 5.37% |
| Spain | 1.66% | 2.94% | 2.32% |

Germany's numbers fall steadily, but see the limitations below before reading
that as good news.

---

## Limitations

**Germany's evaluation coverage is dropping.** The share of German samples with
no evaluated result rose from 8.7% to 12.0% between 2022 and 2024, at the same
time as its exceedance rate fell. Unevaluated samples are excluded from the rate,
so part of the "improvement" may just be a reporting change. I could not tell the
two apart from this data.

**Germany reports no origin for 17% of its samples** (9,441 of about 55,000),
against under 1% for Spain. Anything broken down by origin therefore
under-represents German sampling.

**Origin is unknown for 10,134 samples overall.** These are kept as a separate
`UNKNOWN` group rather than hidden inside non EU.

**A high rate does not mean unsafe food.** These numbers show how often samples
break the legal limit, not how safe a country's food is. Countries also choose
what to test, and shipments they already suspect get tested more often, which
pushes their rate up.

**Minimum sample thresholds are arbitrary.** I used 200 samples for
product/origin lists and 50 for combinations. Lower thresholds fill the list with
noise; higher ones hide interesting cases.

**Small things I checked and left alone:** 3 samples (of 103,820) are reported
against two product codes each. 3 product codes out of 1,353 have no name in the
catalogue version I used. 111 UK-origin samples are treated as non EU throughout.

---

## Notes on method

Rates are always calculated at sample level. A sample counts as exceeding if any
of its analyses exceeded.

Samples with no evaluated result are excluded from both the numerator and the
denominator. Leaving them in pulls every rate down it changed the overall
figure from 3.60% to 3.38%.

Two different metrics exist and they are not the same:
- **exceedance** — above the MRL (`J003A` or `J031A`)
- **non-compliance** — above the MRL beyond measurement uncertainty (`J003A`)

Overall figures: 3.6% exceedance, 2.0% non-compliance. These are close to what
EFSA publishes, which was a useful check that the pipeline works.

Missing values in `result_value` and `loq` were **not** filled in. A missing
result value means no residue was detected, not that data is missing. Filling it
with zero would invent a measurement that was never taken.

---

## Running it

```bash
git clone <repo>
cd eu-pesticide-mrl-compliance

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` from `.env.example` and fill in your database details.

```bash
# 1. create the tables
psql -d pesticides -f sql/schema/01_create_tables.sql

# 2. run the pipeline
python -m src.extract      # download from Zenodo (~1.7 GB)
python -m src.transform    # clean and save as parquet
python -m src.load         # load into PostgreSQL
python -m src.catalogues   # load the code lookup tables

# 3. create the indexes, after loading
psql -d pesticides -f sql/schema/02_indexes.sql
```

Indexes come after the load, not before. If they exist while you insert, every new
row has to update them and the load gets much slower.

Loading uses `COPY` instead of `to_sql`. Inserting row by row took hours for 32
million rows; `COPY` takes about ten minutes.


## Repo layout

```
src/          extract, transform, load, catalogues, db connection
sql/schema/   table definitions and indexes
sql/analysis/ one file per question
notebooks/    exploration and cleaning
data/         raw and processed (not in git)
```

---

## Source

EFSA pesticide residue monitoring data, published on Zenodo under CC-BY 4.0.
Product and substance names come from the EFSA FoodEx2 (MTX) and PARAM
catalogues, available at github.com/openefsa/efsa-catalogues.
