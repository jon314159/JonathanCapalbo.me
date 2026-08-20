# Excel Activity Reporting System

## Summary

This Excel project uses a separate tracking sheet for every day of a 31-day month. Daily totals feed a monthly summary and dashboard, while a Settings page controls fictional product labels, goals, target days, and point values. The public workbook contains 35 sheets, 32 Excel tables, 2,231 formula cells, and 2,480 cells covered by validation rules.

The public case study is available at [jonathancapalbo.me/sales-activity-tracker.html](https://jonathancapalbo.me/sales-activity-tracker.html).

## Public demonstration workbook

The downloadable workbook was rebuilt from scratch using fabricated records. It contains 35 sheets:

1. **Dashboard:** four KPI cards and two charts comparing fictional results with goals.
2. **Monthly Summary:** one row for each day, linked to the 31 daily sheets.
3. **Settings:** editable month, product labels, monthly product goals, daily goals, and point values.
4. **Day 01 through Day 31:** separate activity tables, daily totals, goal status, and product progress.
5. **Read Me:** instructions and a clear privacy statement.

## Workbook features

- A separate filterable activity table for each day of the month
- Fictional interaction IDs, products, outcomes, units, points, follow-up flags, and notes
- Drop-down validation for products, outcomes, and follow-up choices, plus whole-number validation from 0 through 10 for units
- Daily summary cards for activities, completed units, points, goal, and status
- Daily product totals and progress compared with a pro-rated daily target
- A monthly summary linked to all 31 daily sheets
- A line chart comparing daily completed units with the editable daily goal
- A bar chart comparing fictional product totals with editable monthly goals
- Conditional formatting for completed outcomes, follow-ups, and goal status
- Filters, date formats, instructions, and editable blue input cells

## How settings affect the workbook

`Settings → Daily sheets → Monthly Summary → Dashboard`

Changing a fictional product name updates connected labels and the available drop-down choices. Existing manually entered activity text remains as recorded. Product goals update product progress and the dashboard comparison; the daily goal updates status and the daily chart; target days update the Monthly Summary comparison; and point values recalculate point totals.

## Demonstration finding

The fictional month exceeded aggregate product goals while daily consistency remained uneven:

- 324 completed units against 310 combined product-goal units, or **104.5%** attainment;
- 402.5 points against a 400-point goal, or **100.6%** attainment;
- all four product totals finished above their configured goals; and
- only 14 of 31 days met the daily unit goal, while 17 finished below it.

This distinction is the main analytical value of the model: a strong monthly total does not necessarily mean the daily operating pattern was consistent.

## Validation checks

- Four product totals reconcile to the 324 completed-unit dashboard total.
- Product-level points reconcile to the 402.5 dashboard total.
- Fourteen Met days plus 17 Below days account for all 31 days.
- Ninety-five Follow-up outcomes reconcile to 95 Yes follow-up flags.

## Design trade-off

Separate daily tabs make each day easy to isolate and review, but repeated sheets increase maintenance. A more scalable next version would use one normalized activity table with date filtering, PivotTables or Power Query, sheet protection, and expanded exception reporting.

## Fictional public version

The public workbook contains no:

- real customer, account, or employee identifiers;
- employer-specific names, products, pricing, offers, or internal terminology;
- actual revenue, compensation, quotas, goals, or performance results; or
- confidential processes, scripts, systems, or operational instructions.

Every published product name, goal, activity record, identifier, date, note, result, and chart value is fictional.

## Tools used

- Cross-sheet Excel formulas
- Excel tables and filters
- Data validation
- Conditional formatting
- Excel charts
- Editable settings and assumptions
- Goal tracking
- Dashboard reporting
- Process documentation
