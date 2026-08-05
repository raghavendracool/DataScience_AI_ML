# Spotify Data-Quality Checklist

## Dataset Structure

- [ ] Behavior shape is `(108000, 26)`
- [ ] Demo shape is `(108000, 6)`
- [ ] Required columns exist
- [ ] Column names are standardized

## Missing Values

- [ ] Missing counts checked
- [ ] Missing percentages checked
- [ ] Hidden missing tokens checked
- [ ] Imputation decisions documented

## Duplicates

- [ ] Exact duplicates checked
- [ ] Duplicate `user_id` checked
- [ ] Duplicate-key conflicts investigated

## Data Types

- [ ] Numeric columns are numeric
- [ ] Category columns are standardized
- [ ] `user_id` type matches across datasets

## Business Rules

- [ ] Rate columns fall between 0 and 1
- [ ] Days active falls between 0 and 30
- [ ] Age falls between 18 and 70
- [ ] City tier is 1, 2, or 3
- [ ] Device type contains approved categories

## Outliers

- [ ] IQR report generated
- [ ] Extreme values investigated
- [ ] No valid power users removed automatically

## Relationship

- [ ] `user_id` is non-null
- [ ] `user_id` is unique
- [ ] No unmatched users
- [ ] One-to-one merge validated

## Documentation

- [ ] Raw copies preserved
- [ ] Before/after counts recorded
- [ ] Cleaning decision log completed
- [ ] Final quality status recorded
