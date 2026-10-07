---
name: diagnosing-bugs
description: Diagnose reported website defects and performance regressions with a symptom-specific reproduction, proportionate investigation, and verified regression checks.
---

# Diagnose a website defect

Read [the repository guidance](../../../AGENTS.md) and the affected source before choosing a reproduction. Identify which surface is failing: the static page, Excel walkthrough, React companion, native Tableau workbook, downloadable artifact, or deployment.

## Reproduce the reported behavior

Choose the smallest real entry point that exposes the symptom. Prefer the existing local page with fictional data, a focused browser assertion, or an isolated artifact check. Record the expected result from the source or requirement and the observed failure.

For an obvious defect, a direct reproduction, small fix, and targeted check are sufficient. For an uncertain defect, establish a repeatable symptom before drawing conclusions. Inspect source and captured evidence to construct the reproduction; if access prevents reproduction, report what is known, what remains a hypothesis, and which evidence would resolve it.

Use [behavioral testing](references/behavioral-testing.md) when constructing a test or browser harness. Keep external boundaries isolated, preserve the actual code path, and redact secrets from diagnostics. Native interactions may need an observed manual check; an automated browser result cannot stand in for that check.

## Investigate and fix

Reduce inputs or steps while retaining the reported failure. Test plausible causes against predictions, changing one relevant factor at a time. Use temporary instrumentation only where it adds evidence, then remove it.

Wait for the event that establishes a browser state, such as navigation completion or the rendered result. Distinguish an assertion that ran too early from a product defect. Use repeated or stress checks only when timing is part of the reported problem.

Make the smallest supported change. Preserve original artifact bytes unless the user's task includes replacing the artifact. Use temporary copies for authoring or native save experiments.

## Verify and report

Rerun the original reproduction and checks for the affected behavior. Extend an existing regression check when the defect warrants one; proportionate direct verification can suffice for a reversible copy or link correction. Compare preserved artifacts and report any changed outputs.

State the cause supported by evidence, the changed behavior, the checks actually run, and remaining limits. A local fix, reviewed change, pushed commit, successful Pages build, and verified live page are separate results. Follow current release authorization and review requirements in the repository guidance.

Adapted source and license: [Matt Pocock skills](../../../docs/third-party/matt-pocock-skills.md).
