# Calibration Report

The layer calculates Brier score, logarithmic loss, expected calibration error, calibration bins, overconfidence penalty, underconfidence penalty and A–D reliability grade from settled probability/outcome pairs.

Minimum calibration sample: 60 settled observations. Below this threshold the status is `INSUFFICIENT_DATA`.

No live settled forecast database was available during delivery testing, so no production calibration number is claimed. Synthetic tests verified the calculation path and shadow-only behavior.
