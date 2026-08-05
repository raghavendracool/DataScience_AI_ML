# Module 04 — Glossary

| Term | Simple Meaning | Spotify Example |
|---|---|---|
| Data Cleaning | Fixing data-quality problems | Correcting invalid skip rates |
| Preprocessing | Preparing data for analysis/modeling | Scaling features |
| Missing Value | Information is unavailable | Missing device type |
| Fill Rate | Percentage of available values | 100% in current dataset |
| Imputation | Replacing missing values | Fill age with median |
| Duplicate Row | Repeated full record | Same user row twice |
| Duplicate Key | Repeated identifier | Same `user_id` twice |
| Wrong Data Type | Incorrect technical storage type | Age stored as text |
| Invalid Value | Impossible value | Skip rate above 1 |
| Inconsistent Value | Same meaning, different format | `mobile` and `Mobile` |
| Range Validation | Minimum/maximum check | Days active between 0 and 30 |
| Outlier | Unusually extreme value | Very high listening minutes |
| IQR | Interquartile Range | Outlier boundary method |
| Primary Key | Unique and non-null identifier | `user_id` |
| Business Rule | Domain validation rule | Age between 18 and 70 |
| Schema Check | Required structure validation | 26 behavior columns |
| Decision Log | Cleaning action record | Why a row was removed |
| Audit Trail | History of changes | Before/after counts |
| Quarantine | Separate suspicious data | Invalid user records |
| Winsorization | Cap extreme values | Limit very high minutes |
