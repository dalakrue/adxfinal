# Path-Dependent Volatility Method

The path-memory prototype uses recursive exponentially weighted short/long returns and squared returns. It derives short/long trend memory, activity memory, path-dependent volatility, acceleration, agreement and H+1/H+3/H+6 expected range proxies.

Recursive updates avoid rebuilding the full path on every normal rerun. Parameters are research defaults; EURUSD-specific walk-forward optimization remains incomplete.
