# Module 07 — Scaler Selection Checklist

## Before Scaling

- [ ] `user_id` removed
- [ ] Numeric features selected
- [ ] Missing values handled
- [ ] Infinite values handled
- [ ] Feature units documented
- [ ] Feature ranges documented
- [ ] Skewness calculated
- [ ] Outliers investigated

## Candidate Methods

- [ ] StandardScaler baseline
- [ ] MinMaxScaler where bounded output is useful
- [ ] RobustScaler for outlier-heavy distributions
- [ ] Log1p for non-negative right-skewed variables
- [ ] PowerTransformer for skewness
- [ ] QuantileTransformer only when justified

## Correct Fitting

- [ ] Fit on reference/training data
- [ ] Future data uses `transform()`
- [ ] Feature order preserved
- [ ] Same scaler reused
- [ ] Scaler saved with version

## Validation

- [ ] Row count unchanged
- [ ] Column count unchanged
- [ ] No missing values created
- [ ] No infinite values created
- [ ] Expected mean/range checked
- [ ] Distribution plotted
- [ ] Cluster metrics compared
- [ ] Business profiles compared
- [ ] Final decision documented
