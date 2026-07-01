# Formula and Data Dictionary

- `actual_open_to_close_pips = (target_close - target_open) / 0.0001`
- `alpha_pips = (current_raw_forecast - current_completed_origin_close) / 0.0001`
- `beta_pips = (previous_immutable_raw_forecast - previous_completed_origin_close) / 0.0001`
- `alpha_beta_difference_pips = abs(alpha_pips - beta_pips)`
- `robust_z = abs(alpha-beta) / max(1.4826*MAD(historical alpha-beta differences), epsilon)`
- `active_cap_pips = min(50, ATR cap, available conditional 99th-percentile absolute move, available conditional 99th-percentile absolute forecast error)`
- `safe_path_point = origin_close + clipped(rescaled raw displacement, ±active_cap_pips)*0.0001`
- Hierarchical probability shrinkage: `(class_count + prior_strength*parent_probability)/(sample_count+prior_strength)`.
- Probability vector fields: `p_buy`, `p_sell`, `p_neutral`; they are normalized to sum to one.
- Operational fields never replace `production_action`, `raw_forecast`, canonical ids, or protected central-path data.
