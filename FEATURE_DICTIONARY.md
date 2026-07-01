# ARERT Feature Dictionary

| Feature | Definition | Timing rule | Typical use |
|---|---|---|---|
| `return_1h/3h/6h` | backward close-to-close percentage return | known at row time | regime, change, analogue |
| `range_pct` | absolute high-low range divided by close | completed candle only | volatility/jump |
| `vol_24h`, `vol_120h` | rolling standard deviation of past H1 returns | trailing windows | volatility state |
| `lower_z` | rolling 24-hour mean return divided by scale | trailing only | lower regime |
| `middle_z` | rolling 120-hour mean return divided by scale | trailing only | middle regime |
| `higher_z` | rolling 600-hour mean return divided by scale | trailing only | higher regime |
| `lower/middle/higher_regime` | BULL, BEAR, or COMPRESSION from each scale | research-only | hierarchy/duration |
| `session` | London, overlap, New York, or other by broker-hour mapping | row timestamp | conditioning |
| `volatility_state` | rolling high/low volatility classification | past median only | conditioning |
| `vote_mean` | signed mean of available internal decision votes | same timestamp | agreement |
| `vote_coverage` | fraction of available vote columns | same timestamp | data quality |
| `vote_agreement` | mean absolute vote strength | same timestamp | confidence proxy |
| `news_sentiment` | timestamp-aligned normalized sentiment | equal/past timestamp | behavior/event |
| `news_impact` | timestamp-aligned impact/priority | equal/past timestamp | jump/event |
| `future_return_H` | close at t+H divided by close at t minus one | label only after settlement | validation/outcome |
| `outcome_H` | sign class of settled future return | label only | supervised evaluation |
| regime age | hours since start of current research state | current/past states only | duration reliability |
| analogue distance | standardized multivariate distance to historical rows | current row excluded | historical support |
| conformal residual | absolute settled target minus historical point forecast | settled rows only | interval calibration |
| ARERT component | raw and normalized 0–100 evidence/penalty score | frozen module result | reliability decomposition |

Production columns retain their original names and values. Protective-action columns are display-only translations and never replace raw BUY/SELL/WAIT fields.
