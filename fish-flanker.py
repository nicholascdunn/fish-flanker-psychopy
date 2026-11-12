'''
Fish Flanker Task (Eriksen flanker task for children)
Version 1.0
By: Nicholas C. Dunn

Five fish (then five arrows) appear in a row. The child presses the left or right
arrow key to match the way the MIDDLE one is pointing.

Run it from PsychoPy Coder, or from a terminal:
    python fish-flanker.py            the real task (full screen)
    python fish-flanker.py --pilot    a test run that presses the keys by itself

Press Escape at any time to stop. The trials done so far are already saved.
'''

import argparse
import csv
import os
import random
import re

from psychopy import core, data, event, gui, visual, __version__ as psychopy_version
from psychopy.hardware import keyboard

import flanker_design as design

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------
EXP_NAME = 'fish-flanker'
VERSION = '1.0'

FIXATION_S = 1.0      # fixation cross before each trial
RESPONSE_S = 2.0      # the stimuli stay up until a key press or this long
BLANK_S = 0.5         # blank screen after each trial
FEEDBACK_S = 1.5      # practice feedback

LEFT_KEY = 'left'     # the left yellow button
RIGHT_KEY = 'right'   # the right yellow button
NEXT_KEY = 'space'    # the RA moves through the instructions
QUIT_KEY = 'escape'

# Colors and font from ncdunn.com (src/styles/global.css)
BG = '#1c1b1d'
TEXT = '#e6e1e3'
MUTED = '#9a9498'
RED = '#ff4757'
FONT = 'Space Mono'

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGES = os.path.join(HERE, 'images')
FONT_FILES = [os.path.join(HERE, 'fonts', 'SpaceMono-Regular.ttf'),
              os.path.join(HERE, 'fonts', 'SpaceMono-Bold.ttf')]
CONDITIONS = os.path.join(HERE, 'conditions.xlsx')
DATA_DIR = os.path.join(HERE, 'data')

# Sizes in 'height' units: 1.0 is the height of the screen.
STIM_W, STIM_H = 0.14, 0.10   # one fish or arrow (the pixel maps are 7 x 5)
STIM_GAP = 0.18               # centre to centre
TEXT_H = 0.038

INSTRUCTIONS = [
    # (text, picture). picture is None, 'mouth_tail', 'one_fish', or a case number (1 to 4).
    ("Welcome to the Flanker Task.", None),
    ("This is a fish!\n\nA fish has a MOUTH and a TAIL\n[point to mouth and tail]\n\n"
     "The fish is pointing the same way the MOUTH is pointing.\n[point right]", 'mouth_tail'),
    ("Here is a MIDDLE fish! Can you point to the MIDDLE Fish?", 'one_fish'),
    ("Where is the MIDDLE fish here?", 1),
    ("Look at all the Fish!!!\n\nThe Fish in the MIDDLE is hungry.", 1),
    ("To feed the MIDDLE Fish,\npress the yellow button that matches the way the MIDDLE Fish "
     "is pointing.", 1),
    ("If the MIDDLE Fish is pointing this way, press this yellow button.", 1),
    ("Sometimes all the Fish will point the same way.\nSometimes the MIDDLE Fish will point a "
     "different way from his friends,\nlike this [point to the way middle fish is pointing]\n\n"
     "You should always press the button that matches the way the MIDDLE Fish is pointing.", 3),
    ("Let me show you how to play!", None),
    ("Here the MIDDLE Fish is pointing this way, so I'll press this button.", 2),
    ("Here the MIDDLE Fish is pointing this way, so I'll press this button.", 4),
    ("Now it's your turn to try!\n\nTry to answer as fast as you can without making mistakes.\n"
     "If you make a mistake, just keep going!", None),
]
BEFORE_FISH = ("GOOD JOB! Now you get to play on your own without my help\n\n"
               "Remember, keep your eyes on the screen\nand try to answer as fast as you can "
               "without making mistakes.\nIf you make a mistake, just keep going!")
