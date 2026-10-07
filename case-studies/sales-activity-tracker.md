# Activity Reporting: Excel and Tableau

## Summary

This Excel project originated as a workplace initiative connecting daily activity records to monthly reporting. The public sample uses fictional data. Inputs include fictional interaction IDs, product selections, outcomes, units, follow-up flags, and notes. The dashboard compares completed units with monthly product goals and a separately configured daily target. Settings controls product labels, goals, target days, and point values.

The public case study is available at [jonathancapalbo.me/sales-activity-tracker.html](https://jonathancapalbo.me/sales-activity-tracker.html).

The Tableau and React portions are new, AI-assisted portfolio extensions using the fictional public records. They are separate from the workplace Excel initiative and Jonathan's prior Tableau coursework. The browser explorer is a separate React implementation; the Tableau image is a static native export and the TWBX provides native interaction.

Excel settings guide daily entry, and the monthly summary and dashboard consolidate those entries for reporting. The Tableau extension reuses the same 465 fictional daily records for outcome, target, and record analysis. These are two views of the same activity-reporting project.

## Tableau and browser review

- [Packaged Tableau workbook](../downloads/Activity_Outcomes_Daily_Target_Review.twbx), with its fictional CSV included
- [Native Tableau export](../assets/images/tableau-activity-review.png)
- [All 465 fictional source records](../downloads/Fictional_Activities.csv)
- [React browser explorer](https://jonathancapalbo.me/sales-activity-tracker.html#browser-explorer)

Both views show outcomes by product, daily completed units, activity volume, completed-interaction share, units per completed interaction, and source records. Monthly totals and all daily charts always use the full source. Product and outcome controls narrow outcomes and records. Day and chart selections narrow records further. Clearing chart selection returns to the product/outcome subset. The React reset button restores 465 records and target 11. In Tableau, Escape clears the chart selection; set Product and Outcome to All and the daily target to 11 to restore defaults.

The React view uses semantic count and record tables, keyboard controls, an explicit empty state, and record details with all 10 source fields. Ratios divide total numerators by total denominators; they do not average daily percentages. Dates are July reporting dates, with no timezone conversion. Follow-up flags record activity, not an unresolved backlog. The sample provides no evidence of causes, response times, revenue, or business improvement.

React and ReactDOM 18.3.1 are pinned and self-hosted with their MIT license. The app uses `createRoot` and `createElement`, with no package installation or build step. The Excel walkthrough remains its original plain JavaScript implementation. Existing page fragments and workbook bytes are preserved. A local HTTP server is required for the JSON fetch; static results and downloads remain readable without JavaScript.

## Public demonstration workbook

[Download the workbook](../downloads/Fictional_Sales_Activity_Tracker.xlsx). It was rebuilt from scratch using fabricated records. The case-study screenshots and analysis refer to this file. It contains 35 sheets:

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

On October 6, 2026, all 465 records and all 10 fields were reconciled with the fictional source. The revised packaged workbook opened in native Tableau; its exported preview and website download were checked against the final files. Native checks confirmed fixed month totals, target changes, an empty date/subset intersection, Escape recovery to 22 records, and the full source worksheet.

Browser checks covered targets 0, 10, 11, 12, 13 and 25; all outcome counts and daily selections; 465 unique records across 47 pages; keyboard and touch controls; empty-state recovery; loading and failure fallback; and no-JavaScript content. At widths 320, 390, 768 and 1440, the expanded daily and record tables had no horizontal overflow at normal and 200% root text size. Chart axes use HTML labels at 16 and 32 pixels respectively. The existing walkthrough, navigation, SQL-copy controls and downloads passed their regression checks.

The native workbook has a fixed canvas and scrollable records. Full native keyboard-only, screen-reader, mobile and 200% text operation were not certified. The PNG is a static preview; native controls require the TWBX. The React explorer is a separate implementation using the same data.

A September 11, 2026 source-record check independently reproduced 465 activities, 324 units, 402.5 points, and the daily and product totals from the original public workbook. This was a reconciliation of the source records and saved outputs, not a native Excel interaction test.

- Four product totals reconcile to the 324 completed-unit dashboard total.
- Product-level points reconcile to the 402.5 dashboard total.
- Fourteen Met days plus 17 Below days account for all 31 days.
- Ninety-five Follow-up outcomes reconcile to 95 Yes follow-up flags.
- Sample notes agree with their row's outcome and follow-up flag. Notes were corrected during the September 2026 portfolio review without changing numeric records or formulas.

## Design trade-off

Separate daily tabs keep each day's inputs, totals, and goal status together for review. The monthly summary connects those daily views to the dashboard. Changes to repeated layouts or formulas need consistent updates across the tabs, followed by reconciliation of monthly totals.

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
