# Fish Flanker Task

An Eriksen flanker task for children, written in PsychoPy. Five fish appear in a row, and the child presses the button that matches the way the MIDDLE fish is pointing. A second set of trials uses arrows in place of fish. The screens use the colors, font and pixel fish of [ncdunn.com](https://ncdunn.com).

Version 1.0. Tested with PsychoPy 2026.2.5 on Python 3.10, Windows 11.

## Running it

1. Install [PsychoPy](https://www.psychopy.org/download.html).
2. Download or clone this repository.
3. Open `fish-flanker.py` in PsychoPy Coder and press Run. You can also run `python fish-flanker.py` in a terminal where PsychoPy is installed.
4. Enter the participant ID (required), the timepoint and the RA's name.

The task runs full screen. Press **Escape** at any time to stop. Every trial is saved as soon as it ends, so a stopped session keeps the trials done so far.

To try the task without a child, run `python fish-flanker.py --pilot`. It opens a window and presses the keys by itself. Add `--screenshots shots` to save a picture of each screen to `shots/`.

## Keys

| Key | Who | What |
|---|---|---|
| Space | RA | Next instruction screen |
| Left arrow | Child | Middle fish points left (left yellow button) |
| Right arrow | Child | Middle fish points right (right yellow button) |
| Escape | RA | Stop the task |

Put yellow stickers on the arrow keys, or set `LEFT_KEY` and `RIGHT_KEY` at the top of `fish-flanker.py` to the keys your button box sends.

## What the child sees

1. Twelve instruction screens, which the RA reads aloud and moves through with the space bar. Words in [brackets] are prompts for the RA.
2. Four practice trials with fish. After each one the screen says "Good job!", "Oops! Look at the MIDDLE fish." or, when there was no press, "Try to answer a little faster!"
3. A reminder screen, then 25 fish trials with no feedback.
4. A screen that introduces the arrows, then 25 arrow trials with no feedback.
5. "You're all done!"

Each trial shows a fixation cross for 1 s. The five stimuli then stay up until the child presses a key, or for 2 s. A blank screen follows for 0.5 s (practice trials show feedback for 1.5 s instead). These times are set at the top of `fish-flanker.py`.

## Trial list

`conditions.xlsx` holds the trials in the order they run. Each row has:

| Column | Meaning |
|---|---|
| `trial` | Trial number in the file |
| `practice` | 1 for a practice trial, 0 otherwise |
| `stimulus` | `fish` or `arrow` |
| `case` | 1 to 4, see below |
| `corrAns` | The correct key, `left` or `right` |

| Case | Flankers | Middle | Condition | Correct key |
|---|---|---|---|---|
| 1 | left | left | congruent | left |
| 2 | right | right | congruent | right |
| 3 | left | right | incongruent | right |
| 4 | right | left | incongruent | left |

The task checks the file before it starts and stops with a message if `corrAns` does not match `case`.

## Data

Each session writes one CSV file to `data/`, named with the participant ID, timepoint and start time, for example `1001_T1_fish-flanker_2026-11-12-1430.csv`. There is one row per trial:

| Column | Meaning |
|---|---|
| `participant`, `timepoint`, `ra`, `date` | From the start dialog |
| `block` | `practice`, `fish` or `arrow` |
| `block_trial` | Trial number within the block |
| `trial` | Trial number from `conditions.xlsx` |
| `case`, `condition`, `stimulus`, `corr_ans` | What was shown and the right answer |
| `response` | `left`, `right`, or empty when there was no press |
| `rt_ms` | Response time in ms from when the stimuli appeared; empty when there was no press |
| `correct` | 1 for correct, 0 for wrong or no press |
| `frame_rate` | The monitor's measured refresh rate |
| `task_version`, `psychopy_version` | For the record |

The `data/` folder is in `.gitignore`, so participant files are never committed.

## Files

- `fish-flanker.py` runs the task.
- `flanker_design.py` holds the rules for what each case shows and how a response is scored. It has no PsychoPy code, so the tests in `tests/` can check it with `pytest`.
- `images/` holds the pixel fish and arrows. `tools/make_pixel_images.py` draws them from the same pixel maps as the demo on ncdunn.com.
- `fonts/` holds Space Mono (SIL Open Font License, see `fonts/OFL.txt`).

## License

MIT, see `LICENSE`. Space Mono is under the SIL Open Font License 1.1.
