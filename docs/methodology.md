# Methodology

## Labels
Each row is one trade signal from a rule-based strategy. The label is good (1) if the trade hit its target and bad
(0) otherwise. The goal is a filter, not a new strategy: keep the trades the model scores highly.

## Features
Technical indicators at the entry bar, time-of-day and recency flags, standardised per segment (currency,
condition, timeframe). K-means cluster labels are added as extra features at several cluster counts. A decision
tree ranks variables per segment and the top ones are kept.

## Split
Time-based: train on years up to 2018, test on 2019 and 2020. Results are shown overall and per year.

## Models
- Random Forest with grid search (cross-validated on the training years)
- SVM with grid search
- Keras feed-forward network (ReLU hidden layers, sigmoid output), fixed seeds

## Evaluation
For each percentile of the predicted probability (10th to 90th) I count TP / FP / TN / FN, the share of trades
that pass, the precision of the predicted good trades, and the profit kept by the filter compared with taking every
trade. I also compare the model probability with the break-even rate `1 / (1 + RR)` for several reward-to-risk
settings.

## Known limits
Scaling, clustering and feature ranking were fitted on all years, so the test years are not fully clean.
Probabilities are not calibrated. Costs are not modelled. See the README for what I would change.
