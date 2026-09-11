# Excel Activity Reporting System

## Summary

This Excel project connects daily activity records to monthly reporting. Inputs include fictional interaction IDs, product selections, outcomes, units, follow-up flags, and notes. The dashboard compares completed units with monthly product goals and a separately configured daily target. Settings controls product labels, goals, target days, and point values.

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

The fictional workbook uses separate monthly product goals and a daily target:

- 324 completed units against 310 combined product-goal units, or **104.5%** attainment;
- 402.5 points against a 400-point goal, or **100.6%** attainment;
- all four product totals finished above their configured goals; and
- only 14 of 31 days met the daily unit goal, while 17 finished below it.

The monthly product goals total 310 units. The separate daily target is 11 units, implying 341 units across 31 days. The same 324 completed units represent 95.0% of that 341-unit benchmark. These independently editable targets are not equivalent, so the contrast cannot by itself establish a performance problem.

Before recommending a process change, confirm the intended relationship between the targets, then compare activity volume and completed units on below-target days. The fictional data does not establish causes such as staffing, demand, or employee performance.

## Validation checks

A September 11, 2026 source-record check independently reproduced 465 activities, 324 units, 402.5 points, and the daily and product totals from the original public workbook. This was a reconciliation of the source records and saved outputs, not a native Excel interaction test.

- Four product totals reconcile to the 324 completed-unit dashboard total.
- Product-level points reconcile to the 402.5 dashboard total.
- Fourteen Met days plus 17 Below days account for all 31 days.
- Ninety-five Follow-up outcomes reconcile to 95 Yes follow-up flags.
- Sample notes agree with their row's outcome and follow-up flag. Notes were corrected during the September 2026 portfolio review without changing numeric records or formulas.

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
