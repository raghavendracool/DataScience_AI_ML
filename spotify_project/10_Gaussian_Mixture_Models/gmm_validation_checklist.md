# Module 10 — GMM Validation Checklist

## Input

- [ ] Clean data loaded
- [ ] `user_id` separated
- [ ] Behavioral features selected
- [ ] Numerical types confirmed
- [ ] Missing values checked
- [ ] Infinite values checked
- [ ] Features scaled or transformed

## Search Space

- [ ] Component range documented
- [ ] Full covariance tested
- [ ] Tied covariance tested
- [ ] Diagonal covariance tested
- [ ] Spherical covariance tested
- [ ] Explicit initialization configured
- [ ] `n_init` documented
- [ ] `random_state` fixed
- [ ] `reg_covar` documented

## Evaluation

- [ ] AIC calculated
- [ ] BIC calculated
- [ ] Average log-likelihood calculated
- [ ] Convergence checked
- [ ] Iteration count checked
- [ ] Hard-label Silhouette calculated
- [ ] Component sizes reviewed
- [ ] Mixture weights reviewed
- [ ] Confidence distribution reviewed
- [ ] Boundary users reviewed
- [ ] Stability tested

## Interpretation

- [ ] Means profiled
- [ ] Covariances interpreted
- [ ] Hard-label behavior profiles created
- [ ] Demographics joined
- [ ] Persona names justified
- [ ] Business actions documented
- [ ] Uncertainty included in interpretation

## Reproducibility

- [ ] Feature order saved
- [ ] Scaler saved
- [ ] GMM model saved
- [ ] Experiment ID recorded
- [ ] Probability-column order saved
- [ ] Persona mapping versioned
