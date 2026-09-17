# Behavior-First Vertical Slice

Use this shared rule only when requested behavior is stable enough to state and a durable public seam can observe it. Exploratory visuals, generated code, and behavior without an honest executable seam may use another focused validation path with the reason recorded.

## Seam Gate

Before writing a test or check:

1. name the repository's existing public seam and the external behavior it exposes;
2. confirm that the seam can observe the requested result without reaching into private state or duplicating implementation logic;
3. select one behavior and one independent expected result from the specification, a worked example, or a known-good fixture.

Do not invent an abstraction only to make a test possible. If no honest seam exists, report the gap; a brittle internal assertion is not a substitute.

## Focused Behavior Check

Reuse an existing check when it observes the requested behavior and independent
expected result. Add or extend a check only for an uncovered, meaningful regression
risk; do not create a test that restates a reversible low-impact implementation.

For a bug fix with a reproducible failure, run the focused check before the fix when
practical, then verify the corrected result. Implement related changes as one coherent
slice and run affected checks plus required project gates. Once they pass, expand or
repeat only for new changes, failures, unresolved concerns, or an explicit requirement.

Mock only true external boundaries; never mock the behavior owner being verified.
A passing test that was never observed red is validation evidence, not red-green
evidence. Preserve an explicitly required TDD workflow when the project adopts one.
