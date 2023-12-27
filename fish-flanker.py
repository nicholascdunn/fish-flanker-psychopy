'''
Fish Flanker Task (Eriksen Flanker Task)
Version 0.1
Updated: 12/23/2023
By: Nicholas C. Dunn
'''

import os
import sys
from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, monitors
from psychopy.hardware import keyboard
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np
import pandas as pd

# Constants
PSYCHOPY_VERSION = '2023.2.3'
EXP_NAME = 'Fish-Flanker'
FRAME_TOLERANCE = 0.0001
REFRESH_RATE = 1.0 / 60.0

# Initial Setup
this_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(this_dir)
exp_info = {'Participant ID': '', 'Timepoint': '', 'RA Name': ''}
dlg = gui.DlgFromDict(dictionary=exp_info, sortKeys=False, title=EXP_NAME)
if not dlg.OK:
    core.quit()
exp_info['date'] = data.getDateStr(format="%Y-%m-%d-%H%M")
exp_info['expName'] = EXP_NAME
exp_info['psychopyVersion'] = PSYCHOPY_VERSION
filename = this_dir + os.sep + f'data/{exp_info["participant"]}_{EXP_NAME}_{exp_info["date"]}_{exp_info["session"]}'

# Experiment Handler - handles saving data during the task.
thisExp = data.ExperimentHandler(
    name=EXP_NAME, version='',
    extraInfo=exp_info, runtimeInfo=None,
    originPath='F:\\Coding Projects\\fish-flanker-psychopy', 
    savePickle=True, saveWideText=True,
    dataFileName=filename
)
log_file = logging.LogFile(filename + '.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)

# Monitor and Window Setup
monitor = monitors.Monitor('monitor')
window = visual.Window(size=(1920, 1080), fullscr=True)
exp_info['frameRate'] = window.getActualFrameRate()
frame_dur = 1.0 / round(exp_info['frameRate']) if exp_info['frameRate'] else REFRESH_RATE

# Stimuli
left_arrow = 'images\L_Arrow.jpg'
right_arrow = 'images\R_Arrow.jpg'
left_fish = 'images\L_Fish.jpg'
right_fish = 'images\R_Fish.jpg'
instruction_fish = 'images\mouthTailFish.jpg'

text_stim = visual.TextStim(window)  # instructions
fixation_stim = visual.TextStim(window, '+')
fish1 = visual.ImageStim(window, pos=(-1, 0))  # left left fish
fish2 = visual.ImageStim(window, pos=(-.5, 0))  # left fish
fish3 = visual.ImageStim(window, pos=(0, 0))  # middle fish
fish4 = visual.ImageStim(window, pos=(.5, 0))  # right fish
fish5 = visual.ImageStim(window, pos=(1, 0))  # right right fish
background_box = visual.rect.Rect(window, pos=(0, .17), size=(2, .66), color='white')

# Initialize instructions list
instructions = []

# Initialize keyboard
kb = keyboard.Keyboard()

# Intialize Clocks and Timers
global_clock = core.Clock()
cd_timer = core.CountdownTimer()


# Functions

def initialize_trial_handler(block):
    return data.TrialHandler(
        nReps=1, method='sequential', trialList=data.importConditions(block)
        )


def add_trial_data(stim_onset, end_time):
    '''
    Handles adding some trial data to excel output file.
    
    Parameters:
    stim_onset (float): time in milliseconds at which stimulus was displayed.
    end_time (float): time in milliseconds at which the trial ended.
    '''
    thisExp.addData('block', block_count)
    thisExp.addData('trial', trial_count)
    thisExp.addData('stim_onset', stim_onset*1000)
    thisExp.addData('trial_duration', end_time)


def append_instructions(instructions):
    instr1 = "Welcome to the Flanker Task."
    instr2 = "This is a fish!\n\nA fish has a MOUTH and a TAIL\n[point to mouth and tail]\n\nThe fish is pointing the same way the MOUTH is pointing.\n[point right]"
    instr3 = "Here is a MIDDLE fish! Can you point to the MIDDLE Fish?"
    instr4 = "Where is the MIDDLE fish here?"
    instr5 = "Look at all the Fish!!!\n\nThe Fish in the MIDDLE is hungry."
    instr6 = "To feed the MIDDLE Fish,\npress the yellow button that matches the way the MIDDLE Fish is pointing."
    instr7 = "If the MIDDLE Fish is pointing this way, press this yellow button."
    instr8 = "Sometimes all the Fish will point the same way.\nSometimes the MIDDLE Fish will point a different way from his friends,\nlike this [point to the way middle fish is pointing]\n\nYou should always press the button that matches the way the MIDDLE Fish is pointing."
    instr9 = "Let me show you how to play!"
    instr10 = "Here the MIDDLE Fish is pointing this way, so I'll press this button."
    instr11 = "Here the MIDDLE Fish is pointing this way, so I'll press this button."
    instr12 = "Now it's your turn to try!\n\nTry to answer as fast as you can without making mistakes.\nIf you make a mistake, just keep going!"
    instr13 = "GOOD JOB! Now you get to play on your own without my help\n\nRemember, keep your eyes on the screen\nand try to answer as fast as you can without making mistakes.\nIf you make a mistake, just keep going!"
    instr14 = "Now you will do the same thing, but you will see arrows instead of fish.\n\nRemember, keep your eyes on the screen\nand try to answer as fast as you can without making mistakes."

    instructions.append(
        instr1, instr2, instr3, instr4, instr5, instr6, instr7, instr8, instr9, instr10, instr11, instr12, instr13, instr14
        )

def practice_block(instructions):
    continue_routine = True
    instruction_index = 0
    top_pos = (0, .5)
    bottom_pos = (0, -.33)
    if instruction_index == 0:
        text_stim.pos(top_pos)
    elif instruction_index == 1:
        text_stim.pos(bottom_pos)
        fish3.setImage(instruction_fish)
    elif instruction_index == 2:
        text_stim.pos(bottom_pos)
    elif 2 < instruction_index <= 6:
        text_stim.pos(bottom_pos)
        fish1.setImage(left_fish)
        fish2.setImage(left_fish)
        fish3.setImage(left_fish)
        fish4.setImage(left_fish)
        fish5.setImage(left_fish)
    elif instruction_index == 6:
        text_stim.pos(bottom_pos)
    if instruction_index != 14:
        while continue_routine:
            text_stim.setText(INSTRUCTIONS[instruction_index])
            text_stim.draw()
            if instruction_index == 1:
                fish3.draw()
            if 2 < instruction_index <= 6:
                fish1.draw()
                fish2.draw()
                fish3.draw()
                fish4.draw()
                fish5.draw()
            keys = kb.waitKey(['space'])
            if keys == True:
                instruction_index += 1
                break
        practice_block(INSTRUCTIONS)

def run_fixation():
    cd_timer.add(2)
    while cd_timer.getTime() > 0:
        fixation_stim.draw()
        window.flip()


def run_case1(trial, trial_clock):
    stim_onset = trial_clock.getTime() * 1000
    sub_resp = None
    kb.clock.reset()
    cd_timer.add(2)
    if trial['stimulus'] == 'fish':
        fish1.setImage(left_fish)
        fish2.setImage(left_fish)
        fish3.setImage(left_fish)
        fish4.setImage(left_fish)
        fish5.setImage(left_fish)
    elif trial['stimulus'] == 'arrow':
        fish1.setImage(left_arrow)
        fish2.setImage(left_arrow)
        fish3.setImage(left_arrow)
        fish4.setImage(left_arrow)
        fish5.setImage(left_arrow)
    while cd_timer.getTime() > 0:
        fish1.draw()
        fish2.draw()
        fish3.draw()
        fish4.draw()
        fish5.draw()
        window.flip()    
    keys = kb.getKeys(['left', 'right'])
    rt = ''
    for key in keys:
        rt = (key.rt) * 1000
        sub_resp = key.name
        correct = 1 if key_name == trial['corrAns'] else 0
        break
    end_time = trial_clock.getTime() * 1000
    add_trial_data(trial, stim_onset, end_time)
    thisExp.addData('condition', "congruent")
    thisExp.addData('rt', rt)
    thisExp.addData('response', sub_resp)
    thisExp.addData('correct', correct)


def run_case2(trial, trial_clock):
    stim_onset = trial_clock.getTime() * 1000
    sub_resp = None
    kb.clock.reset()
    cd_timer.add(2)
    if trial['stimulus'] == 'fish':
        fish1.setImage(right_fish)
        fish2.setImage(right_fish)
        fish3.setImage(right_fish)
        fish4.setImage(right_fish)
        fish5.setImage(right_fish)
    elif trial['stimulus'] == 'arrow':
        fish1.setImage(right_arrow)
        fish2.setImage(right_arrow)
        fish3.setImage(right_arrow)
        fish4.setImage(right_arrow)
        fish5.setImage(right_arrow)
    while cd_timer.getTime() > 0:
        fish1.draw()
        fish2.draw()
        fish3.draw()
        fish4.draw()
        fish5.draw()
        window.flip()    
    keys = kb.getKeys(['left', 'right'])
    rt = ''
    for key in keys:
        rt = (key.rt) * 1000
        sub_resp = key.name
        correct = 1 if key_name == trial['corrAns'] else 0
        break
    end_time = trial_clock.getTime() * 1000
    add_trial_data(trial, stim_onset, end_time)
    thisExp.addData('condition', "congruent")
    thisExp.addData('rt', rt)
    thisExp.addData('response', sub_resp)
    thisExp.addData('correct', correct)


def run_case3(trial, trial_clock):
    stim_onset = trial_clock.getTime() * 1000
    sub_resp = None
    kb.clock.reset()
    cd_timer.add(2)
    if trial['stimulus'] == 'fish':
        fish1.setImage(left_fish)
        fish2.setImage(left_fish)
        fish3.setImage(right_fish)
        fish4.setImage(left_fish)
        fish5.setImage(left_fish)
    elif trial['stimulus'] == 'arrow':
        fish1.setImage(left_arrow)
        fish2.setImage(left_arrow)
        fish3.setImage(right_arrow)
        fish4.setImage(left_arrow)
        fish5.setImage(left_arrow)
    while cd_timer.getTime() > 0:
        fish1.draw()
        fish2.draw()
        fish3.draw()
        fish4.draw()
        fish5.draw()
        window.flip()    
    keys = kb.getKeys(['left', 'right'])
    rt = ''
    for key in keys:
        rt = (key.rt) * 1000
        sub_resp = key.name
        correct = 1 if key_name == trial['corrAns'] else 0
        break
    end_time = trial_clock.getTime() * 1000
    add_trial_data(trial, stim_onset, end_time)
    thisExp.addData('condition', "incongruent")
    thisExp.addData('rt', rt)
    thisExp.addData('response', sub_resp)
    thisExp.addData('correct', correct)


def run_case4(trial, trial_clock):
    stim_onset = trial_clock.getTime() * 1000
    sub_resp = None
    kb.clock.reset()
    cd_timer.add(2)
    if trial['stimulus'] == 'fish':
        fish1.setImage(right_fish)
        fish2.setImage(right_fish)
        fish3.setImage(left_fish)
        fish4.setImage(right_fish)
        fish5.setImage(right_fish)
    elif trial['stimulus'] == 'arrow':
        fish1.setImage(right_arrow)
        fish2.setImage(right_arrow)
        fish3.setImage(left_arrow)
        fish4.setImage(right_arrow)
        fish5.setImage(right_arrow)
    while cd_timer.getTime() > 0:
        fish1.draw()
        fish2.draw()
        fish3.draw()
        fish4.draw()
        fish5.draw()
        window.flip()    
    keys = kb.getKeys(['left', 'right'])
    rt = ''
    for key in keys:
        rt = (key.rt) * 1000
        sub_resp = key.name
        correct = 1 if key.name == trial['corrAns'] else 0
        break
    end_time = trial_clock.getTime() * 1000
    add_trial_data(trial, stim_onset, end_time)
    thisExp.addData('condition', "incongruent")
    thisExp.addData('rt', rt)
    thisExp.addData('response', sub_resp)
    thisExp.addData('correct', correct)


block_files = ['conditions.xlsx']
block_count = 1

background_box.draw()

for instruction in instructions:


for block in block_files:
    trials = initialize_trial_handler(block)
    trial_count = 1
    trial_clock = core.Clock()
    global_clock.reset()
    for trial in trials:
        kb.clearEvents(eventType='keyboard')
        trial_clock.reset()
        run_fixation()
        if trial['condition'] == 1:
            run_case1(trial, trial_clock)
        elif trial['condition'] == 2:
            run_case2(trial, trial_clock)
        elif trial['condition'] == 3:
            run_case3(trial, trial_clock)
        elif trial['condition'] == 4:
            run_case4(trial, trial_clock)
        trial_count += 1
        thisExp.nextEntry()
    if 'escape' in kb.getKeys():
        window.close()
        core.quit()
    block_count += 1

window.flip()       
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()

thisExp.abort()
window.close()
core.quit()