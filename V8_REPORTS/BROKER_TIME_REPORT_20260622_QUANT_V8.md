# Broker-Time Hardening Report

## Authoritative time contract

Internal persistence, joins, settlement and model calculations remain UTC. MetaTrader bars and ticks are treated as UTC. Broker and Myanmar clocks are display/export projections only.

Resolution precedence is:

1. validated Doo Bridge broker-server timestamp plus UTC receipt observation;
2. configured IANA broker timezone;
3. explicit manual broker-chart offset;
4. persisted previously validated offset;
5. `BROKER TIME UNAVAILABLE — CONFIGURE SETTINGS`.

Bridge observations reject stale receipt times, impossible offsets and aware timestamps that differ from receipt UTC by more than the allowed network window. IANA conversion uses `zoneinfo` and therefore follows daylight-saving changes. Myanmar display is UTC+06:30 / Asia-Yangon-equivalent, while UTC identity is retained.

The Settings page no longer seeds a fixed +4 offset. It exposes an IANA timezone input and an optional manual fallback. The shared provider publishes its source, observation time, offset, timezone and contract version. Active Field 1, Morning, AI evidence and copy output consume this provider.

## Validation evidence

Tests passed for UTC storage, Myanmar +06:30 display, January/July DST conversion in `America/New_York`, validated bridge precedence, invalid-offset rejection, IANA-over-manual precedence and unavailable-clock handling.
