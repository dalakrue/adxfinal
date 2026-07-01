# Mobile Test Report

Passed checks include:

- presentation-only mode switch;
- canonical result unchanged;
- exact bounded-view value parity;
- no more than 10 rows in the default mobile acceptance view;
- one IMAP-RV field at a time;
- no heavy calculation in page/column selection benchmark;
- full export frame retained;
- both entry files start;
- navigation survives AppTest reruns;
- missing optional/live data does not cause an uncaught exception.

Real-device browser refresh, touch interaction and battery tests remain incomplete.
