# Module 10 — Glossary

| Term | Simple Meaning | Spotify Example |
|---|---|---|
| GMM | Gaussian Mixture Model | Soft user personas |
| Gaussian Component | One probability distribution | Power Streamer component |
| Mixture Weight | Component share | 28% modeled population |
| Mean Vector | Component center | Average behavior |
| Variance | Spread of one feature | Listening variation |
| Covariance | Two-feature co-movement | Listening and sessions |
| Covariance Matrix | Shape and orientation | Rotated ellipse |
| Probability Density | Relative model likelihood | User fit under component |
| Soft Clustering | Probability across groups | 70% Persona A |
| Hard Label | Highest-probability group | Component 2 |
| Responsibility | EM membership probability | γ(i, k) |
| E-Step | Estimate responsibilities | User probabilities |
| M-Step | Update model parameters | New means/covariances |
| EM | Expectation-Maximization | GMM training |
| Convergence | Objective improvement becomes small | Training stops |
| Log-Likelihood | Probability-based fit | `model.score()` |
| Full Covariance | Own complete matrix | Rotated component |
| Tied Covariance | Shared complete matrix | Same shape |
| Diagonal Covariance | No modeled feature covariance | Axis-aligned ellipse |
| Spherical Covariance | One variance per component | Circle |
| AIC | Fit-complexity score | Lower is better |
| BIC | Stronger complexity score | Lower is better |
| Confidence | Highest membership probability | 0.88 |
| Boundary User | Mixed membership | 0.51 vs 0.46 |
| `reg_covar` | Covariance stabilization | Add diagonal regularization |
