# Formulas and Assumptions

Gaussian CRPS uses the closed-form normal-distribution expression. Sample CRPS is mean absolute observation distance minus half the mean pairwise sample distance. Quantile CRPS integrates pinball loss. Interval score uses width plus alpha-scaled miss penalties. Quantiles are made monotone with cumulative maxima. Dynamic weights are exponential transforms of decayed historical losses, clipped to floors/ceilings and renormalized.

Regime probabilities are lightweight shadow approximations based on trailing trend and volatility. Duration inference uses empirical completed episodes when enough samples exist. These are research diagnostics, not claims of a fully estimated production Hamilton/Filardo/HSMM model.
