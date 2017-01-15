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

ntrain  = 50  # using 50 trials, as per Daw et al. 2011
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

# Color palette (Colorbrewer qualitative set 1)
pal = [[ 0.78125  , -0.796875 , -0.78125  ],
       [-0.5703125, -0.015625 ,  0.4375   ],
       [-0.3984375,  0.3671875, -0.421875 ],
       [ 0.1875   , -0.390625 ,  0.2734375],
       [ 0.9921875, -0.0078125, -1.       ],
       [ 0.9921875,  0.9921875, -0.6015625]]

# Color palette for training stimuli
trainpal = [[1. , -1., -1.],
            [-1.,  1., -1.],
            [-1., -1.,  1.]]

# Characters for stimuli
chars = [u'\u0EB0',
         u'\u0ED0',
         u'\u0E81',
         u'\u0EC1',
         u'\u0ED1',
         u'\u0E82']

# Characters for practice stimuli
trainchars = [u'\u03E0',
              u'\u0372',
              u'\u0394',
              u'\u03D8',
              u'\u03EA',
              u'\u0398']

isi = 1

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

# Done task message
donetaskmsg = visual.TextStim(win,
    text='Great work! You\'ve successfully completed the task!\n\n' +
         'Thank you for participating in our research study.\n\n' +
         'Press the "V" key to exit.'
)

'''
================================================================================

    FUNCTIONS

================================================================================
'''

# Function to initialize the stimuli
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

# Function to initialize the small stimuli for training
def drawstructurestims(stim, stimtext):

    stim[0][0][0].pos     = [-0.1*monitor_width, 0.4*monitor_height]
    stim[0][0][1].pos     = [ 0.1*monitor_width, 0.4*monitor_height]
    stim[0][0][0].opacity = 1
    stim[0][0][1].opacity = 1

    stim[1][0][0].pos     = [-0.7*monitor_width, -0.2*monitor_height]
    stim[1][0][1].pos     = [-0.5*monitor_width, -0.2*monitor_height]
    stim[1][0][0].opacity = 1
    stim[1][0][1].opacity = 1

    stim[1][1][0].pos     = [ 0.5*monitor_width, -0.2*monitor_height]
    stim[1][1][1].pos     = [ 0.7*monitor_width, -0.2*monitor_height]
    stim[1][1][0].opacity = 1
    stim[1][1][1].opacity = 1

    stimtext[0][0][0].pos     = [-0.1*monitor_width, 0.4*monitor_height]
    stimtext[0][0][1].pos     = [ 0.1*monitor_width, 0.4*monitor_height]
    stimtext[0][0][0].opacity = 1
    stimtext[0][0][1].opacity = 1

    stimtext[1][0][0].pos     = [-0.7*monitor_width, -0.2*monitor_height]
    stimtext[1][0][1].pos     = [-0.5*monitor_width, -0.2*monitor_height]
    stimtext[1][0][0].opacity = 1
    stimtext[1][0][1].opacity = 1

    stimtext[1][1][0].pos     = [ 0.5*monitor_width, -0.2*monitor_height]
    stimtext[1][1][1].pos     = [ 0.7*monitor_width, -0.2*monitor_height]
    stimtext[1][1][1].opacity = 1
    stimtext[1][1][1].opacity = 1

    stim[0][0][0].draw()
    stim[0][0][1].draw()
    stim[1][0][0].draw()
    stim[1][0][1].draw()
    stim[1][1][0].draw()
    stim[1][1][1].draw()
    stimtext[0][0][0].draw()
    stimtext[0][0][1].draw()
    stimtext[1][0][0].draw()
    stimtext[1][0][1].draw()
    stimtext[1][1][0].draw()
    stimtext[1][1][1].draw()

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
    rewardicons['icon'][reward].pos = [0, -0.15*monitor_height]
    rewardicons['text'][reward].pos = [0, -0.15*monitor_height]
    rewardicons['icon'][reward].draw()
    rewardicons['text'][reward].draw()

# Animate movement of chosen option to top of screen
def animatechoice(step, state, sel, stim, stimtext):
    endpos = np.array([0, 0.25*monitor_height])
    startpos = stim[step][state][sel].pos
    nframes = int(np.floor(0.4/win.monitorFramePeriod))
    ddist = (endpos - startpos)/nframes
    for frame in range(nframes):
        stim[step][state][sel].pos = stim[step][state][sel].pos + ddist
        stimtext[step][state][sel].pos = stim[step][state][sel].pos
        stim[step][state][sel].draw()
        stimtext[step][state][sel].draw()
        win.flip()

