# Module 06 — Feature Selection Checklist

## Project Objective

- [ ] Segmentation objective is documented
- [ ] Required business dimensions are defined
- [ ] Feature meaning is understood

## Raw Features

- [ ] Behavioral features listed
- [ ] Demographic features listed
- [ ] Identifiers listed
- [ ] Technical metadata columns listed

## Exclusions

- [ ] `user_id` removed from model inputs
- [ ] Irrelevant columns reviewed
- [ ] Future outcome fields excluded
- [ ] Previous cluster labels excluded

## Quality

- [ ] Missing values reviewed
- [ ] Data types reviewed
- [ ] Infinite values reviewed
- [ ] Constant features reviewed
- [ ] Near-constant features reviewed

## Redundancy

- [ ] Pearson/Spearman correlation reviewed
- [ ] Derived-vs-raw overlap reviewed
- [ ] Duplicate business meaning reviewed
- [ ] Over-weighted dimensions reviewed

## Engineering

- [ ] Every formula is documented
- [ ] Division by zero is handled
- [ ] Raw columns are preserved
- [ ] New ranges are validated
- [ ] Composite features use scaled inputs where required
- [ ] Leakage risk is assessed

## Experiment Preparation

- [ ] Core feature set created
- [ ] Expanded feature set created
- [ ] Engineered feature set created
- [ ] Profiling features separated
- [ ] Feature-set version recorded
