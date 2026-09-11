# JonathanCapalbo.me

Personal portfolio for Jonathan Capalbo, a customer operations professional transitioning into entry-level business analysis, reporting, and business systems work. Professional experience, academic lab work, personal tool use, and hypothetical portfolio planning are labeled separately.

## Featured case studies

[Arcade Operations Ticketing Modernization](arcade-ticketing-modernization.html): a self-directed, hypothetical business analysis study. The [existing evidence pack](arcade-ticketing-evidence.html) contains a process comparison, proposed requirements, linked stories and acceptance criteria, planned UAT, and traceability. All tests are Not Executed. ServiceNow is a conceptual frame only.

[NJIT Registrar ServiceNow Portal](servicenow-njit-registrar.html): an academic school-lab project with a searchable portal, 42 articles organized into 12 categories, and a revised registration guide. Evidence includes a preserved lab screenshot and an explicitly recreated excerpt.

[Excel Activity Reporting System](sales-activity-tracker.html): a fictional Excel demonstration with controlled daily entry, editable goals, monthly consolidation, and separate product and daily goal comparisons. The [original workbook](downloads/Fictional_Sales_Activity_Tracker.xlsx) remains the public download.

## Resume variants and editable source

- [Primary business analysis / junior business systems resume](resume.pdf)
- [Reporting / operations resume](downloads/Jonathan_Capalbo_Reporting_Operations_Resume.pdf)

Both PDFs use the shared factual content in [`tools/resume_content.json`](tools/resume_content.json) and the ReportLab generator [`tools/build_resume.py`](tools/build_resume.py). Each has selectable text, embedded contact and project links, and 10.5-point body text. Variants change positioning, skills emphasis, project order, and relevant undergraduate coursework; employment history stays identical.

Run `python tools/build_resume.py` with ReportLab installed to rebuild both PDFs. Use `--variant business-analysis` or `--variant reporting-operations` to rebuild one. Review extracted text, hyperlinks, page count, and a rendered image after any content change. Serve this static site with `python -m http.server 8765` for local browser checks.

Undergraduate course attribution was confirmed by the author on September 11, 2026. Training remains separate from certifications. No phone number, new availability claim, or new proficiency level was added.

Technical and scope notes are documented in:

- [`case-studies/arcade-operations-ticketing-modernization.md`](case-studies/arcade-operations-ticketing-modernization.md)
- [`case-studies/servicenow-njit-registrar.md`](case-studies/servicenow-njit-registrar.md)
- [`case-studies/sales-activity-tracker.md`](case-studies/sales-activity-tracker.md)

## Privacy

The arcade case study is entirely hypothetical and simulated. It does not describe a real arcade, a live ServiceNow implementation, executed UAT, or measured business results.

The ServiceNow material is from a school lab, not NJIT's production registrar platform or live NJIT guidance. It contains no real student records. Public materials include the author's project description, a sanitized school-lab screenshot, and a recreated excerpt based on the author's project revision. Internal user details are omitted, and operational details are corrected or synthetic. The documented scope excludes registrar request forms and ServiceNow catalog items.

The public Excel workbook was rebuilt using entirely fictional records. It contains invented product labels, goals, activities, and results, but no employer-specific products, customer or account data, actual revenue, compensation information, or real performance results.
