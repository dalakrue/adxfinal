# Dinner Integration

Dinner is a direct top-level route owned by the shared application shell.

Rendering order:

1. canonical identity strip;
2. Dinner Combined History — Last 25 Broker Days;
3. compact current metrics;
4. closed Field 4 detail;
5. closed Field 6 detail;
6. closed Field 7 detail;
7. closed Field 8 detail;
8. closed Field 9 detail;
9. closed CRCEF-SV diagnostics;
10. source-column audit and export.

The history builder recursively discovers genuine timestamped Field 4/6/7/8/9 publications. It retains disagreements and calculates conflict rather than deleting one field. It never fabricates 25 days; it shows all genuinely available completed rows in the latest 25 broker-day window.
