# ML trading classifiers (2020)

[![tests](https://github.com/Avinash186200/ml-trading-classifiers-2020/actions/workflows/ci.yml/badge.svg)](https://github.com/Avinash186200/ml-trading-classifiers-2020/actions/workflows/ci.yml)

This is one of my early machine learning projects. I trained classifiers to predict whether a rule-based FX
trade signal would end up as a good trade or a bad trade, and then used the predicted probability as a filter:
only take the trade when the model is confident enough. I compared Random Forest, SVM and a small neural
network, and judged them on both classification metrics and the profit of the trades that pass the filter.

**When:** built in 2020 (first commits 14 Dec 2020, last notebook update Nov 2021).

**Modern version:** the maintained, cleaner version of this idea is
[trading-algorithm-backtester](https://github.com/Avinash186200/trading-algorithm-backtester).

## Problem

A trading strategy produces entry signals per currency pair, timeframe and condition. Many signals lose money.
The question was: given the market state at entry (technical indicators, time features, cluster labels), can a
model tell good entries from bad ones well enough to improve the profit of the strategy?

## Approach

- **Target:** `Good_Bad_Flag` per trade (good = the trade reached its target, bad = it did not).
- **Features:** technical indicators at entry time (built in my
  [feature pipeline repo](https://github.com/Avinash186200/ml-feature-engineering-pipeline-2020)), time of day and
  recency features, standardised per currency/condition/timeframe, plus K-means cluster labels (10 to 50 clusters).
- **Feature selection:** top variables by decision-tree relative importance, per segment.
- **Models:** Random Forest (grid search over trees, depth, max features, leaf size), SVM (grid search), and a
  small Keras feed-forward network. Each trained model is saved with pickle / h5.
- **Validation:** time-based split by year. Train on data up to 2018, test on 2019 and 2020 separately and overall.
- **Evaluation:** percentile tables of the predicted probability (TP, FP, TN, FN at each cut-off), share of trades
  that pass, accuracy of predicted 1s, model profit vs base profit, and model probability compared with the
  break-even rate `1 / (1 + reward-to-risk ratio)`.
- An iteration list (a small table of technique, method, cluster setting and feature setting) drives the main loop,
  so many model variants run in one go.

## Notebooks

| Notebook | What it does |
|---|---|
| [`model_building_backtest.ipynb`](notebooks/model_building_backtest.ipynb) | Main loop: loads segment data, splits by year, selects features, trains each model variant, builds the evaluation tables |
| [`random_forest_model.ipynb`](notebooks/random_forest_model.ipynb) | Grid search and Random Forest training, permutation importance, model save |
| [`svm_model.ipynb`](notebooks/svm_model.ipynb) | Grid search and SVM training |
| [`neural_network_model.ipynb`](notebooks/neural_network_model.ipynb) | Keras feed-forward network with fixed seeds |

The three model notebooks are imported by the main notebook with `import_ipynb`.

## How to run

```bash
python -m venv .venv
.venv/Scripts/activate        # on Linux / macOS: source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook notebooks/model_building_backtest.ipynb
```

The data is not included. See [data/README.md](data/README.md) for the expected inputs, and set the path
variables in the first cells of the main notebook. More detail is in [docs/methodology.md](docs/methodology.md).

## What I would do differently today

- **Leakage.** Standardisation, clustering and feature importance were fitted on the full history, including the
  test years. Today I would fit all of them on the training window only, inside a pipeline.
- **Proper time-series CV.** One split at 2018 is a single test. I would use walk-forward or purged, embargoed
  cross-validation so overlapping trades do not leak across folds.
- **Too many variants.** Many model variants on the same test years means the best one is partly luck. I would keep
  a final hold-out that is touched once, and correct for the number of trials.
- **Calibration.** I compared raw probabilities with the break-even rate. They should be calibrated first
  (Platt or isotonic) for that comparison to mean anything.
- **Costs.** Profit should include spread and slippage.
- **Code.** Notebooks importing notebooks was quick but fragile. Today this would be a small Python package with
  tests, a config file instead of hard-coded paths, and experiment tracking.
