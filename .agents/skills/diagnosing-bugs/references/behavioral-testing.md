# Website behavioral testing

Use this reference when changing website behavior or diagnosing a defect. Choose checks for the affected user action and consequence. Documentation-only changes need instruction, link, license, scope, and configuration checks; they do not by themselves justify rerunning every UI suite.

## Test the observable result

Drive the real page, rendered controls, download response, or artifact boundary. Prefer accessible names and stable public identifiers. Compare against independently established expectations: source records, a worked example, preserved bytes, or an explicit requirement. Recomputing the expected value with the implementation's own helper cannot establish correctness.

For test-first work, add one failing behavior check, make the smallest change that passes it, then continue with the next needed behavior. The task and existing interfaces usually establish the test boundary; routine test selection does not need an extra approval round. Keep implementation and tests together as the behavior becomes clear.

Isolate external services, time, and other nondeterministic inputs where needed. Browser failure injection should verify the visible fallback or recovery, rather than merely asserting an internal call. Keep the application's own data and rendering path real.

## Preserve the three review surfaces

- Native Tableau: open the exact packaged workbook and exercise its controls when native behavior changes. Escape clears a selected mark; Product and Outcome return to All and target 11 manually. It has no reset-all button.
- Static export: verify the native image's source, legibility, dimensions, and defaults. Its pictured controls are not interactive.
- React companion: verify its separate browser state and recovery controls. Its Reset all controls action restores all records, target 11, and cleared day/mark selections.

Browser accessibility or responsive checks establish browser behavior only. Package structure, hashes, or a static export do not certify native interaction or accessibility.

## Worked example from the fictional July data

The [source CSV](../../../../downloads/Fictional_Activities.csv) has SHA-256 `13ad6bd3d5ec94bd71353bcf7fd1bb4e7b0cf132da5cf7102e700ff1c9229dd7`. These expectations describe that fixture; re-establish them independently if the source changes.

| Action or result | Expected behavior |
| --- | --- |
| Full-month totals | 465 records across 31 days; 282 completed interactions; 324 completed units; 402.5 points |
| Daily targets 0, 10, 11, 12, 13, 25 | 31, 19, 14, 12, 3, 0 Met days respectively |
| Core Package plus Follow-up | 22 matching records |
| Add July 1 to that subset | Zero matching records and an explicit empty state |
| Clear chart selection in React | Restore 22 records while retaining product/outcome filters |
| Reset all controls in React | Restore 465 records and target 11 |
| Product/outcome selections | Narrow records and outcome views; retain full-month totals and daily charts |

Monthly product goals and the daily target are different assumptions. The monthly goals total 310 units; target 11 across 31 days implies 341 units. A comparison must identify its denominator.

## Select relevant checks

For filters, verify narrowing, clearing, reset, stable month scope, and empty-result recovery. For record review, verify pagination and complete source detail. For navigation and layout, verify destinations, anchor visibility, keyboard operation, visible focus, narrow widths, text resizing, and reduced motion as affected. For data loading or dependencies, verify loading, failure, retry, malformed data, and the no-JavaScript fallback. For downloads, check status and expected artifact bytes, not status alone.

A Website Improvement workspace may contain the following optional evidence producers outside this repository. Locate them by filename and inspect the actual version, working-directory assumptions, inputs, and writes before execution. They are not dependencies of a standalone clone.

| Local file | Useful coverage |
| --- | --- |
| `verify-browser.cjs` | React counts, selections, reset, records, keyboard, touch, reflow, failures, fallback, download hashes |
| `verify-case-study.cjs` | Excel walkthrough, reduced motion, contents/anchors, clipboard recovery, downloads |
| `verify-download-layout.cjs` | Narrow download labels at doubled text size and fallback fonts |
| `verify-release.cjs` | Cross-page navigation, keyboard links, layouts, release downloads |
| `finalize_delivery.py`, `validate-release.py` | Preservation and source/release consistency; write manifests and evidence |
| `validate_package.py` | Tableau package structure and source consistency; writes reports and may offer a metadata-changing option |

These scripts can write JSON, screenshots, manifests, or diffs. Keep new run evidence separate from historical receipts and originals. Use a temporary output location or a scoped harness when appropriate.

For isolated browser runs, allow only the intended localhost server and fixture responses in every browser context, including touch and no-JavaScript contexts; apply equivalent isolation to standalone request clients. Existing scripts do not all supply that coverage. A live smoke check is a separate, scoped activity; avoid analytics beacons or other unintended external requests.

Native `REVIEWED_VALIDATION.md`, when present locally, supersedes the initial `NATIVE_VALIDATION.md` for revised-artifact checks. Its publication paragraphs remain historical; use current Git and release evidence to establish deployment.

Record the source version, check command or manual steps, observed result, and omissions. Rerun relevant checks after a change or failure; broaden testing when unresolved risk warrants it. Keep independent review separate from the implementer's own verification.
