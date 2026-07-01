# Validation and Leakage Control

## CPCV

`research_quant/validation/cpcv.py` creates deterministic chronological groups, chooses combinatorial test groups, purges overlapping information intervals, and applies an embargo after each contiguous test block.

## PBO

`research_quant/validation/pbo.py` compares the in-sample winning candidate with its out-of-sample percentile rank across aligned paths. A candidate is not promotable when competitive PBO cannot be estimated.

## Leakage rules

- Historical features are cut at the completed broker candle.
- Labels carry explicit start/end information intervals.
- Calibration is fitted on a period separate from base-model training and evaluated on untouched test data.
- Conformal residuals must be strictly out of sample.
- Smoothed Markov probabilities are historical-research only; live decisions use filtered information.
- Event matching excludes future responses.
- Opening a page, field, chart control, or expander cannot train or publish a model.

## Reproducibility

Canonical identity, input-feature hash, model version, output hash, data window, sample size, runtime, and warnings are stored in `research_audit`. Duplicate exact-run publications use `INSERT OR IGNORE` uniqueness constraints.
