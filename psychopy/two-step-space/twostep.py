#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import core, visual, event, gui
import sys
import pandas as pd
import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt
from random import shuffle

from twostepimg import get_images

'''
================================================================================

    GET SUBJECT ID

================================================================================
'''

infodict = {'Subject ID': ''}
mygui = gui.DlgFromDict(dictionary=infodict, title='Two-Step Task')

subject_id = infodict['Subject ID'].encode('utf8')

if subject_id == '': # If no subject ID entered, quit.
    core.quit()

'''
================================================================================

    EXPERIMENTAL PARAMETERS

================================================================================
'''

ntrain  = 1  # using 50 trials, as per Daw et al. 2011
ntrials = 1 # number of trials to complete

lbound = 0.25 # lower bound on reward probabilities
ubound = 0.75 # upper bound on reward probabilities
sdrewardpath = 0.025 # SD of the Gaussian process for reward probabilities

# Specify whether subjects will be paid per reward, and the amount that will be paid per reward gained
pay_per_reward = True
val_reward = 0.02 # amount to pay per reward on task

tlimitchoice = 3.0 # time limit for choices
isi = 1 # intertrial interval

fullscreen = True
if fullscreen is True:
    monitor_width  = 1024.
    monitor_height = 768.
else:
    monitor_width  = 500
    monitor_height = 500

'''
================================================================================================

    INITIALIZE SOME COMPONENTS

================================================================================================
'''

# Set up the window
win = visual.Window(
    [monitor_width, monitor_height],
    monitor="testMonitor",
    fullscr=fullscreen,
    units='pix'
)

stim = get_images(win=win)

'''
--------------------------------------------------------------------------------

    INTRODUCTION SCREEN

--------------------------------------------------------------------------------
'''

# Introduction message
visual.TextStim(win,
    text='Thank you for participating in our study.\n\n' +
         'You will play a game in which you fly spaceships to different planets to get space treasure.\n\n' +
         'We will start with a training step in order to familiarize yourself with the task. Please read all of the instructions carefully.\n\n' + 'It will take some time, but otherwise you will not know what to do\n\n' +
         'Press any key to continue...'
).draw()
win.flip()
core.wait(1.0)
event.waitKeys()

'''
--------------------------------------------------------------------------------

    INSTRUCTION START

--------------------------------------------------------------------------------
'''

# PLANETS
visual.TextStim(win,
    text='In this task, you will be taking a spaceship from earth to look for space treasure on two different planets',
    pos=(0, 0.3*monitor_height)
).draw()

stim['planets']['example'].size = stim['planets']['example'].size*0.75
stim['planets']['example'].draw()

visual.TextStim(win,
    text='Please press any key to continue...',
    pos=(0, -0.3*monitor_height)
).draw()
win.flip()
core.wait(1.0)
event.waitKeys()

# ALIENS
visual.TextStim(win,
    text='Each planet has two aliens on it and each alien has its own space treasure mine.',
    pos=(0, 0.3*monitor_height)
).draw()

stim['aliens']['example'].size = stim['aliens']['example'].size
stim['aliens']['example'].draw()

visual.TextStim(win,
    text='Once you arrive to each planet, you will ask one of the aliens for space treasure from its mine\n\n' +
    'Please press any key to continue...',
    pos=(0, -0.3*monitor_height)
).draw()
win.flip()
core.wait(1.0)
event.waitKeys()

# TREASURE/NOTREASURE
visual.TextStim(win,
    text='These aliens are nice, so if an alien just brought treasure up from the mine, it will share it with you. Space treasure looks like this:',
    pos=(0, 0.3*monitor_height)
).draw()

stim['reward'].pos = (0, 0.20*monitor_height)
stim['reward'].draw()

visual.TextStim(win,
    text='Sometimes, the alien will not bring up any treasure and you will see an empty circle:',
    pos=(0, 0.1*monitor_height)
).draw()

stim['noreward'].pos = (0, 0*monitor_height)
stim['noreward'].draw()

visual.TextStim(win,
    text='Please press any key to continue...',
    pos=(0, -0.3*monitor_height)
).draw()
win.flip()
core.wait(1.0)
event.waitKeys()

# REWARD FUNCTION EXPLANATION
visual.TextStim(win,
    text='If an alien has a good mine, then it can easily dig up space treasure and will be very likely to have some to share. Although it might not have treasure every time you ask, an alien with a good mine will have treasure most of the time.\n\n' +
    'Another alien might have a bad mine that is hard to dig through at the moment and will not have treasure to share most times you ask.\n\n' +
    'At the end of each trial, the space treasure that you earned will be converted to points.\n\n' +
    'Each piece of space treasure will be worth one point.\n\n' +
    'Please press the "V" key to continue.'
).draw()
win.flip()
core.wait(2.5)
event.waitKeys(keyList=['v'])

# EXPLAINING KEYS
visual.TextStim(win,
    text='On each planet, you can choose the LEFT alien by pressing the "F" key.\n\n' +
    'Alternatively, you can select the RIGHT alien by pressing the "J" key.\n\n' +
    'You will then see whether you got treasure.\n\n' +
    'Try practicing this a few times. In the following practice phase, always pick the alien that is highlighted.\n\n' +
    'Please press the "V" key to continue.'
).draw()
win.flip()
core.wait(2.5)
event.waitKeys(keyList=['v'])

