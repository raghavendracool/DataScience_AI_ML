# Final Project Explanation Script

## 30-Second Version

I built an end-to-end Spotify user-segmentation project using behavioral and demographic data. I cleaned and explored the data, engineered relevant features, compared multiple scaling methods, automated K-Means and GMM experiments, and evaluated them using clustering metrics, stability, balance and business interpretation. The illustrative final model was StandardScaler with K-Means K=4, producing Casual Snackers, Exploratory Samplers, Habitual Loyalists and Power Streamers. I then created persona-specific recommendation, retention and Premium strategies with measurable KPIs and guardrails.

## Two-Minute Version

The project objective was to segment Spotify users based on behavior and convert the technical groups into actionable personas.

I started by understanding the behavioral and demographic datasets, then validated missing values, duplicates, data types and ranges. I performed exploratory analysis using histograms, box plots, scatter plots and correlation heatmaps.

I selected behaviorally meaningful features, removed user identifiers from the model matrix, and engineered additional engagement, loyalty and friction features where useful. Since clustering is sensitive to scale, I compared StandardScaler, RobustScaler, MinMaxScaler, PowerTransformer and other transformations.

I automated K-Means and Gaussian Mixture Model experiments across multiple cluster counts and covariance types. I logged every configuration and compared the models using Silhouette Score, Davies-Bouldin, Calinski-Harabasz, inertia, AIC, BIC, cluster-size balance and stability.

The illustrative final selection was StandardScaler with K-Means K=4 because it provided the strongest overall combination of technical quality, stability, business interpretability and deployment simplicity. GMM was retained for soft-membership and boundary-user analysis.

I profiled the four groups and created Casual Snackers, Exploratory Samplers, Habitual Loyalists and Power Streamers. Finally, I translated the personas into recommendation, retention, discovery, loyalty and Premium-conversion hypotheses with primary and guardrail KPIs.

The next step would be to productionize the pipeline, monitor drift and validate the recommendations through controlled experiments.
