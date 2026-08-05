# Module 07 — Glossary

| Term | Simple Meaning | Spotify Example |
|---|---|---|
| Scaling | Make feature magnitudes comparable | Minutes and skip rate |
| Transformation | Change data representation or shape | Yeo-Johnson |
| Standardization | Mean 0 and standard deviation 1 | StandardScaler |
| Min-Max Scaling | Map fitted values to a range | 0 to 1 |
| Robust Scaling | Median and IQR scaling | Power-user-resistant center |
| Mean | Average value | Average listening minutes |
| Standard Deviation | Spread around mean | Listening variation |
| Median | Middle value | Typical listener |
| IQR | Q3 minus Q1 | Central 50% spread |
| Skewness | Asymmetry | Long right listening tail |
| Log Transform | Compress large positive values | `log1p(minutes)` |
| Power Transform | Learned monotonic shape change | Yeo-Johnson |
| Quantile Transform | Rank-based mapping | Normal output |
| Fit | Learn parameters | Learn mean and standard deviation |
| Transform | Apply learned parameters | Scale future users |
| Inverse Transform | Return to original units | Scaled centroid to minutes |
| Pipeline | Ordered preprocessing and model | Scaler then K-Means |
| Leakage | Improper use of future/evaluation data | Fit on all periods |
| Euclidean Distance | Straight-line numeric distance | User-to-centroid distance |
| Bounded Output | Values kept in a selected range | MinMax 0 to 1 |
| Monotonic | Preserves ordering | Power transformation |