'''
================================================================================

    EXPERIMENT TRAINING

================================================================================
'''

'''
--------------------------------------------------------------------------------

    TRAINING STEP COMPONENTS

--------------------------------------------------------------------------------
'''
# Load training stimuli
stim, stimtext, rewardicons = initgraphics()

# TEXT ELEMENTS

ftext = visual.TextStim(win,
    text='"f"',
    units='pix',
    pos=[-0.25*monitor_width, -0.3*monitor_height]
)

jtext = visual.TextStim(win,
    text='"j"',
    units='pix',
    pos=[0.25*monitor_width, -0.3*monitor_height]
)

makeselection = visual.TextStim(win,
    text='Make your selection',
    units='pix',
    pos=[0, -0.3*monitor_height]
)

trainingstep1msg = visual.TextStim(win,
    text = 'At the first step, you will see two shapes with symbols inside of them.\n\n' +
    'You must select between one or the other using the "f" key (for the left one), or the "j" key (for the right one):\n\n' +
    'Press the "Q" key to try it out...'
)

trainingstep1resultmsg = visual.TextStim(win,
    text = 'As you can see, your choice will move to the top of the screen.\n\n' +
    'After the first step choice, you will be presented with another pair of choices that will look different. You will again need to choose between them using the "f" or "j" keys, as before.\n\n' +
    'Press the "Q" key to try it out...',
    pos = [0, -0.1*monitor_height]

)

trainingstep2resultmsg = visual.TextStim(win,
    text = 'Again, your choice will move to the top of the screen.\n\n' +
    'You will now either receive a reward (the coin), or not (the red "X") depending on your selection.\n\n' +
    'This sequence of steps will be repeated many times.\n\n' +
    'Before starting the actual task, we will give you 50 practice trials to become familiar with the task.\n\n'
    'Press the "Q" key to continue...',
    pos = [0, -0.1*monitor_height]
)

step1options = visual.TextStim(win,
    text = 'First Step Options',
    pos = [0, 0.6*monitor_height]
)

step2optionsA = visual.TextStim(win,
    text = 'Step 2 Options (Pair A)',
    pos = [-0.6*monitor_width, -0.0*monitor_height]
)

step2optionsB = visual.TextStim(win,
    text = 'Step 2 Options (Pair B)',
    pos = [0.6*monitor_width, -0.0*monitor_height]
)

structuredemomsg = visual.TextStim(win,
    text = 'The symbols that you are presented with at Step 1 are shown above. They never change throughout the task, but their order (left side vs. right side) can change.\n\n' +
    'After your choice at Step 1, you will be presented with either "Pair A" (here shown on the left), or "Pair B" (here shown on the right). Pair A and Pair B never get mixed up. You will always be presented with either one or the other at Step 2.\n\n' +
    'Selecting one of the symbols during Step 1 will lead you to Pair A more often, but the other symbol will lead you to Pair B more often.\n\n' +
    'Your choice at Step 1 is like choosing which dice to roll to determine the Pair you get at Step 2! These dice never change, so the odds of which Pair you get at Step 2 is always the same.\n\n' +
    'Press the "Q" key to continue',
    pos = [0, -0.1*monitor_height]
)

rewardstructuredemomsg = visual.TextStim(win,
    text = 'At Step 2, each option gives you a different chance of winning a reward (again, this is like rolling dice).\n\n' +
    'NOW BEWARE...the dice at this second step will gradually change over time! So the best options early in the game might not be the best later on.\n\n' +
    'Press the "Q" key to continue'
)

practicetrialsmsg = visual.TextStim(win,
    text = 'We\'ll now do some practice of the game. \n\n' +
           'You\'ll do 50 trials that won\'t count toward your overall rewards. They are just to help familiarize you with the game.\n\n' +
           'Note that there will be time limits at each step. If you respond too slowly, that trial will be aborted and you will see a message asking you to respond faster. Don\'t worry, though, you\'ll still receive a total of 50 practice trials.\n\n' +
           'Although there are time limits, during this practice you should focus more on learning how the game works.\n\n' +
           'Press the "Q" key to continue'
)

donepracticemsg = visual.TextStim(win,
    text = 'Great work!\n\n' +
           'Now that you have familiarized yourself with how the task works, you are ready to perform the real trials.\n\n' +
           'When you are ready to begin, press the "W" key'
)

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

    TRAINING INSTRUCTIONS

