#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import core, visual, event, gui
import sys
import pandas as pd
import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt
from random import shuffle

from twostepcore import *

'''
================================================================================

    GET SUBJECT ID

================================================================================
'''

infodict = {
    'Subject ID': '',
    'Block'     : ''}
mygui = gui.DlgFromDict(dictionary=infodict, title='Two-Step Task')

subject_id = infodict['Subject ID'].encode('utf8')
block = infodict['Block'].encode('utf8')

if subject_id == '': # If no subject ID entered, quit.
    core.quit()

if block == '': # If no block number entered, quit.
    core.quit()
else:
    block = int(block)

'''
================================================================================

    EXPERIMENTAL PARAMETERS

================================================================================
'''

trials_per_block = 5      # using 75 trials per block
ptrans           = 0.7     # Probability of the correct transition
preward_low      = 0.25    # lower bound on reward probabilities
preward_high     = 0.75    # upper bound on reward probabilities
preward_sd       = 0.025   # SD of the Gaussian process reward prob
tlimitchoice     = 3       # Time limit for making a choice (sec)
t_transition     = 0.4     # Time during transition animations (sec)
ititime          = 1       # Mean of exponentially distributed ITI time (sec)

fullscreen = True
if fullscreen is True:
    monitor_width  = 1024.
    monitor_height = 768.
else:
    monitor_width  = 500
    monitor_height = 500

textypos = {
    'top': 0.35*monitor_height,
    'bottom': -0.35*monitor_height
}
boxpos = {
    'x' : {
        'neutral': 0,
        'left'  : -0.25*monitor_width,
        'right' : 0.25*monitor_width
    },
    'y' : {
        'neutral': 0,
        'high' : 0.4*monitor_height,
        'low' : -0.2*monitor_height
    }
}

'''
================================================================================

    INITIALIZE  COMPONENTS

================================================================================
'''

# Set up the window
win = visual.Window(
    [monitor_width, monitor_height],
    color=[-1, -1, -1],
    monitor="testMonitor",
    fullscr=fullscreen,
    units='pix'
)

# Stimuli
taskstim = loadstimuli(win=win,
                       stim_set='task',
                       stim_size=0.3*monitor_height)

rewardstim = loadstimuli(win=win,
                         stim_set='reward',
                         stim_size=0.3*monitor_height)

'''
================================================================================

    TUTORIAL
        Code for screens in this section is organized as the stimuli would be
        shown on screen. I.e. if text is above stimuli in the code, then the
        text should be above the stimuli on the screen

================================================================================
'''

# Screen 1
visual.TextStim(win,
    text = 'You are now ready to start the real task.\n\nIt is important to note that the boxes will now look different. However, everything you learned about how the task works (from the tutorial) will be the same.\n\nRemember, now you are playing for money, so do your best to remain focused throughout the game.\n\nPress "c" to start.'
).draw()
win.flip()
event.waitKeys(keyList=['c'])


"""
================================================================================

    TASK

================================================================================
"""

# Assign reward and transition probabilities to stimuli
trials = Trials(subject_id=subject_id,
                win=win,
                state_a_stim=taskstim[0],
                state_b_stim=taskstim[1],
                state_c_stim=taskstim[2],
                reward_stim=rewardstim,
                ntrials=trials_per_block,
                block=block,
                boxpos=boxpos,
                tutorial=False,
                ptrans=ptrans,
                preward_low=preward_low,
                preward_high=preward_high,
                preward_sd=preward_sd,
                tlimitchoice=tlimitchoice,
                t_transition=t_transition,
                ititime=ititime)

trials.run()
trials.savedata()
trials.plotrewardpaths()

# Screen 34
visual.TextStim(win,
    text='That is the end of the game.\n\n' +
    'You got ' + str(np.nansum(trials.data['r'])) + ' rewards!\n\n' +
    'Thank you for participating in our experiment.\n\n'
    'Press "c" to exit.',
    pos=[0, textypos['top']]
).draw()
win.flip()
event.waitKeys(keyList=['c'])



win.close()
core.quit()
