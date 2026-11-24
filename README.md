# Jonathan Capalbo | Portfolio

I’m working on my master’s in business and information systems at NJIT. My background is in customer operations, and I’m looking for an early-career role in business analysis, reporting, operations, business systems, or project coordination.

[Visit my portfolio](https://jonathancapalbo.me/)

At Comcast/Xfinity, I used Power Automate to filter daily reports for our team of 10 and deliver them by email or Microsoft Teams. The case study includes a working example with fictional teams and reports.

[Read the report-distribution case study](https://jonathancapalbo.me/report-distribution.html)

I also corrected formulas in my Excel activity tracker after I found entries missing from the monthly total. The downloadable workbook demonstrates how I check totals using fictional sales data.

## Explore the projects

### Chicago Food Inspections

I built four Tableau dashboards for an NJIT team project with Camerun Hannah, Mostafa Moawad and Yovanny Moscoso Huaman. We used City of Chicago inspection records from 2019 through 2025. The dashboards let you compare outcomes by facility, risk, inspection type and ZIP code, and follow trends by month or year.

[Read the case study](https://jonathancapalbo.me/chicago-food-inspections.html) · [Download the four-dashboard Tableau workbook](downloads/Chicago_Food_Inspections.twbx) · [Validation totals](downloads/Chicago_Food_Inspections_Validation.json) · [Four dashboards on Tableau Public](https://public.tableau.com/app/profile/jonathan.capalbo/viz/Chicago_Food_Inspections_17926114522930/3Geography)

The downloadable workbook contains the source CSV and omits author and machine metadata. The case study shows previews from Tableau Desktop 2026.2 and charts based on the workbook’s data.

### Activity Reporting: Excel and Tableau

The sample workbook links a month of daily activity logs to a dashboard. With 324 units against a monthly product goal of 310, the sample exceeds its monthly goal even though 17 of the 31 days fall below the daily target of 11 units.

For the portfolio, I also used AI assistance to build Tableau and React views of the same 465 fictional records. In either view you can change the daily target and inspect the records behind a result.

[Read the case study](https://jonathancapalbo.me/sales-activity-tracker.html) · [Download the Excel workbook](https://jonathancapalbo.me/downloads/Fictional_Sales_Activity_Tracker.xlsx)

[Tableau workbook](downloads/Activity_Outcomes_Daily_Target_Review.twbx) · [Native Tableau export](assets/images/tableau-activity-review.png) · [Fictional source CSV](downloads/Fictional_Activities.csv) · [Browser explorer](https://jonathancapalbo.me/sales-activity-tracker.html#browser-explorer)

The browser view uses React and ReactDOM 18.3.1, served from `assets/vendor/react-18.3.1` with their MIT license. Serve the site over HTTP to load the JSON dataset. There’s no build step. Visitors can still read the totals, view the Tableau export and download the files if JavaScript or the dataset fails to load.

### NJIT Registrar ServiceNow Portal

In an NJIT ServiceNow lab, I configured a searchable portal, organized 42 help articles into 12 categories, and revised a registration guide. The case study includes a screenshot of the lab portal and a recreation of the guide.

[Read the case study](https://jonathancapalbo.me/servicenow-njit-registrar.html)

### Arcade Operations Ticketing Modernization

For a hypothetical arcade, I mapped how staff could report a problem, assign an owner and verify a fix. The case study includes 10 requirements and 14 proposed acceptance tests for that design.

[Read the case study](https://jonathancapalbo.me/arcade-ticketing-modernization.html) · [View the supporting work](https://jonathancapalbo.me/arcade-ticketing-evidence.html)

### Movie Rental Database

My Oracle SQL final for an undergraduate database class. It connects customers, movie copies, and rental history, with a query showing which copies have not been returned.

The public copy uses fictional customer details. It passed 43 checks, but two rental rules needed more work. In a separate AI-assisted revision, I added checks that reject a return dated before checkout and prevent two open rentals for the same copy. All 20 tests for the revision passed on Oracle AI Database 26ai Free (23.26.3.0.0). Those tests covered individual sessions. Concurrent access and performance are still untested.

[Read the SQL project](https://jonathancapalbo.me/sql-movie-rental.html) · [Download the SQL](https://jonathancapalbo.me/downloads/Movie_Rental_Database.sql)

[Download the separate Oracle revision](https://jonathancapalbo.me/downloads/Movie_Rental_Improvements.sql) · [Download revision tests](https://jonathancapalbo.me/downloads/Movie_Rental_Improvements_Validation.sql)

[Recorded revision results](https://jonathancapalbo.me/downloads/Movie_Rental_Improvements_Validation_Results.json) · [Recorded test output](https://jonathancapalbo.me/downloads/Movie_Rental_Improvements_Validation_Output.txt)

### Additional independent project

I adapted Mads Lorentzen’s AI Job Search to flag duplicate postings, check résumé versions, and track submissions. The case study uses a fictional application to show how I handle a timeout when the employer’s portal hasn’t confirmed receipt.

[Read the case study](https://jonathancapalbo.me/job-search-operations.html) · [Original upstream project](https://github.com/MadsLorentzen/ai-job-search)

## Résumés

- [Business analysis and business systems (default)](https://jonathancapalbo.me/downloads/Jonathan_Capalbo_Business_Analyst_Resume.pdf)
- [Reporting and operations](https://jonathancapalbo.me/downloads/Jonathan_Capalbo_Reporting_Operations_Resume.pdf)
