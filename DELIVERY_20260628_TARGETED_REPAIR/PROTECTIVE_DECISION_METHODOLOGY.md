# Protective-Decision Methodology

## Purpose

The protective result is an additive risk-control interpretation. It does not replace the production BUY/SELL/WAIT direction.

## Permitted final labels

- `ALLOWED`
- `WAIT FOR PULLBACK`
- `HOLD AND PROTECT`
- `NO TRADE`

## Same-row evidence

The implementation reads only evidence available on the same published historical row:

- production direction, otherwise technical consensus;
- coverage;
- conflict;
- uncertainty;
- reliability;
- model/prediction agreement when published.

It does not copy unrelated rows or invent missing values.

## Deterministic policy

1. Missing or low coverage → `NO TRADE`.
2. High conflict → `NO TRADE`.
3. High uncertainty → `NO TRADE`.
4. Neutral/pullback direction → `WAIT FOR PULLBACK`.
5. Adequate reliability/agreement and low conflict → `ALLOWED`.
6. Otherwise → `HOLD AND PROTECT`.

The reason is stored beside every label. `Protective Validation Status` confirms membership in the four-label vocabulary.

## Historical-source quality

For each Dinner field, row-varying historical publications are ranked ahead of constant current-snapshot columns. The selected source is retained, and the table records whether it is row-varying, constant, sparse, or unavailable.

## Research limitation

The deterministic policy is not presented as a fully trained meta-labeling classifier. Validation-set threshold fitting and final holdout evaluation must be completed before claiming academic meta-label performance.
