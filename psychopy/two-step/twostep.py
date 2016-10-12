#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import core, visual, event, gui
import sys
import pandas as pd
import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt
from random import shuffle

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

ntrials = 201 # number of trials to complete

lbound = 0.25 # lower bound on reward probabilities
ubound = 0.75 # upper bound on reward probabilities
sdrewardpath = 0.025 # SD of the Gaussian process for reward probabilities

tlimitchoice = 3.0 # time limit for choices

fullscreen = True
if fullscreen is True:
    monitor_width  = 1024.
    monitor_height = 768.
else:
    monitor_width = 700
    monitor_height = 700

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

# Color palette (Colorbrewer qualitative set 1)
pal = [[ 0.78125  , -0.796875 , -0.78125  ],
       [-0.5703125, -0.015625 ,  0.4375   ],
       [-0.3984375,  0.3671875, -0.421875 ],
       [ 0.1875   , -0.390625 ,  0.2734375],
       [ 0.9921875, -0.0078125, -1.       ],
       [ 0.9921875,  0.9921875, -0.6015625]]

# Characters for stimuli
chars = [u'\u0EB0',
         u'\u0ED0',
         u'\u0E81',
         u'\u0EC1',
         u'\u0ED1',
         u'\u0E82']

'''
--------------------------------------------------------------------------------

    TEXT

--------------------------------------------------------------------------------
'''

# Introduction message
intromessage = visual.TextStim(win,
    text='Thank you for participating in our study.\n\n' +
         'You will be playing a game in which the goal is to maximize the amount of reward you receive.\n\n' +
         'We will start with a training step in order to familiarize yourself with the task.\n\n'
         'Press any key to continue...'
)



# Respond faster message
respondfaster = visual.TextStim(win,
    text='You must respond faster!'
)

'''
================================================================================

    FUNCTIONS

================================================================================
'''

# Function to initialize the stimulus colours
def initgraphics(pal=pal, chars=chars):
    shuffle(chars)
    shuffle(pal)
    stim = {
        0: {
            0: {
                0: visual.Rect(win, units='pix', width=0.25*monitor_height, height=0.25*monitor_height, lineColor=[-1,-1,-1], fillColor=pal[0]),
                1: visual.Rect(win, units='pix', width=0.25*monitor_height, height=0.25*monitor_height, lineColor=[-1,-1,-1], fillColor=pal[0])
            }
        },
        1: {
            0: {
                0: visual.Rect(win, units='pix', width=0.25*monitor_height, height=0.25*monitor_height, lineColor=[-1,-1,-1], fillColor=pal[1]),
                1: visual.Rect(win, units='pix', width=0.25*monitor_height, height=0.25*monitor_height, lineColor=[-1,-1,-1], fillColor=pal[1])
            },
            1: {
                0: visual.Rect(win, units='pix', width=0.25*monitor_height, height=0.25*monitor_height, lineColor=[-1,-1,-1], fillColor=pal[2]),
                1: visual.Rect(win, units='pix', width=0.25*monitor_height, height=0.25*monitor_height, lineColor=[-1,-1,-1], fillColor=pal[2])
            }
        }
    }

    stimtext = {
        0: {
            0: {
                0: visual.TextStim(win, text=chars[0], units='pix', height=0.2*monitor_height, color=[-1,-1,-1], font='DejaVu Sans'),
                1: visual.TextStim(win, text=chars[1], units='pix', height=0.2*monitor_height, color=[-1,-1,-1], font='DejaVu Sans')
            }
        },
        1: {
            0: {
                0: visual.TextStim(win, text=chars[2], units='pix', height=0.2*monitor_height, color=[-1,-1,-1], font='DejaVu Sans'),
                1: visual.TextStim(win, text=chars[3], units='pix', height=0.2*monitor_height, color=[-1,-1,-1], font='DejaVu Sans')
            },
            1: {
                0: visual.TextStim(win, text=chars[4], units='pix', height=0.2*monitor_height, color=[-1,-1,-1], font='DejaVu Sans'),
                1: visual.TextStim(win, text=chars[5], units='pix', height=0.2*monitor_height, color=[-1,-1,-1], font='DejaVu Sans')
            }
        }
    }

    rewardicons = {
        'icon': {
            0: visual.Circle(win, units='pix', radius=0.15*monitor_height, pos=[0, -0.15*monitor_height],
                             lineColor=[-0.164, -0.96, -1],
                             fillColor=[0.375, -0.7421875,-0.9296875]),
            1: visual.Circle(win, units='pix', radius=0.15*monitor_height, pos=[0, -0.15*monitor_height],
                             lineColor=[0.375, -0.359, -0.93],
                             fillColor=[0.9921875, 0.5703125, -1.])
        },
        'text': {
            0: visual.TextStim(win, text='X', units='pix', height=0.25*monitor_height, pos=[0,-0.15*monitor_height], color=[-0.164, -0.96, -1]),
            1: visual.TextStim(win, text='$', units='pix', height=0.25*monitor_height, pos=[0,-0.15*monitor_height], color=[0.375, -0.359, -0.93])
        }
    }

    return stim, stimtext, rewardicons

