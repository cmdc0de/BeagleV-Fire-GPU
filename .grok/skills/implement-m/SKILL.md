---
name: implement-m
description: >
  Implement the last BeagleV-Fire GPU slice spec that was agreed to. Build
  only what docs/slices/m{n}s{x}-plan.md describes, then stop so the user can
  walk through m{n}s{x}-test-plan.md. When the user passes close, mark that
  slice's features done, commit, push, and tag the repo m{n}s{x}. Use when
  the user runs /implement-m, /implement-m close, or asks to implement the
  last agreed slice.
---

# Implement milestone slice

Implement one agreed slice. The user walks the test plan. Passing `close` is what commits, pushes, and tags.

`n` is the milestone number and `x` is the slice number. `S0.4` is `m0s4`. Do not pad with zeros.

## Which slice

With no slice argument, use the last agreed spec: the newest `docs/slices/*-plan.md` that has a matching `docs/slices/*-test-plan.md` and does not already have a git tag named `m{n}s{x}`.

A named slice (`/implement-m S0.4` or `/implement-m m0s4`) uses that pair of files.

If no plan exists, stop and tell the user to run `/spec`. Do not invent a slice.

## Implement

Read the plan, the test plan, and the working agreements in `docs/project_goals.md`. Build only what the plan includes.

- Leave the next slice's features alone.
- Follow the working agreements. HDL stays a `CAPE_OPTION`. New register offsets do not reuse offsets a done slice already tests.
- When a bitstream is built, add an `## Implementation notes` section to the plan file with the logic-element, RAM, and math-block counts, plus decisions the code does not make obvious.
- Do not mark features `done`.
- Do not commit, push, or tag.

When the code is ready, stop. Point the user at `docs/slices/m{n}s{x}-test-plan.md` and tell them to walk those steps. Wait for `close`.

## Close

Run this only when the user passes `close` (`/implement-m close`). That means they walked the test plan and it passed. Do not rerun the board or laptop walkthrough.

1. Use the slice from this conversation. If there is none, use the same rule as "Which slice".
2. In `docs/project_goals.md`, set each feature in that plan to `` `done`. `` Keep the milestone and slice on the line. Add one changelog line naming the slice and the feature ids.
3. In the test plan's pass-record table, record the date and that the user passed `close`. Do not invent command output or a design version they did not report.
4. Commit the slice's changes. The subject names the slice, for example `Finish S0.4 and mark its features done.`
5. Create an annotated tag named `m{n}s{x}`. The message names the slice and says the test plan passed. If that tag already exists, stop before pushing and say so.
6. Push the current branch and push the tag. Do not force-push. If the push fails, say so. Leave the local commit and tag in place.

`close` does not start the next slice.
