# Visible UI change checks

Apply to the changed surface on each target, including a project's first page. Use the project's existing tests and verification record. Choose only rows affected by the request.

| Change | Before implementation | Independent review and passing evidence |
| --- | --- | --- |
| Visible words or controls | List each addition or replacement with the original instruction or confirmed source, location, trigger and channel. Include text bound from status/reason fields, conditional branches, notifications, tooltips and recovery buttons. Preserve existing approved feedback at its trigger. | Inventory the actual rendered delta against the accepted baseline, including a reachable exceptional state. Exercise both the state that must stay silent and any approved feedback in its own state. A candidate spec, a test expectation or a server string cannot authorize a new display. Flag the specific unsupported addition even if all tests pass. |
| Selected design or screenshot | Open the selected frame/version or accepted export. For each affected state fix the target viewport, regions in order, content that belongs in them, and important geometry or image fitting. Map those observations to components before styling. If the source is inaccessible, use an accepted equivalent or keep that design decision open. | Compare the rendered target to the same frame, state and viewport. Check the shell, missing/extra regions and hit areas before polish. Use DOM geometry for measurable claims and a side-by-side or overlay for appearance. A mismatched region requires correction. Source-only checks or a screenshot of the implementation alone leave visual acceptance open. Reuse the existing [visual evidence procedure](frontend-visual-evidence.md). |
| Repeated interaction | Inspect the public component and the closest accepted consumers. Identify who owns markup, hit area and feedback, and who owns navigation or the business action. Use the public owner where its contract fits. If none exists, give the first repeated pattern one owner within scope. Record the concrete mismatch before choosing a separate implementation. | Trace both consumers through the public API to the actual hit target and feedback implementation. Test the whole target, accessible role, focus and activation on the applicable platform. A shared import or the same CSS class alone does not establish reuse. Preserve legitimate distinctions such as link versus command and independent sibling tools. |

When a row reveals a regression, put the smallest discriminating assertion in the normal project test entry. Run it against the prior faulty component or a labeled, isolated reconstruction and the corrected candidate with the same harness and inputs. Require the intended assertion to fail on the control and pass on the candidate. A setup error, skipped test or updated expected output does not qualify. For a single Node TAP test the bundled [replay tool](../scripts/replay-ui-regression.py) checks both outcomes. Run from the test workspace with its own root variable, test name and assertion message. Other runners can use their native equivalent. Existing verified checks can be reused on a matching basis.

Report each affected row with its source, observed result and evidence location. A confirmed unauthorized addition, design mismatch or unjustified second owner prevents a pass. Missing decisive evidence leaves the affected row unverified. A matching no-op needs no new component, text, test or specification. Pure internal changes with no affected UI contract use their existing checks.

For example, a Node project that uses `APP_SOURCE_ROOT` can replay one test as follows. Set the three path variables to the installed Skill and the two source snapshots. Both runs use the same test file.

```sh
python3 "$SKILL_DIR/scripts/replay-ui-regression.py" --root-env APP_SOURCE_ROOT \
  --control-root "$FAULTY_ROOT" --candidate-root "$FIXED_ROOT" \
  --name "card header activation" --assertion "heading must be one hit target" \
  -- node --test --test-reporter=tap --test-name-pattern="^card header activation$" header.test.mjs
```