# Draw fixation cross
def drawfixation():
    vert = visual.Rect(win, units='pix', height=0.025*monitor_height, width=0.005*monitor_width, fillColor=[1,1,1], lineColor=[1,1,1])
    horz = visual.Rect(win, units='pix', height=0.005*monitor_height, width=0.025*monitor_width, fillColor=[1,1,1], lineColor=[1,1,1])
    vert.draw()
    horz.draw()

# Function to draw the stimuli
def drawrect(step, state, stim, stimtext, sel=None):
    pos = [[-0.25*monitor_width, -0.1*monitor_height   ],
           [0.25*monitor_width , -0.1*monitor_height   ],
           [0   , 0.25*monitor_height ]];

    if sel is not None:
        drawselected(0, 0, sel, stim, stimtext)

    stimorder = [0, 1]
    shuffle(stimorder)

    stim[step][state][stimorder[0]].pos = pos[0]
    stim[step][state][stimorder[1]].pos = pos[1]
    stim[step][state][stimorder[0]].opacity = 1
    stim[step][state][stimorder[1]].opacity = 1

    stim[step][state][stimorder[0]].draw()
    stim[step][state][stimorder[1]].draw()

    stimtext[step][state][stimorder[0]].pos = pos[0]
    stimtext[step][state][stimorder[1]].pos = pos[1]
    stimtext[step][state][stimorder[0]].opacity = 1
    stimtext[step][state][stimorder[1]].opacity = 1

    stimtext[step][state][stimorder[0]].draw()
    stimtext[step][state][stimorder[1]].draw()

    return stimorder

# Draw the selected stimulus with reduced opacity
def drawselected(step, state, sel, stim, stimtext):
    stim[step][state][sel].pos = [0, 0.25*monitor_height]
    stim[step][state][sel].opacity = 0.5
    stimtext[step][state][sel].pos = [0, 0.25*monitor_height]
    stimtext[step][state][sel].opacity = 0.5

    stim[step][state][sel].draw()
    stimtext[step][state][sel].draw()

# Transition function
def transition(sel):
    ptrans = [0.3, 0.7]

    return rnd.binomial(1, ptrans[sel])

# Translate key to choice
def key2choice(stimorder, keys):
    if keys[0] == 'f':
        choice = stimorder[0]
    elif keys[0] == 'j':
        choice = stimorder[1]
    return choice

# Update reward probabilities
def rewardpathupdate(paths, lbound=lbound, ubound=ubound, sd=sdrewardpath):
    return np.maximum(np.minimum(paths + sd*rnd.normal(0, 1, 4), ubound), lbound)

# Sample reward
def rewardfunction(state, choice, paths):
    rprob = paths[2*state + choice]
    return rnd.binomial(1, rprob)

# Draw reward or no-reward icon
def displayreward(reward, rewardicons):
    rewardicons['icon'][reward].draw()
    rewardicons['text'][reward].draw()

# Animate movement of chosen option to top of screen
def animatechoice(step, state, sel, stim, stimtext):
    endpos = np.array([0, 0.25*monitor_height])
    startpos = stim[step][state][sel].pos
    nframes = int(np.floor(1.0/win.monitorFramePeriod))
    ddist = (endpos - startpos)/nframes
    for frame in range(nframes):
        stim[step][state][sel].pos = stim[step][state][sel].pos + ddist
        stimtext[step][state][sel].pos = stim[step][state][sel].pos
        stim[step][state][sel].draw()
        stimtext[step][state][sel].draw()
        win.flip()

'''
================================================================================

    INITIALIZE DATA STRUCTURES, PRELOAD STIMULI

================================================================================
'''

stim, stimtext, rewardicons = initgraphics()             # Initialize the stimuli

paths      = np.zeros([ntrials+1, 4])          # Initialize path array
paths[0,:] = rnd.uniform(lbound, ubound, 4)    # Set initial reward probabilities

choices  = np.zeros([ntrials, 2])
states   = np.zeros(ntrials)                   # Only one column because step 1 state is always 0
rewards  = np.zeros(ntrials)
rt       = np.zeros([ntrials, 2])              # Store reaction times
keyarray = np.empty([ntrials, 2], dtype='<U1') # Log the keys pressed for choices

