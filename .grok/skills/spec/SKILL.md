---
name: spec
description: >
  Pick the features for the next BeagleV-Fire GPU slice. Read the open
  features in docs/project_goals.md, enter plan mode, and suggest the feature
  list for the next slice. After the user approves, write
  docs/slices/m{n}s{x}-plan.md and docs/slices/m{n}s{x}-test-plan.md, and
  record that milestone and slice on each placed feature in
  docs/project_goals.md. Use when the user runs /spec, asks to spec a slice,
  or asks which features belong in the next slice.
---

# Spec

Use this skill to choose the features for one slice and write that slice's plan and test plan. `docs/project_goals.md` is the feature index. This skill does not implement the slice.

## When the user names a scope

- `/spec` with no argument: the next slice in the project that does not yet have a plan.
- A milestone, such as `M3`: the next slice in that milestone that does not yet have a plan.
- A slice, such as `S0.4` or `m0s4`: that slice.

A slice already has a plan if either of these exists:

- `docs/slices/m{n}s{x}-plan.md`
- a `goals.md` whose slice id matches, under `docs/milestones/`

`n` is the milestone number and `x` is the slice number. `S0.4` is `m0s4`. `S7.3` is `m7s3`. Do not pad with zeros.

## Read before proposing

Read `docs/project_goals.md`. Then look at `docs/slices/` and `docs/milestones/` for plans that already exist.

An open feature has status `planned` and is not in the parking lot. Parking-lot features stay out unless the user asks to pull one in.

## Plan mode

Call `enter_plan_mode` before suggesting the feature list. In the plan, name the slice and propose the features that belong in it.

- Start from the slice's row in the milestone table. Map that row onto feature ids.
- Keep the list to what that one slice delivers. Leave the next slice's features out.
- For each proposed feature, give its id and one line on why it is in this slice.
- Name the features you considered and left out.

Call `exit_plan_mode` so the user can approve or change the list. Do not write slice files and do not edit `docs/project_goals.md` until the user approves that list. If they change the list, revise the plan and ask again.

## After approval

Write both files. Do not mark any feature `done`.

`docs/slices/m{n}s{x}-plan.md`:

- Milestone, slice id, and the slice name from `docs/project_goals.md`
- Features in this slice, each with the behavior this slice will implement
- Out of this slice
- Done when: the matching test plan passes

`docs/slices/m{n}s{x}-test-plan.md`:

- Setup: board, laptop, cables, image, bitstream, and kernel the reader needs
- Numbered steps a reader can follow without reading the HDL
- Expected results after each step that can fail: screen, command output, dmesg, or register values
- A pass-record table with date, what was programmed, and result

Update `docs/project_goals.md` in the same change:

- On each placed feature, record the milestone and the slice, for example `` `planned`. Milestone M0, slice S0.1. `` Leave the status `planned`.
- If the slice row does not mention those feature ids, add them.
- Add one changelog line naming the slice and the feature ids.

Do not add implementation notes. Those are written when the slice is built.