'''
----------------------------------------------------------------------

    PRACTICE PHASE 1 (KEY PRESSING)

----------------------------------------------------------------------
'''

def drawpos(stim, pos=(0, 0)):
    """ Draws at a specific position without changing image default pos """
    stim.pos = pos
    stim.draw()

def drawaliens(stim1, stim2):
    """ Draws aliens side by side in a randomized fashion during key press training """
    if np.random.binomial(1, p=0.5) == 1:
        stim1.pos = (-0.15*monitor_width, 0)
        stim2.pos = (0.15*monitor_width, 0)
        correct_key = 'f'
    else:
        stim1.pos = (0.15*monitor_width, 0)
        stim2.pos = (-0.15*monitor_width, 0)
        correct_key = 'j'

    stim1.draw()
    stim2.draw()

    stims = [stim1, stim2]
    return stims, correct_key

for i in range(10):
    drawpos(stim['planets']['green']['planet'])
    stims, correct_key = drawaliens(stim1=stim['planets']['green']['stim1']['stim'], stim2=stim['planets']['green']['stim2']['deact'])

    win.flip()
    keys = event.waitKeys(keyList=[correct_key])

    drawpos(stim['planets']['green']['planet'])
    stims[0].draw()
    stims[1].draw()

    if correct_key == 'f':
        r_pos = (stims[0].pos[0], 0.15*monitor_height)
    else:
        r_pos = (stims[0].pos[0], 0.15*monitor_height)

    if np.random.uniform(0, 1) < 0.8:
        outcomestim = stim['reward']
    else:
        outcomestim = stim['noreward']

    drawpos(outcomestim, pos=r_pos)
    visual.Rect(win, units='pix', lineColor=[1,-1,-1], fillColor=None, size=stims[0].size*2, lineWidth=3, pos=stims[0].pos).draw()

    win.flip()
    core.wait(1.0)

# CONCLUSION OF FIRST KEYPRESS TRAINING (HIGHLY REWARDED)
visual.TextStim(win,
    text="You may have noticed that this alien's mine was good. It gave you space treasure most, if not all, of the time.\n\n" +
    "The mines of other aliens might be less good. To see this, you are going to ask another alien for treasure a few times.\n\n"
    'Please press the "V" key to continue.'
).draw()
win.flip()
core.wait(2.5)
event.waitKeys(keyList=['v'])

# KEYPRESS TRAINING WITH LOW REWARD
for i in range(10):
    drawpos(stim['planets']['yellow']['planet'])
    stims, correct_key = drawaliens(stim1=stim['planets']['yellow']['stim1']['stim'], stim2=stim['planets']['yellow']['stim2']['deact'])

    win.flip()
    keys = event.waitKeys(keyList=[correct_key])

    drawpos(stim['planets']['yellow']['planet'])
    stims[0].draw()
    stims[1].draw()

    if correct_key == 'f':
        r_pos = (stims[0].pos[0], 0.15*monitor_height)
    else:
        r_pos = (stims[0].pos[0], 0.15*monitor_height)

    if np.random.uniform(0, 1) < 0.2:
        outcomestim = stim['reward']
    else:
        outcomestim = stim['noreward']

    drawpos(outcomestim, pos=r_pos)
    visual.Rect(win, units='pix', lineColor=[1,-1,-1], fillColor=None, size=stims[0].size*2, lineWidth=3, pos=stims[0].pos).draw()

    win.flip()
    core.wait(1.0)
    win.flip()
    core.wait(0.5)

# CONCLUSION OF FIRST KEYPRESS TRAINING (LOW REWARD)
visual.TextStim(win,
    text="See, this alien was not in a very good part of the mine, and could share very little space treasure.\n\n" +
    "Every alien has treasure in its mine, but they can't share every time. Some will be more likely to share, but during times when it's easier for them to dig.\n\n" +
    "In the following practice phase, you can choose between two aliens and try to figure out which one has more treasure to share.\n\n" +
    "Each alien will sometimes come up on the right, and sometimes come up on the left.\n\n" +
    "Which side an alien appears on does not matter. For instance, left is not luckier than right.\n\n" +
    'Please press the "V" key to continue.'
).draw()
win.flip()
core.wait(2.5)
event.waitKeys(keyList=['v'])

'''
================================================================================

    CONCLUSION TEXT

================================================================================
'''

if pay_per_reward is True:
    payout = np.round(val_reward * np.sum(rewards), 2)

    # Done task message
    donetaskmsg = visual.TextStim(win,
        text='Great work! You\'ve successfully completed the task!\n\n' +
        'Total Earnings: $' + str(payout) + '\n\n' +
        'Thank you for participating in our research study.\n\n' +
        'Press the "V" key to exit.'
    )
else:
    donetaskmsg = visual.TextStim(win,
        text='Great work! You\'ve successfully completed the task!\n\n' +
        'Thank you for participating in our research study.\n\n' +
        'Press the "V" key to exit.'
    )

donetaskmsg.draw()
win.flip()
core.wait(5.0)
keys = event.waitKeys(keyList=['v'])

if keys[0] == 'v':
    win.close()
    core.quit()
