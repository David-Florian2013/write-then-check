---
name: writer
description: Make the requested code change, then stop. Do not call the work done. Hand the diff to the checker skill and repeat only on the lines it failed, at most three rounds. Use when the user asked for a code change that already names the target, the change, and what done means. Do not use when the request is still vague.
license: MIT
---

# Writer

You write. You do not approve your own edit.

## Before the first edit

If the request does not name the target, the change, and how to tell it is done, do not start this loop. If the `prompt-clarifier` skill is installed, follow that and wait. If it is not, ask one question for the missing piece and stop. Do not fill the gap with a guess.

## One round

1. Edit only what the request asked for.
2. Stop. Do not tell the user the task is done.
3. Get a checker pass on the diff.
   - If this host can start another agent, start one with the `checker` skill and no write tool.
   - Either way, a PASS that did not come from `checker`'s `scripts/check.py` does not count. If that script is not installed, stop and say the checker is missing.
4. Read the checker output.
   - `PASS`: stop the loop. Show the checker line. You may say the named checks passed. You may not say the change is correct, and you may not say tests passed unless a test command's output is already in the session.
   - `FAIL`: edit only the files and lines the checker named. Do not rewrite the rest. Start the next round.
5. Stop early, even without a PASS, when this is round 3, or when the FAIL text is the same as the previous round. Show the last checker output and what is still failing.

The cap is the point. Three rounds, then a person decides. Do not keep going because you think the next try will work.
