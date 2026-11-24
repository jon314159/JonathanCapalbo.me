# Activity Reporting: Excel and Tableau

## Summary

At Comcast/Xfinity, I found that the monthly totals in my Excel activity tracker skipped some days. I corrected the formulas. For this portfolio, I built a separate workbook with fictional records so readers can check how daily entries add up over a month.

[Read the case study and follow a day through the workbook](https://jonathancapalbo.me/sales-activity-tracker.html).

I later built two AI-assisted versions for this portfolio, one in Tableau and one in React. Both use the same 465 fictional records as the Excel workbook. My Tableau coursework was a separate project.

July’s 324 completed units exceeded the combined monthly product goals of 310. Only 14 of 31 days met the daily target. The workbook lets you inspect both calculations.

## Tableau and browser review

- [Packaged Tableau workbook](../downloads/Activity_Outcomes_Daily_Target_Review.twbx), with its fictional CSV included
- [Native Tableau export](../assets/images/tableau-activity-review.png)
- [All 465 fictional source records](../downloads/Fictional_Activities.csv)
- [React browser explorer](https://jonathancapalbo.me/sales-activity-tracker.html#browser-explorer)

Open the packaged workbook in Tableau or use the browser version to compare outcomes by product and see the underlying records. The daily charts show completed units, activity volume, the percentage of interactions completed, and units per completed interaction. Monthly totals and daily charts always include the full month.

Product and outcome filters narrow the counts and records. Selecting a day or count narrows the record list further. In the browser, **Clear chart selection** keeps your product and outcome filters. **Reset all controls** restores the 465 records and the daily target of 11 units. In Tableau, press **Escape** to clear a chart selection. To restore the defaults, set Product and Outcome to All and the target to 11.

The browser view includes keyboard-accessible count and record tables. Open **Details** to read all 10 fields. The completion percentage uses all completed interactions divided by all interactions. Dates follow the workbook’s July reporting dates. A follow-up flag records an activity at the time of entry. The records have no later status to show whether the follow-up remains open.

The site serves React and ReactDOM 18.3.1 locally with their MIT license. The explorer uses `createRoot` and `createElement` and needs no build step. For local testing, use an HTTP server so the explorer can load its JSON data. The Excel walkthrough uses plain JavaScript. The results table and downloads also work with JavaScript turned off.

## Public demonstration workbook

The [downloadable Excel workbook](../downloads/Fictional_Sales_Activity_Tracker.xlsx) is the source for the screenshots and figures in the case study. Its 35 sheets include the following.

1. **Dashboard:** four KPI cards and two charts comparing fictional results with goals.
2. **Monthly Summary:** one row per day, with figures pulled from the daily worksheets.
3. **Settings:** editable month, product labels, monthly product goals, daily goals, and point values.
4. **Day 01 through Day 31:** separate activity tables, daily totals, goal status, and product progress.
5. **Read Me:** instructions and a clear privacy statement.

## Workbook features

- A separate filterable activity table for each day of the month
- Fictional interaction IDs, products, outcomes, units, points, follow-up flags, and notes
- Drop-down validation for products, outcomes, and follow-up choices, plus whole-number validation from 0 through 10 for units
- Daily summary cards for activities, completed units, points, goal, and status
- Daily product totals and progress compared with a pro-rated daily target
- A monthly summary that uses formulas to pull in totals from all 31 daily worksheets
- A line chart comparing daily completed units with the editable daily goal
- A bar chart comparing fictional product totals with editable monthly goals
- Conditional formatting for completed outcomes, follow-ups, and goal status
- Filters, date formats, instructions, and editable blue input cells

## How settings affect the workbook

The daily sheets read their goals and product names from Settings. Monthly Summary pulls in the daily totals, and the Dashboard reads the summary.

Renaming a product updates its labels and drop-down choices. Earlier entries keep the text originally entered. Changing a product goal updates the dashboard comparison, while changing the daily goal updates each day’s status and the line chart. Target days feed the Monthly Summary comparison. Point values determine the points totals.

## Demonstration finding

July’s dashboard compares each product with its monthly goal and each day with the daily target.

- 324 completed units against a combined monthly product goal of 310, or **104.5%**.
- 402.5 points against a 400-point goal, or **100.6%**.
- All four products finished above their goals.
- 14 days met the daily goal and 17 fell short.

At 11 units per day, the target for 31 days adds up to 341. The same 324 completed units reached 95.0% of that benchmark. You can change either target independently in Settings.

Before proposing a process change, I’d ask how the two goals were set and compare activity counts with completed units on the 17 below-target days. Explaining why those days fell short would also require information about staffing and demand.

## Validation checks

The October 6, 2026 checks compared all 10 fields in each of the 465 records with the fictional source. The test opened the packaged workbook in Tableau and checked the preview and download against the final files. Monthly totals held steady when the target changed. When a day selection narrowed the filtered results to zero, Escape restored all 22 matching records. The checks also covered the full source worksheet.

Browser checks covered targets 0, 10, 11, 12, 13 and 25; all outcome counts and daily selections; 465 unique records across 47 pages; keyboard and touch controls; empty-state recovery; loading and failure fallback; and no-JavaScript content. At widths 320, 390, 768 and 1440, the expanded daily and record tables had no horizontal overflow at normal and 200% root text size. Chart axes use HTML labels at 16 and 32 pixels respectively. The existing walkthrough, navigation, SQL-copy controls and downloads passed their regression checks.

The native workbook has a fixed canvas and scrollable records. Full native keyboard-only, screen-reader, mobile and 200% text operation were not certified. The PNG is a static preview; native controls require the TWBX. The React explorer is a separate implementation using the same data.

A September 11, 2026 check compared the entries with the workbook’s saved results. Adding them independently reproduced the daily and product totals, including 465 activities, 324 units, and 402.5 points.

- Four product totals reconcile to the 324 completed-unit dashboard total.
- Product-level points reconcile to the 402.5 dashboard total.
- Fourteen Met days plus 17 Below days account for all 31 days.
- Ninety-five Follow-up outcomes reconcile to 95 Yes follow-up flags.
- Sample notes agree with their row's outcome and follow-up flag. Notes were corrected during the September 2026 portfolio review without changing numeric records or formulas.

## Design trade-off

Separate tabs put one day’s entries beside its totals and goal status. That makes one day easy to check, but it adds maintenance. If I change a daily formula or layout, I have to update the affected tabs and recheck the monthly totals.

## Fictional public version

The public workbook contains no:

- real customer, account, or employee identifiers;
- employer-specific names, products, pricing, offers, or internal terminology;
- actual revenue, compensation, quotas, goals, or performance results; or
- confidential processes, scripts, systems, or operational instructions.

All published names, goals, records and chart values are fictional.

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
