# Formulas and assumptions

- Gaussian CRPS uses `sigma[z(2Phi(z)-1)+2phi(z)-1/sqrt(pi)]`.
- Sample CRPS uses mean absolute observation error minus half the pairwise sample distance.
- Conformal widening uses the finite-sample `(n+1)(1-alpha)` order statistic over supplied prior matured scores only.
- Expected Markov duration is `1/(1-p_ii)`.
- DM variance uses a Newey-West/HAC correction through `horizon-1` lags.
- Counterfactual BUY/SELL values deduct spread/transaction cost; WAIT is zero.
- Attribution is predictive, not causal.
