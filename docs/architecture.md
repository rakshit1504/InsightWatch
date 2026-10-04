# InsightWatch Architecture

InsightWatch follows an end-to-end analytics pipeline that transforms raw retail transactions into business anomaly alerts.

```text
UCI Online Retail II
        ↓
Python / Pandas
        ↓
Data Cleaning & Transaction Classification
        ↓
Daily KPI Generation
        ↓
Weekday-Aware Baseline + Z-Score
        ↓
Revenue Anomaly Detection
        ↓
AI-Assisted Business Insights
        ↓
PostgreSQL / Neon
        ↓
Power BI Dashboard
        +
Automated Email Alerts
