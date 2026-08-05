# Module 11 — Experiment Automation Checklist

## Configuration

- [ ] Feature sets defined
- [ ] Preprocessors defined
- [ ] Transformations defined
- [ ] K values defined
- [ ] GMM component values defined
- [ ] Covariance types defined
- [ ] Random states defined
- [ ] Silhouette sample size defined

## Code Design

- [ ] Input validation function
- [ ] Preprocessor factory
- [ ] Model factory
- [ ] Metric functions
- [ ] Cluster-size function
- [ ] Experiment runner
- [ ] Logging function
- [ ] Comparison function
- [ ] Artifact-saving function

## Logging

- [ ] Unique experiment ID
- [ ] Run timestamp
- [ ] Feature set and order
- [ ] Preprocessor and parameters
- [ ] Model and parameters
- [ ] Status
- [ ] Runtime
- [ ] Metrics
- [ ] Cluster sizes
- [ ] Error type and message

## Comparison

- [ ] Failed runs removed from ranking
- [ ] K-Means and GMM separated
- [ ] Inertia compared only in valid groups
- [ ] AIC/BIC compared only in valid groups
- [ ] Cluster balance reviewed
- [ ] Stability reviewed
- [ ] Business profiles reviewed
- [ ] Candidate shortlist created

## Reproducibility

- [ ] Dataset version recorded
- [ ] Feature order saved
- [ ] Configuration saved
- [ ] Random state saved
- [ ] Library versions saved
- [ ] Selected preprocessor saved
- [ ] Selected model saved
- [ ] Metrics and profiles saved
