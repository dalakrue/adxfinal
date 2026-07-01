# Hansen SPA / Data-Snooping Report

- Benchmark and all candidate loss columns are evaluated together.
- Moving-block bootstrap preserves H1 dependence.
- Candidate names, count, bootstrap draws, block length, p-value, OOS status and promotion status are persisted in `field10_research_experiments`.
- Without explicit OOS verification, promotion remains `RESEARCH_ONLY` even when the sample statistic appears favorable.

No real candidate registry was available at delivery time. Runtime experiment rows will show `INSUFFICIENT_DATA` or research-only evidence instead of inventing a result.
