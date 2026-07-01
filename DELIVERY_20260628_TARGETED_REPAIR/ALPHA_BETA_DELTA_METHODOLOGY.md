# Alpha–Beta–Delta Methodology

## Preservation rule

This repair does **not** redefine or overwrite the existing Alpha, Beta, or Delta formulas. The protected production decision-table hashes are unchanged.

## Interpretation retained in the guide

- **Alpha**: directional tendency, magnitude, horizon behavior, and stability.
- **Beta**: sensitivity to price, volatility, regime, pressure, news, session, and model agreement.
- **Delta**: change in Alpha/Beta/pressure/confidence/uncertainty/error, including acceleration.

## Safe implementation boundary

Any enhanced Alpha–Beta–Delta component must remain an additive research record with:

- raw and normalized value;
- sample period and sample size;
- source columns and version;
- data-quality/missingness status;
- walk-forward-selected weights;
- no holdout-set weight selection;
- no future timestamp in a current feature.

## Status in this delivery

The existing research outputs are preserved and explainable through the new guide. No new production formula or weight was introduced. A complete audited component registry and walk-forward re-estimation of every requested sensitivity remains outside this targeted repair.
