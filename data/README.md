# Data

The data is not included in this repo. The notebooks expect these inputs, which you place here and point the
path variables at:

1. **Segment model files** (one CSV per currency / condition / timeframe, with cluster setting in the file name,
   e.g. `*cluster_10*.csv`). Columns:
   - `Currency`, `Condition`, `TimeFrame`, `Strategy`, `date`, `Year`
   - `Good_Bad_Flag` - target, 1 = good trade, 0 = bad trade
   - `Profit` - profit of the trade in price units
   - `TP_Ratio` - reward-to-risk ratio of the trade
   - feature columns from `_volume` onwards (standardised indicators, time features, cluster labels)
2. **`All Strategy_Relative_importance.csv`** - output of the feature pipeline: `Variable`, `Currency`,
   `Condition`, `TimeFrame`, `Strategy`, `Relative_Importance_Score`, `Rank`.
3. **Iteration list** (Excel) - one row per model variant: `Technique`, `Method`, `Method_Type`,
   `Cluster_Requirement`, `Rel_Imp_Requirement`, `Strategy`, plus seeds.
4. **Classifier list** (Excel, per strategy and method) - which segments to model.

The features come from the
[feature engineering pipeline](https://github.com/Avinash186200/ml-feature-engineering-pipeline-2020).
