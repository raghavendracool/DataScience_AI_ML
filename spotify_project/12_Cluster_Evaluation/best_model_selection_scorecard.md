# Best Model Selection Scorecard

Use one row for every shortlisted candidate.

| Candidate | Algorithm | Preprocessing | K / Components | Separation | Compactness / Fit | Balance | Stability | Interpretability | Actionability | Operational Simplicity | Risks | Decision |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| Candidate A | K-Means | StandardScaler | K=4 |  |  |  |  |  |  |  |  |  |
| Candidate B | K-Means | RobustScaler | K=5 |  |  |  |  |  |  |  |  |  |
| Candidate C | GMM | PowerTransformer | C=4 full |  |  |  |  |  |  |  |  |  |

## Suggested Review Questions

### Separation

- Is Silhouette strong?
- Is Davies-Bouldin acceptably low?
- Is Calinski-Harabasz strong?

### Fit

- Does K-Means show a meaningful elbow?
- Are GMM AIC and BIC competitive within the same feature space?

### Balance

- Are clusters too small or too dominant?
- Are niche groups stable and meaningful?

### Stability

- Are results consistent across seeds?
- Are cluster profiles consistent across samples?

### Business

- Can each cluster be explained?
- Can each cluster receive a distinct action?
- Is the number of personas operationally manageable?

## Decision Rule

Do not select using the total score alone.

Document:

1. Technical evidence
2. Stability evidence
3. Business evidence
4. Known risks
5. Final selection reason
