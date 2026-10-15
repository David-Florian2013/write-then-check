# Contributing

Change `skills/checker/scripts/check.py` or the demo, then run:

```bash
python3 scripts/demo.py
```

If the output changed, replace `docs/demo-transcript.txt` with that output and put the same text in the README fence. CI fails when those three differ.

Do not add a number, a study, or a claim the diff cannot show. A new secret shape needs a fixture in `scripts/demo.py` that fails without it and passes when the line is gone.
