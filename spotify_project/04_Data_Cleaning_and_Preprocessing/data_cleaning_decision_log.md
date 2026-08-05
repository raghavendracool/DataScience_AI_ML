# Data-Cleaning Decision Log Template

Use one row for every approved data change.

| Date | Dataset | Column | Issue Type | Issue Description | Rows Affected | Decision | Business Reason | Before | After | Approved By |
|---|---|---|---|---|---:|---|---|---|---|---|
| YYYY-MM-DD | spotify_user_behavior | skip_rate | Invalid range | Values above 1 | 0 | No action | Current data passes validation | N/A | N/A | Project team |

## Decision Rules

1. Never change data without identifying the issue.
2. Record the number of affected rows.
3. Explain the business reason.
4. Preserve raw values where possible.
5. Validate the result after cleaning.
6. Avoid removing valid extreme users.
