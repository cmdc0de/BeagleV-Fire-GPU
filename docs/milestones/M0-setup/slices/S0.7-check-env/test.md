# S0.7 test

## Setup

S0.1, S0.2, and S0.4 have been followed. The script from `goals.md` is in the tree.

## Steps

On the laptop, from a new terminal:

```bash
python3 scripts/check-env.py --host
```

On the board:

```bash
python3 scripts/check-env.py --board
```

Also run `python3 scripts/check-env.py` with no arguments and confirm it exits non-zero.

## Expected results

- `--host` prints a `PASS` line for every item in `goals.md` and exits 0.
- `--board` prints a `PASS` line for every item in `goals.md` and exits 0.
- No arguments exits non-zero.
- A `FAIL` line names the missing tool. The run is not a pass while any `FAIL` remains.

## Pass record

| Date | Host result | Board result |
| --- | --- | --- |
| | | |