BEFORE_ARROWS = ("Now you will do the same thing, but you will see arrows instead of fish.\n\n"
                 "Remember, keep your eyes on the screen\nand try to answer as fast as you can "
                 "without making mistakes.")
THE_END = "You're all done!\n\nThank you for playing."
FEEDBACK_RIGHT = "Good job!"
FEEDBACK_WRONG = "Oops! Look at the MIDDLE fish."
FEEDBACK_SLOW = "Try to answer a little faster!"

COLUMNS = ['participant', 'timepoint', 'ra', 'date', 'block', 'block_trial', 'trial', 'case',
           'condition', 'stimulus', 'corr_ans', 'response', 'rt_ms', 'correct',
           'frame_rate', 'task_version', 'psychopy_version']


class Quit(Exception):
    """Raised when Escape is pressed."""


class Task:
    def __init__(self, info, pilot=False, screenshot_dir=None):
        self.info = info
        self.pilot = pilot
        self.screenshot_dir = screenshot_dir
        self.shot_count = 0
        self.quitting = False

        self.win = visual.Window(
            size=(1280, 720) if pilot else (1920, 1080), fullscr=not pilot,
            color=BG, units='height', allowGUI=pilot)
        self.win.mouseVisible = False
        rate = self.win.getActualFrameRate()
        self.frame_rate = round(rate, 2) if rate else ''
        self.kb = keyboard.Keyboard()

        def text(height=TEXT_H, color=TEXT, bold=False, **kw):
            return visual.TextStim(self.win, font=FONT, fontFiles=FONT_FILES, height=height,
                                   color=color, bold=bold,
                                   wrapWidth=1.6, alignText='center', **kw)

        self.text = text()
        self.title = text(height=0.06, color=RED, bold=True)
        self.hint = text(height=0.024, color=MUTED, pos=(0, -0.46),
                         text=f'[{NEXT_KEY}] next')
        self.fixation = text(height=0.08, text='+')
        self.feedback = text(height=0.05)

        def image(name):
            return os.path.join(IMAGES, name)
        self.images = {
            ('fish', 'left'): image('fish_left.png'), ('fish', 'right'): image('fish_right.png'),
            ('arrow', 'left'): image('arrow_left.png'), ('arrow', 'right'): image('arrow_right.png'),
        }
        self.row = [visual.ImageStim(self.win, size=(STIM_W, STIM_H), interpolate=False,
                                     pos=((k - 2) * STIM_GAP, 0)) for k in range(5)]

        # The instruction picture of one big fish with its mouth and tail labelled.
        self.big_fish = visual.ImageStim(self.win, image=self.images[('fish', 'right')],
                                         size=(0.42, 0.30), pos=(0, 0.18), interpolate=False)
        self.tail_label = text(color=RED, bold=True, text='Tail', pos=(-0.42, 0.30))
        self.mouth_label = text(color=RED, bold=True, text='Mouth', pos=(0.42, 0.30))
        self.tail_line = visual.Line(self.win, start=(-0.40, 0.27), end=(-0.24, 0.20),
                                     lineColor=RED, lineWidth=3)
        self.mouth_line = visual.Line(self.win, start=(0.40, 0.27), end=(0.24, 0.20),
                                      lineColor=RED, lineWidth=3)

        event.globalKeys.add(key=QUIT_KEY, func=self.quit, name='quit')

        os.makedirs(DATA_DIR, exist_ok=True)
        self.data_path = os.path.join(DATA_DIR, data_file_name(info))
        self.data_file = open(self.data_path, 'w', newline='', encoding='utf-8')
        self.writer = csv.DictWriter(self.data_file, fieldnames=COLUMNS)
        self.writer.writeheader()
        self.data_file.flush()

    # -- helpers ------------------------------------------------------------
    def quit(self):
        # Called from inside PsychoPy's key handling, where an exception can be lost,
        # so only set a flag here; flip() raises Quit on the next frame.
        self.quitting = True

    def flip(self, shot=None):
        self.win.flip()
        if self.quitting or self.kb.getKeys([QUIT_KEY], waitRelease=False, clear=False):
            raise Quit()
        if shot and self.screenshot_dir:
            self.shot_count += 1
            self.win.getMovieFrame()
            self.win.saveMovieFrames(os.path.join(
                self.screenshot_dir, f'{self.shot_count:02d}-{shot}.png'))

    def wait(self, seconds, draw=lambda: None):
        clock = core.Clock()
        while clock.getTime() < seconds:
            draw()
            self.flip()

    def set_row(self, stimulus, case, y=0.0):
        for k, (stim, way) in enumerate(zip(self.row, design.directions(case))):
            stim.image = self.images[(stimulus, way)]
            stim.pos = ((k - 2) * STIM_GAP, y)

    def draw_row(self, only_middle=False):
        for k, stim in enumerate(self.row):
            if not only_middle or k == 2:
                stim.draw()

    # -- instructions -------------------------------------------------------
    def instruction(self, text, picture=None, title=False, name='screen'):
        """Show one instruction screen until the RA presses the space bar."""
        draws = []
        if picture is None:
            stim = self.title if title else self.text
            stim.text = text
            stim.anchorVert = 'center'
            stim.pos = (0, 0)
            draws.append(stim.draw)
        else:
            if picture == 'mouth_tail':
                draws += [self.big_fish.draw, self.tail_line.draw, self.mouth_line.draw,
                          self.tail_label.draw, self.mouth_label.draw]
                self.text.pos = (0, -0.02)
            else:
                case = 1 if picture == 'one_fish' else picture
                self.set_row('fish', case, y=0.16)
                only_middle = picture == 'one_fish'
                draws.append(lambda: self.draw_row(only_middle))
                self.text.pos = (0, 0.02)
            self.text.text = text
            self.text.anchorVert = 'top'
            draws.append(self.text.draw)
        draws.append(self.hint.draw)

        def draw():
            for d in draws:
                d()

        draw()
        self.flip(shot=name)
        self.kb.clearEvents()
        if self.pilot:
            self.wait(0.3, draw)
            return
        while not self.kb.getKeys([NEXT_KEY], waitRelease=False):
            draw()
            self.flip()

    # -- trials -------------------------------------------------------------
    def trial(self, row, block, block_trial, shot=None):
        case = int(row['case'])
        stimulus = str(row['stimulus']).strip().lower()

        self.wait(FIXATION_S, self.fixation.draw)

        self.set_row(stimulus, case)
        self.kb.clearEvents()
        self.win.callOnFlip(self.kb.clock.reset)
        self.draw_row()
        self.flip(shot=shot)
        onset = core.Clock()

        plan = pilot_response(case) if self.pilot else None
        response, rt = None, None
        while onset.getTime() < RESPONSE_S:
            if self.pilot:
                if plan and onset.getTime() >= plan[1]:
                    response, rt = plan[0], onset.getTime()
                    break
            else:
                keys = self.kb.getKeys([LEFT_KEY, RIGHT_KEY], waitRelease=False)
                if keys:
                    response = 'left' if keys[0].name == LEFT_KEY else 'right'
                    rt = keys[0].rt
                    break
            self.draw_row()
            self.flip()

        self.flip()  # clear the screen
        correct = design.score(case, response)
        self.writer.writerow({
            'participant': self.info['Participant ID'], 'timepoint': self.info['Timepoint'],
            'ra': self.info['RA Name'], 'date': self.info['date'], 'block': block,
            'block_trial': block_trial, 'trial': row.get('trial', ''), 'case': case,
            'condition': design.congruency(case), 'stimulus': stimulus,
            'corr_ans': design.correct_answer(case), 'response': response or '',
            'rt_ms': '' if rt is None else round(rt * 1000, 1), 'correct': correct,
            'frame_rate': self.frame_rate, 'task_version': VERSION,
            'psychopy_version': psychopy_version,
        })
        self.data_file.flush()
        return response, correct

    def run_block(self, rows, block, feedback=False):
        for i, row in enumerate(rows, start=1):
            response, correct = self.trial(row, block, i,
                                           shot=f'{block}-trial' if i == 1 else None)
            if feedback:
                if response is None:
                    self.feedback.text, self.feedback.color = FEEDBACK_SLOW, TEXT
                elif correct:
                    self.feedback.text, self.feedback.color = FEEDBACK_RIGHT, RED
                else:
                    self.feedback.text, self.feedback.color = FEEDBACK_WRONG, TEXT
                self.feedback.draw()
                self.flip(shot=f'feedback-{i}' if i <= 2 else None)
                self.wait(FEEDBACK_S, self.feedback.draw)
            else:
                self.wait(BLANK_S)

    # -- the whole task ------------------------------------------------------
    def run(self, blocks):
        try:
            for n, (text, picture) in enumerate(INSTRUCTIONS, start=1):
                self.instruction(text, picture, title=(n == 1), name=f'instructions-{n:02d}')
            self.run_block(blocks['practice'], 'practice', feedback=True)
            self.instruction(BEFORE_FISH, name='before-fish')
            self.run_block(blocks['fish'], 'fish')
            self.instruction(BEFORE_ARROWS, name='before-arrows')
            self.run_block(blocks['arrow'], 'arrow')
            self.title.text = THE_END
            self.title.pos = (0, 0)
            self.title.draw()
            self.flip(shot='the-end')
            self.wait(3, self.title.draw)
        except Quit:
            print('Stopped with Escape. Trials so far are saved in', self.data_path)
        finally:
            self.data_file.close()
            self.win.close()


