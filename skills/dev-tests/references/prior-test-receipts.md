# Summarizing prior test receipts

Use this procedure for a summary-only request, including a statement that complete receipts exist. Identify the requested case and attempt on the matching code, test, data, browser and configuration basis. Read its case-level terminal record and cite the case ID, original outcome and evidence location in the summary.

| Evidence for the requested case | What the summary can say |
| --- | --- |
| Passed terminal and accessible assertions | Carry forward the pass for the recorded assertions and tested layer. |
| Failed terminal | Carry forward the failure and name the assertion, expected and actual when recorded. |
| Only observations, report index, a passing sibling or run-level exit | Preserve identifiable observations; the requested terminal result is unverified. |
| The original receipt or ID is unavailable | Attribute the existence of the receipt to its source. State that the original ID and/or terminal cannot be checked, and identify the record needed to recover it. |

A hash binds inputs. It does not encode an outcome. Separate an observed browser result with synthetic data from real-service behavior. Reconstruct the original result from the records already available; a summary-only request does not require rerunning the test.