--------------------------------------------------------------------------------
'''
core.wait(1.0)

# FIRST STEP TRAINING
trainingstep1msg.draw() #insructions
win.flip()
core.wait(5.0)
event.waitKeys(keyList=['q'])

drawfixation() #fixation cross
win.flip()
core.wait(rnd.exponential(isi))

tstimorder = drawrect(0, 0, stim=stim, stimtext=stimtext) #stimuli
ftext.draw()
jtext.draw()
makeselection.draw()
win.flip()

tkeys = event.waitKeys(keyList=['f','j'], timeStamped=True) #record response for transition
tstep1key    = tkeys[0][0]
tstep1choice = key2choice(tstimorder, tkeys[0][0])

tstep2state = transition(tstep1choice) #conduct transition

# STEP 2 TRAINING
animatechoice(0, 0, tstep1choice, stim, stimtext) #animate the choice
drawselected(0, 0, tstep1choice, stim, stimtext)
trainingstep1resultmsg.draw()
win.flip()
core.wait(5.0)
event.waitKeys(keyList=['q'])

tstimorder = drawrect(1, tstep2state, stim=stim, stimtext=stimtext, sel=tstep1choice) # present step 2 stim
ftext.draw()
jtext.draw()
makeselection.draw()
win.flip()

tkeys=event.waitKeys(keyList=['f','j'], timeStamped=True)
tstep2key = tkeys[0][0]
tstep2choice = key2choice(tstimorder, tkeys[0][0])

animatechoice(1, tstep2state, tstep2choice, stim, stimtext) #animate the choice
drawselected(1, tstep2state, tstep2choice, stim, stimtext)
trainingstep2resultmsg.draw()
win.flip()
core.wait(5.0)
event.waitKeys(keyList=['q'])

core.wait(1.0)

#Review task structure
#drawstructurestims(stim=stim, stimtext=stimtext)
#step1options.draw()
#step2optionsA.draw()
#step2optionsB.draw()
#structuredemomsg.draw()
#win.flip()
#core.wait(5.0)
#event.waitKeys(keyList=['q'])

#core.wait(1.0)

# Review reward structure
#rewardstructuredemomsg.draw()
#win.flip()
#core.wait(5.0)
#event.waitKeys(keyList=['q'])

# Introduce Practice trials
practicetrialsmsg.draw()
win.flip()
core.wait(5.0)
event.waitKeys(keyList=['q'])

core.wait(1.0)

'''
------------------------------------------------------------------------------

    PRACTICE TRIALS

--------------------------------------------------------------------------------
'''

paths      = np.zeros([ntrain+1, 4])          # Initialize path array
paths[0,:] = rnd.uniform(lbound, ubound, 4)    # Set initial reward probabilities

t = 0
while t <= ntrain-1:
    for trial in range(t, ntrain):
        '''
            INTER-STIMULUS INTERVAL
        '''
        drawfixation()
        win.flip()
        core.wait(rnd.exponential(isi))

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
        core.wait(0.1)

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
        core.wait(0.1)

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

        # Increment trial number
        t += 1

donepracticemsg.draw()
win.flip()
core.wait(5.0)
event.waitKeys(keyList=['w'])

'''
================================================================================

    EXPERIMENT PROPER

================================================================================
'''

#stim, stimtext, rewardicons = initgraphics()             # Initialize the stimuli

paths      = np.zeros([ntrials+1, 4])          # Initialize path array
paths[0,:] = rnd.uniform(lbound, ubound, 4)    # Set initial reward probabilities

choices  = np.zeros([ntrials, 2])
states   = np.zeros(ntrials)                   # Only one column because step 1 state is always 0
rewards  = np.zeros(ntrials)
rt       = np.zeros([ntrials, 2])              # Store reaction times
keyarray = np.empty([ntrials, 2], dtype='<U1') # Log the keys pressed for choices


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
        core.wait(rnd.exponential(isi))

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
        core.wait(0.1)

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
        core.wait(0.1)

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
data.to_csv('data_' + subject_id + '.csv', sep='\t', encoding='utf-8', index=False)

'''
================================================================================

    CONCLUSION TEXT

================================================================================
'''

donetaskmsg.draw()
win.flip()
core.wait(5.0)
keys = event.waitKeys(keyList=['v'])

if keys[0] == 'v':
    win.close()
    core.quit()

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