def pilot_response(case):
    """A made-up response for pilot runs: mostly correct, sometimes wrong or missing."""
    r = random.random()
    if r < 0.05:
        return None
    answer = design.correct_answer(case)
    if r < 0.15:
        answer = 'left' if answer == 'right' else 'right'
    return answer, random.uniform(0.35, 0.9)


def data_file_name(info):
    def clean(s):
        return re.sub(r'[^A-Za-z0-9_-]+', '-', str(s).strip()).strip('-')
    parts = [clean(info['Participant ID'])]
    if clean(info['Timepoint']):
        parts.append('T' + clean(info['Timepoint']))
    parts += [EXP_NAME, info['date']]
    return '_'.join(parts) + '.csv'


def ask_session_info():
    info = {'Participant ID': '', 'Timepoint': '', 'RA Name': ''}
    while True:
        dlg = gui.DlgFromDict(dictionary=info, sortKeys=False, title='Fish Flanker')
        if not dlg.OK:
            core.quit()
        if str(info['Participant ID']).strip():
            return info


def load_blocks():
    return design.split_blocks(data.importConditions(CONDITIONS))


def main():
    parser = argparse.ArgumentParser(description='Fish Flanker Task')
    parser.add_argument('--pilot', action='store_true',
                        help='windowed test run that presses the keys by itself')
    parser.add_argument('--screenshots', metavar='DIR',
                        help='with --pilot, save a picture of each screen to DIR')
    args = parser.parse_args()

    blocks = load_blocks()  # check the trial list before anyone sits down
    if args.pilot:
        info = {'Participant ID': 'PILOT', 'Timepoint': '', 'RA Name': ''}
    else:
        info = ask_session_info()
    info['date'] = data.getDateStr(format='%Y-%m-%d-%H%M')

    if args.screenshots:
        os.makedirs(args.screenshots, exist_ok=True)
    task = Task(info, pilot=args.pilot, screenshot_dir=args.screenshots)
    task.run(blocks)
    core.quit()


if __name__ == '__main__':
    main()