'''
================================================================================

    Experiment

================================================================================
'''


'''
--------------------------------------------------------------------------------

    WELCOME MESSAGE

--------------------------------------------------------------------------------
'''

intromessage.draw()
win.flip()
event.waitKeys()

'''
--------------------------------------------------------------------------------

    TRIALS

--------------------------------------------------------------------------------
'''

t = 0
while t <= ntrials-1:
    for trial in range(t, ntrials):
        '''
            INTER-STIMULUS INTERVAL
        '''
        drawfixation()
        win.flip()
        core.wait(rnd.exponential(1.5))

        '''
            STEP 1
        '''
        # Present stimuli
        stimorder = drawrect(0, 0, stim=stim, stimtext=stimtext)
        win.flip()

        # Collect response within step time limit
        starttime = core.getTime()
        keys = event.waitKeys(maxWait=tlimitchoice, keyList=['f','j'], timeStamped=True)
        if keys is None:
            respondfaster.draw()
            win.flip()
            core.wait(2.0)
            break
        else:
            step1key    = keys[0][0]
            step1choice = key2choice(stimorder, keys[0][0])
            step1rt     = keys[0][1] - starttime

        '''
            TRANSITION
        '''

        # Conduct the transition
        step2state = transition(step1choice)

        # During the transition period, draw the selected Step1 choice above
        animatechoice(0, 0, step1choice, stim, stimtext)
        drawselected(0, 0, step1choice, stim, stimtext)
        win.flip()
        core.wait(1.5)

        '''
            STEP 2
        '''
        # Draw the Step2 Stimuli
        stimorder = drawrect(1, step2state, stim=stim, stimtext=stimtext, sel=step1choice)
        win.flip()

        # Collect the response
        starttime = core.getTime()
        keys=event.waitKeys(maxWait=tlimitchoice, keyList=['f','j'], timeStamped=True)
        if keys is None:
            respondfaster.draw()
            win.flip()
            core.wait(2.0)
            break
        else:
            step2key = keys[0][0]
            step2choice = key2choice(stimorder, keys[0][0])
            step2rt = keys[0][1] - starttime

        '''
            OUTCOME
        '''
        # Compute the reward from reward fuction based on choices
        reward = rewardfunction(step2state, step2choice, paths[t,:])

        # Draw the selected step 2 choice
        animatechoice(1, step2state, step2choice, stim, stimtext)
        drawselected(1, step2state, step2choice, stim, stimtext)
        win.flip()
        core.wait(1.5)

        # Display the reward outcome
        drawselected(1, step2state, step2choice, stim, stimtext)
        displayreward(reward, rewardicons)

        win.flip()
        core.wait(1.0)

        '''
            PARAMETER MANAGEMENT AND DATA STORAGE
        '''

        # Reset keys
        keys = None

        # Update the paths
        paths[t+1,:] = rewardpathupdate(paths[t,:]) # Update reward path

        # Add to data arrays
        states[t]     = step2state
        choices[t,:]  = np.array([step1choice, step2choice])
        rewards[t]    = reward
        rt[t,:]       = np.array([step1rt, step2rt])
        keyarray[t,0] = step1key
        keyarray[t,1] = step2key

        # Increment trial number
        t += 1

'''
================================================================================

    CONVERT AND STORE DATA

================================================================================
'''

# Create data frame
data = pd.DataFrame({
    'subject_id': subject_id,
    'step2state': states,
    'choice1'   : choices[:, 0],
    'choice2'   : choices[:, 1],
    'reward'    : rewards,
    'rt_step1'  : rt[:,0],
    'rt_step2'  : rt[:,1],
    'key_step1' : keyarray[:,0],
    'key_step2' : keyarray[:,1]
})

# Write to csv
data.to_csv('testdata.csv', sep='\t', encoding='utf-8')

'''
================================================================================

    PLOTS

================================================================================
'''

'''
plt.figure()
plt.subplot(1,3,1)
x = np.linspace(0, ntrials, ntrials+1)
for s in range(0, 4):
    plt.plot(x, paths[:, s])
plt.title('Reward Probabilities')
plt.ylabel('Probability of Reward')
plt.xlabel('Trial')
plt.ylim([0, 1])

plt.subplot(1, 3, 2)
x = np.linspace(0, ntrials, ntrials)
plt.plot(x, np.cumsum(rewards))
plt.title('Cumulative Reward')
plt.xlabel('Trials')

plt.subplot(1, 3, 3)
plt.hist(rt, 5, normed=1, histtype='bar', label=['Step 1', 'Step 2'])
plt.title('Reaction Times')
plt.show()
'''

win.close()
core.quit()
