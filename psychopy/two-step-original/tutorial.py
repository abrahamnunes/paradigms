#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import core, visual, event, gui
import sys
import pandas as pd
import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt
from random import shuffle

from twostepstim import loadstimuli
from twostep_utils import *

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

transprob = 0.7 # probability of the correct transition
lbound = 0.25 # lower bound on reward probabilities
ubound = 0.75 # upper bound on reward probabilities
sdrewardpath = 0.025 # SD of the Gaussian process for reward probabilities

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
#moneyypos =
#animxpos =
#animypos =
#moneytime =
isitime = 1 # interstimulus interval
ititime = 1 # intertrial interval time mean of exponential dist
choicetime = 3.0 # time limit for choices
keyleft = 'f'
keyright = 'j'


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
tutorialstim = loadstimuli(win=win,
                           stim_set='tutorial',
                           stim_size=0.3*monitor_height)

rewardstim = loadstimuli(win=win,
                         stim_set='reward',
                         stim_size=0.3*monitor_height)

plotstim = loadstimuli(win=win,
                       stim_set='plots',
                       stim_size=0.7*monitor_height)

# Data vectors
a1 = np.zeros(ntrain)   # first level choice
a2 = np.zeros(ntrain)   # second level choice
s2 = np.zeros(ntrain)   # second level state
pos1 = np.zeros(ntrain) # positioning of first level boxes
pos2 = np.zeros(ntrain) # positioning of second level boxes
rt1  = np.zeros(ntrain) # first level reaction time
rt2  = np.zeros(ntrain) # second level reaction time
r = np.zeros(ntrain)    # reward

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
    text = 'Press any key to start the tutorial.'
).draw()
win.flip()
event.waitKeys()

"""
# Screen 2
visual.TextStim(win,
    text = 'Your goal in this experiment is to win as much money as possible.\n\n' +
    'Press the "c" key to continue.'
).draw()
win.flip()
event.waitKeys(keyList=['c'])

# Screen 3
visual.TextStim(win,
    text='In the game, you will see a pair of boxes identified by a colour and a symbol.\n\n Your job is to choose one of them',
    pos = [0, textypos['top']]
).draw()

drawatpos(tutorialstim[3][0]['norm'],
          xpos=boxpos['x']['left'],
          ypos=boxpos['y']['neutral'])
drawatpos(tutorialstim[3][1]['norm'],
          xpos=boxpos['x']['right'],
          ypos=boxpos['y']['neutral'])

visual.TextStim(win,
    text='Press "c" to continue...',
    pos = [0, textypos['bottom']]
).draw()
win.flip()
event.waitKeys(keyList=['c'])

# Screen 4
visual.TextStim(win,
    text='Each of the first type of box we will consider has a certain chance of containing a reward.\n\n' +
    'The aim is to find which box has the highest chance of reward, and choose it.',
    pos = [0, textypos['top']]
).draw()

drawatpos(tutorialstim[3][0]['norm'],
          xpos=boxpos['x']['left'],
          ypos=boxpos['y']['neutral'])
drawatpos(tutorialstim[3][1]['norm'],
          xpos=boxpos['x']['right'],
          ypos=boxpos['y']['neutral'])

visual.TextStim(win,
    text='In this tutorial, you are not playing for real money. In the actual experiment, you will be.\n\n' +
    'Press "c" to continue...',
    pos = [0, textypos['bottom']]
).draw()
win.flip()
event.waitKeys(keyList=['c'])

# Screen 5
visual.TextStim(win,
    text='For this demonstration, you will select the box you want using the keyboard.\n\n' +
    'Select the left box with the "f" key, and the right box with the "j" key.',
    pos = [0, textypos['top']]
).draw()

drawatpos(tutorialstim[3][0]['norm'],
          xpos=boxpos['x']['left'],
          ypos=boxpos['y']['neutral'])
drawatpos(tutorialstim[3][1]['norm'],
          xpos=boxpos['x']['right'],
          ypos=boxpos['y']['neutral'])

visual.TextStim(win,
    text='Press "c" to continue...',
    pos = [0, textypos['bottom']]
).draw()
win.flip()
event.waitKeys(keyList=['c'])

# Screen 6
visual.TextStim(win,
    text='Practice selecting them now, using the "f" and "j" keys.\n\n' +
    'When you select a box, it will highlight.',
    pos = [0, textypos['top']]
).draw()

drawatpos(tutorialstim[3][0]['norm'],
          xpos=boxpos['x']['left'],
          ypos=boxpos['y']['neutral'])
drawatpos(tutorialstim[3][1]['norm'],
          xpos=boxpos['x']['right'],
          ypos=boxpos['y']['neutral'])

visual.TextStim(win,
    text='The tutorial will continue after 4 presses.\n\n' +
    'Press "c" to continue...',
    pos = [0, textypos['bottom']]
).draw()
win.flip()
event.waitKeys(keyList=['c'])

for t in range(4):
    leftbox = tutorialstim[3][0]
    rightbox = tutorialstim[3][1]

    drawatpos(leftbox['norm'],
              xpos=boxpos['x']['left'],
              ypos=boxpos['y']['neutral'])
    drawatpos(rightbox['norm'],
              xpos=boxpos['x']['right'],
              ypos=boxpos['y']['neutral'])

    win.flip()
    keypress = event.waitKeys(keyList=['f', 'j'])
    if keypress[0][0] == 'f':
        drawatpos(leftbox['act'],
                  xpos=boxpos['x']['left'],
                  ypos=boxpos['y']['neutral'])
        drawatpos(rightbox['deact'],
                  xpos=boxpos['x']['right'],
                  ypos=boxpos['y']['neutral'])
    elif keypress[0][0] == 'j':
        drawatpos(leftbox['deact'],
                  xpos=boxpos['x']['left'],
                  ypos=boxpos['y']['neutral'])
        drawatpos(rightbox['act'],
                  xpos=boxpos['x']['right'],
                  ypos=boxpos['y']['neutral'])

    visual.TextStim(win,
        text='When you select a box, it will highlight.\n\n' +
        'Try selecting another box',
        pos=[0, textypos['bottom']]
    ).draw()
    win.flip()
    core.wait(3.0)

# Screen 7
visual.TextStim(win,
    text='Press any key to continue...'
).draw()
win.flip()
event.waitKeys()

# Screen 8
visual.TextStim(win,
    text='After a box is selected, you will find out the result.\n\n Press "c" key to continue...'
).draw()
win.flip()
event.waitKeys(keyList=['c'])

# Screen 9
visual.TextStim(win,
    text='It is important to understand how the computer decides whether you will win money with your choice.\n\n' +
    'To show you how this works, we will consider just one box for now.',
    pos = [0, textypos['top']]
).draw()

drawatpos(tutorialstim[4]['norm'],
          xpos=boxpos['x']['neutral'],
          ypos=boxpos['y']['neutral'])

visual.TextStim(win,
    text='Press "c" to continue...',
    pos = [0, textypos['bottom']]
).draw()
win.flip()
event.waitKeys(keyList=['c'])

# Screen 10
visual.TextStim(win,
    text='Each time you select a box, the computer flips a "weighted coin" to decide if you win.\n\n' +
    'Normally, flipping a "fair" coin gives you a 50% chance of winning, but a weighted coin might give you more or less than a 50% chance.',
    pos = [0, textypos['top']]
).draw()

drawatpos(tutorialstim[4]['norm'],
          xpos=boxpos['x']['neutral'],
          ypos=boxpos['y']['neutral'])

visual.TextStim(win,
    text='This box will give you a 60% chance of winning, but other boxes might give you more or less than a 60% chance.\n\n' +
    'During the actual task, you will have to figure out on your own what chance each box gives you of winning.\n\n' +
    'Press "c" to continue...',
    pos = [0, textypos['bottom']]
).draw()
win.flip()
event.waitKeys(keyList=['c'])

# Screen 11
visual.TextStim(win,
    text='We will now have some practice to show you what this means.\n\n' +
    'Whenever you select a box, you are essentially playing a game of chance, where your odds of winning are 60%.',
    pos = [0, textypos['top']]
).draw()

drawatpos(tutorialstim[4]['norm'],
          xpos=boxpos['x']['neutral'],
          ypos=boxpos['y']['neutral'])

visual.TextStim(win,
    text='You will now get 10 tries to see how this works. Once you continue to the next screen, press the "j" key to select the box and see what happens.\n\n' +
    'Press "c" to continue...',
    pos = [0, textypos['bottom']]
).draw()
win.flip()
event.waitKeys(keyList=['c'])

outcome = [1, 0, 0, 1, 1, 0, 1, 1, 1, 1]

for i in range(len(outcome)):
    drawatpos(tutorialstim[4]['norm'],
              xpos=boxpos['x']['neutral'],
              ypos=boxpos['y']['neutral'])

    win.flip()
    keypress = event.waitKeys(keyList=['j'])

    if keypress[0][0] == 'j':
        drawatpos(tutorialstim[4]['act'],
                  xpos=boxpos['x']['neutral'],
                  ypos=boxpos['y']['neutral'])
        win.flip()
        core.wait(0.25)

        animatechoice(win=win, stim=tutorialstim[4]['act'],
                      endpos_x=boxpos['x']['neutral'],
                      endpos_y=boxpos['y']['high'],
                      animate_duration=0.4)

        drawatpos(tutorialstim[4]['deact'],
                  xpos=boxpos['x']['neutral'],
                  ypos=boxpos['y']['high'])
        drawatpos(rewardstim[outcome[i]],
                  xpos=boxpos['x']['neutral'],
                  ypos=boxpos['y']['low'])
        win.flip()
        core.wait(2.0)

visual.TextStim(win,
    text='Total number of wins = 9\n\n' +
    'Note that rewards are marked with a coin (with the "$" sign), whereas non-rewards are marked with an empty circle.\n\n' +
    'The "non-reward" outcome (i.e. the empty circle) simply means that you did not receive a reward. It does NOT mean that you lose any rewards you have already gained.\n\n' +
    'Press any key to continue.'
).draw()
win.flip()
event.waitKeys()

# Screen 12
visual.TextStim(win,
    text='As you can see, with a total number of 7 wins in 10 trials, the odds of winning were approximately 60%, although because of randomness you got an extra win!\n\n' +
    'There are no other patterns to find in how rewards are delivered. For instance, rewards and non-rewards do not alternate.\n\n' +
    'Press any key to continue'
).draw()
win.flip()
event.waitKeys()

# Screen 13
visual.TextStim(win,
    text='Remember that some boxes will be more likely to give you rewards than others.\n\n' +
    'In the next example, one box might be better than the other one.\n\n' +
    'Press "c" to continue...'
).draw()
win.flip()
event.waitKeys(keyList=['c'])

# Screen 14
visual.TextStim(win,
    text='Try selecting from each of these boxes, to see if you can figure out which box has the highest chance of reward.',
    pos = [0, textypos['top']]
).draw()

drawatpos(tutorialstim[3][0]['norm'],
          xpos=boxpos['x']['left'],
          ypos=boxpos['y']['neutral'])
drawatpos(tutorialstim[3][1]['norm'],
          xpos=boxpos['x']['right'],
          ypos=boxpos['y']['neutral'])

visual.TextStim(win,
    text='Press "c" to continue...',
    pos = [0, textypos['bottom']]
).draw()
win.flip()
event.waitKeys(keyList=['c'])

# Screen 15a
visual.TextStim(win,
    text='Just to recap, remember that each box is identified by its symbol and its colour.',
    pos = [0, textypos['top']]
).draw()

drawatpos(tutorialstim[3][0]['norm'],
          xpos=boxpos['x']['left'],
          ypos=boxpos['y']['neutral'])
drawatpos(tutorialstim[3][1]['norm'],
          xpos=boxpos['x']['right'],
          ypos=boxpos['y']['neutral'])

visual.TextStim(win,
    text='Press any key',
    pos = [0, textypos['bottom']]
).draw()
win.flip()
event.waitKeys()

# Screen 15b
visual.TextStim(win,
    text='Sometimes a particular box will show up on the left...',
    pos = [0, textypos['top']]
).draw()

drawatpos(tutorialstim[3][0]['norm'],
          xpos=boxpos['x']['left'],
          ypos=boxpos['y']['neutral'])
drawatpos(tutorialstim[3][1]['norm'],
          xpos=boxpos['x']['right'],
          ypos=boxpos['y']['neutral'])

visual.TextStim(win,
    text='Press any key',
    pos = [0, textypos['bottom']]
).draw()
win.flip()
event.waitKeys()

# Screen 15c
visual.TextStim(win,
    text='...and sometimes it will show up on the right...',
    pos = [0, textypos['top']]
).draw()

drawatpos(tutorialstim[3][1]['norm'],
          xpos=boxpos['x']['left'],
          ypos=boxpos['y']['neutral'])
drawatpos(tutorialstim[3][0]['norm'],
          xpos=boxpos['x']['right'],
          ypos=boxpos['y']['neutral'])

visual.TextStim(win,
    text='Press any key',
    pos = [0, textypos['bottom']]
).draw()
win.flip()
event.waitKeys()

# Screen 15d
visual.TextStim(win,
    text='The side on which the box shows up does not change your chances of winning.\n\n' +
    'For instance, left is not luckier than right. Only the box (identified by the symbol and colour) matters.',
    pos = [0, textypos['top']]
).draw()

drawatpos(tutorialstim[3][1]['norm'],
          xpos=boxpos['x']['left'],
          ypos=boxpos['y']['neutral'])
drawatpos(tutorialstim[3][0]['norm'],
          xpos=boxpos['x']['right'],
          ypos=boxpos['y']['neutral'])

visual.TextStim(win,
    text='Press any key',
    pos = [0, textypos['bottom']]
).draw()
win.flip()
event.waitKeys()

# Screen 15e
visual.TextStim(win,
    text='Now try to find the better box.\n\n' +
    'You have 20 trials in this game.\n\n' +
    'Remember, press "f" for the left box, and "j" for the right box.\n\n' +
    'Press "c" to continue'
).draw()
win.flip()
event.waitKeys()

learned_reward = False
while learned_reward is False:
    # Randomize stimuli to either choice1 or choice2
    choice1_id = np.random.binomial(1, p=0.5)
    choice2_id = int(np.abs(1-choice1_id))
    choices = {
        0 : {
            'stim'  : tutorialstim[3][choice1_id],
            'rprob' : 0.75
        },
        1 : {
            'stim' : tutorialstim[3][choice2_id],
            'rprob': 0.25
        }
    }

    for t in range(20):
        # Draw each stimulus randomly on the right or left side
        left_id = np.random.binomial(1, p=0.5)
        leftchoice = {
            'choice' : choices[left_id],
            'key': 'f'
        }
        rightchoice = {
            'choice' : choices[int(np.abs(1-left_id))],
            'key': 'j'
        }
        drawatpos(stim=leftchoice['choice']['stim']['norm'],
                  xpos=boxpos['x']['left'],
                  ypos=boxpos['y']['neutral'])
        drawatpos(stim=rightchoice['choice']['stim']['norm'],
                  xpos=boxpos['x']['right'],
                  ypos=boxpos['y']['neutral'])

        win.flip()
        keypress = event.waitKeys(keyList=['f', 'j'])

        if keypress[0][0] == 'f':
            drawatpos(stim=leftchoice['choice']['stim']['act'],
                      xpos=boxpos['x']['left'],
                      ypos=boxpos['y']['neutral'])
            drawatpos(stim=rightchoice['choice']['stim']['deact'],
                      xpos=boxpos['x']['right'],
                      ypos=boxpos['y']['neutral'])
            win.flip()
            core.wait(0.25)

            animatechoice(win=win, stim=leftchoice['choice']['stim']['act'], endpos_x=boxpos['x']['neutral'], endpos_y=boxpos['y']['high'])

            drawatpos(stim=leftchoice['choice']['stim']['deact'],
                      xpos=boxpos['x']['neutral'],
                      ypos=boxpos['y']['high'])

            win.flip()
            core.wait(0.25)

            # Compute reward
            wl = np.random.binomial(1, p=leftchoice['choice']['rprob'])
            drawatpos(stim=leftchoice['choice']['stim']['deact'],
                      xpos=boxpos['x']['neutral'],
                      ypos=boxpos['y']['high'])
            drawatpos(stim=rewardstim[wl],
                      xpos=boxpos['x']['neutral'],
                      ypos=boxpos['y']['low'])
            win.flip()
            core.wait(1)

        elif keypress[0][0] == 'j':
            drawatpos(stim=leftchoice['choice']['stim']['deact'],
                      xpos=boxpos['x']['left'],
                      ypos=boxpos['y']['neutral'])
            drawatpos(stim=rightchoice['choice']['stim']['act'],
                      xpos=boxpos['x']['right'],
                      ypos=boxpos['y']['neutral'])
            win.flip()
            core.wait(0.25)

            animatechoice(win=win, stim=rightchoice['choice']['stim']['act'], endpos_x=boxpos['x']['neutral'], endpos_y=boxpos['y']['high'])

            drawatpos(stim=rightchoice['choice']['stim']['deact'],
                      xpos=boxpos['x']['neutral'],
                      ypos=boxpos['y']['high'])

            win.flip()
            core.wait(0.25)

            # Compute reward
            wl = np.random.binomial(1, p=rightchoice['choice']['rprob'])
            drawatpos(stim=rightchoice['choice']['stim']['deact'],
                      xpos=boxpos['x']['neutral'],
                      ypos=boxpos['y']['high'])
            drawatpos(stim=rewardstim[wl],
                      xpos=boxpos['x']['neutral'],
                      ypos=boxpos['y']['low'])
            win.flip()
            core.wait(1)

    # Check if they learned correctly
    visual.TextStim(win,
        text='Which box was the better one?\n\n' +
        'Press "f" for the left box, and "j" for the right box.',
        pos=[0, textypos['top']]
    ).draw()

    drawatpos(choices[0]['stim']['norm'],
              xpos=boxpos['x']['left'],
              ypos=boxpos['y']['neutral'])
    drawatpos(choices[1]['stim']['norm'],
              xpos=boxpos['x']['right'],
              ypos=boxpos['y']['neutral'])

    win.flip()
    keypress = event.waitKeys(keyList=['f', 'j'])

    if keypress[0][0] == 'f':
        visual.TextStim(win,
            text='Correct!\n\n' +
            'If you were playing for real, then you would want to choose it, since it would give you the most reward.',
            pos=[0, textypos['top']]
        ).draw()
        drawatpos(choices[0]['stim']['act'],
                  xpos=boxpos['x']['left'],
                  ypos=boxpos['y']['neutral'])
        drawatpos(choices[1]['stim']['deact'],
                  xpos=boxpos['x']['right'],
                  ypos=boxpos['y']['neutral'])
        visual.TextStim(win,
            text='Press "c" to continue',
            pos=[0, textypos['bottom']]
        ).draw()
        win.flip()
        event.waitKeys(keyList=['c'])
        learned_reward = True
    elif keypress[0][0] == 'j':
        visual.TextStim(win,
            text='Looks like you might need some more practice.\n\n' +
            'Take another shot at figuring out which one is best.\n\n' +
            'Note that the best box might change now, so it is important that you try to learn which one is best through experience.',
            pos=[0, textypos['top']]
        ).draw()
        drawatpos(choices[0]['stim']['deact'],
                  xpos=boxpos['x']['left'],
                  ypos=boxpos['y']['neutral'])
        drawatpos(choices[1]['stim']['act'],
                  xpos=boxpos['x']['right'],
                  ypos=boxpos['y']['neutral'])
        visual.TextStim(win,
            text='Press "c" to continue',
            pos=[0, textypos['bottom']]
        ).draw()
        win.flip()
        event.waitKeys(keyList=['c'])

# Screen 16
visual.TextStim(win,
    text='The actual game will be harder for two reasons.\n\n' +
    'First, there are more boxes to keep track of (we will go over this more in a moment)\n\n' +
    'Second, the chance that a box contains money will change slowly over time. We wil go over this point in more detail now.\n\n' +
    'Press "c" to continue.'
).draw()
win.flip()
event.waitKeys(keyList=['c'])

# Screen 17
visual.TextStim(win,
    text='Since the chances of getting a reward in each box will change slowly, a box that starts out better can become worse later on.\n\n' +
    'Alternatively, a box that starts out worse can become better later on.\n\n' +
    'This means that to find the box that is best right now, you will need to stay concentrated throughout the task.\n\n' +
    'Press any key to continue.'
).draw()
win.flip()
event.waitKeys()

# Screen 18
visual.TextStim(win,
    text='The chances of getting reward at each box can change, but they can also stay more or less the same.\n\n' +
    'They can also change back and forth, or many other patterns.\n\n' +
    'The change is completely unpredictable, but it will always be slow. This means that a box that is good now will probably remain pretty good for a while.\n\n' +
    'Press any key to continue.'
).draw()
win.flip()
event.waitKeys()


# Screen 19
visual.TextStim(win,
    text='To illustrate this, let us again consider just one box\n\n' +
    'Here is an example of how the chance of wins might start off.\n\n' +
    'Initially, there is a 60% chance of winning.',
    pos=[0, textypos['top']]
).draw()
drawatpos(tutorialstim[4]['norm'],
          xpos=boxpos['x']['left'],
          ypos=boxpos['y']['neutral'])
drawatpos(plotstim['s1t1'],
          xpos=boxpos['x']['right'],
          ypos=boxpos['y']['low'])
visual.TextStim(win,
    text='Press any key',
    pos=[0, -0.6*monitor_height]
).draw()
win.flip()
event.waitKeys()

#Screen 20
visual.TextStim(win,
    text='Over the next few trials the chance of winning is similar...',
    pos=[0, textypos['top']]
).draw()
drawatpos(tutorialstim[4]['norm'],
          xpos=boxpos['x']['left'],
          ypos=boxpos['y']['neutral'])
drawatpos(plotstim['s1t6'],
          xpos=boxpos['x']['right'],
          ypos=boxpos['y']['low'])
visual.TextStim(win,
    text='Press any key',
    pos=[0, -0.6*monitor_height]
).draw()
win.flip()
event.waitKeys()

#Screen 21
visual.TextStim(win,
    text='But over many trials, your chances of winning a reward can change dramatically...',
    pos=[0, textypos['top']]
).draw()
drawatpos(tutorialstim[4]['norm'],
          xpos=boxpos['x']['left'],
          ypos=boxpos['y']['neutral'])
drawatpos(plotstim['s1t60'],
          xpos=boxpos['x']['right'],
          ypos=boxpos['y']['low'])
visual.TextStim(win,
    text='Press any key',
    pos=[0, -0.6*monitor_height]
).draw()
win.flip()
event.waitKeys()

#Screen 22
visual.TextStim(win,
    text='Later on, the box might improve again.\n\nThis plot below shows only some improvement at the end, but in the real task the boxes can sometimes become even better than they ever were.',
    pos=[0, textypos['top']]
).draw()
drawatpos(tutorialstim[4]['norm'],
          xpos=boxpos['x']['left'],
          ypos=boxpos['y']['neutral'])
drawatpos(plotstim['s1tw'],
          xpos=boxpos['x']['right'],
          ypos=boxpos['y']['low'])
visual.TextStim(win,
    text='Press any key',
    pos=[0, -0.6*monitor_height]
).draw()
win.flip()
event.waitKeys()

#Screen 23
visual.TextStim(win,
    text='Imagine you were choosing this box repeatedly.\n\n' +
    'You would get rewards sometimes (shown by the black dots over the line), but other times not.\n\n' +
    'Notice that when the chances of reward are highest for this box (e.g. when the blue line is highest), there are more black dots over it. When the chances are low, there still might be some rewards, but not as often.',
    pos=[0, textypos['top']]
).draw()
drawatpos(tutorialstim[4]['norm'],
          xpos=boxpos['x']['left'],
          ypos=boxpos['y']['neutral'])
drawatpos(plotstim['s1twr'],
          xpos=boxpos['x']['right'],
          ypos=boxpos['y']['low'])
visual.TextStim(win,
    text='Press any key',
    pos=[0, -0.6*monitor_height]
).draw()
win.flip()
event.waitKeys()

#Screen 23
visual.TextStim(win,
    text='The red line here shows the chances of winning with another potential box. It starts off worse than the first box, but at one point becomes better before dropping off again.\n\n' +
    'This highlights the importance of staying focused throughout the task, since you will want to know which boxes are the best at any given moment.',
    pos=[0, textypos['top']]
).draw()
drawatpos(tutorialstim[4]['norm'],
          xpos=boxpos['x']['left'],
          ypos=boxpos['y']['neutral'])
drawatpos(tutorialstim[3][0]['norm'],
          xpos=boxpos['x']['left'],
          ypos=boxpos['y']['neutral']-0.35*monitor_height)
drawatpos(plotstim['s2tw'],
          xpos=boxpos['x']['right'],
          ypos=boxpos['y']['low'])
visual.TextStim(win,
    text='Press any key',
    pos=[0, -0.6*monitor_height]
).draw()
win.flip()
event.waitKeys()

#Screen 23
visual.TextStim(win,
    text='Remember, these are just examples for now. In the real game, the boxes can show many different patterns of change.',
    pos=[0, textypos['top']]
).draw()
drawatpos(tutorialstim[4]['norm'],
          xpos=boxpos['x']['left'],
          ypos=boxpos['y']['neutral'])
drawatpos(tutorialstim[3][0]['norm'],
          xpos=boxpos['x']['left'],
          ypos=boxpos['y']['neutral']-0.35*monitor_height)
drawatpos(plotstim['s2tw'],
          xpos=boxpos['x']['right'],
          ypos=boxpos['y']['low'])
visual.TextStim(win,
    text='Press any key',
    pos=[0, -0.6*monitor_height]
).draw()
win.flip()
event.waitKeys()
"""

#Screen 24
visual.TextStim(win,
    text='You are almost ready to try out the full game, but there is one more complication: more boxes.\n\n' +
    'Press "c" to continue.'
).draw()
win.flip()
event.waitKeys(keyList=['c'])

# Screen 25
visual.TextStim(win,
    text='In particular, there are two pairs of boxes containing money. Each pair has its own colour and will always be presented together (i.e. you never see boxes of different colours presented together).',
    pos=[0, textypos['top']]
).draw()

drawatpos(tutorialstim[1][0]['norm'],
          xpos=boxpos['x']['left'],
          ypos=boxpos['y']['neutral']+0.1*monitor_height)
drawatpos(tutorialstim[1][1]['norm'],
        xpos=boxpos['x']['right'],
        ypos=boxpos['y']['neutral']+0.1*monitor_height)
drawatpos(tutorialstim[2][0]['norm'],
          xpos=boxpos['x']['left'],
          ypos=boxpos['y']['neutral']-0.35*monitor_height)
drawatpos(tutorialstim[2][1]['norm'],
        xpos=boxpos['x']['right'],
        ypos=boxpos['y']['neutral']-0.35*monitor_height)

visual.TextStim(win,
    text='Press any key',
    pos=[0, -0.6*monitor_height]
).draw()
win.flip()
event.waitKeys()

# Screen 26
visual.TextStim(win,
    text='There is also a third pair of boxes.\n\n' +
    'In the game, you start each trial by choosing between these two.\n\n' +
    'Rather than having some chance of giving you money, these have a chance of giving you either of the two pairs of money boxes, which you then choose between to win money (as before).',
    pos=[0, textypos['top']]
).draw()

drawatpos(tutorialstim[0][0]['norm'],
          xpos=boxpos['x']['left'],
          ypos=boxpos['y']['neutral'])
drawatpos(tutorialstim[0][1]['norm'],
        xpos=boxpos['x']['right'],
        ypos=boxpos['y']['neutral'])

visual.TextStim(win,
    text='Press any key',
    pos=[0, textypos['bottom']]
).draw()
win.flip()
event.waitKeys()

# Screen 27
visual.TextStim(win,
    text='Give it a try. Choose between one of these boxes and notice that you will then be shown one of the two pairs of money boxes.\n\nThen choose between the money boxes to get a chance at winning a reward.\n\nRemember use "f" to select the left box, and "j" to select the right box.',
    pos=[0, textypos['top']]
).draw()

drawatpos(tutorialstim[0][0]['norm'],
          xpos=boxpos['x']['left'],
          ypos=boxpos['y']['neutral'])
drawatpos(tutorialstim[0][1]['norm'],
        xpos=boxpos['x']['right'],
        ypos=boxpos['y']['neutral'])
win.flip()

keypress = event.waitKeys(keyList=['f', 'j'])

if keypress[0][0] == 'f':
    drawatpos(tutorialstim[0][0]['act'],
              xpos=boxpos['x']['left'],
              ypos=boxpos['y']['neutral'])
    drawatpos(tutorialstim[0][1]['deact'],
            xpos=boxpos['x']['right'],
            ypos=boxpos['y']['neutral'])

    core.wait(0.5)
    win.flip()

    animatechoice(win=win,
                  stim=tutorialstim[0][0]['act'],
                  endpos_x=boxpos['x']['neutral'],
                  endpos_y=boxpos['y']['high'])

    drawatpos(tutorialstim[0][0]['deact'],
              xpos=boxpos['x']['neutral'],
              ypos=boxpos['y']['high'])

    visual.TextStim(win,
        text='Now you will see a pair of the money boxes show up.\n\nChoose between them, like you did before.'
    ).draw()
    win.flip()
    core.wait(5)

    drawatpos(tutorialstim[0][0]['deact'],
              xpos=boxpos['x']['neutral'],
              ypos=boxpos['y']['high'])
    drawatpos(tutorialstim[1][0]['norm'],
              xpos=boxpos['x']['left'],
              ypos=boxpos['y']['neutral'])
    drawatpos(tutorialstim[1][1]['norm'],
            xpos=boxpos['x']['right'],
            ypos=boxpos['y']['neutral'])
    win.flip()
    keypress = event.waitKeys(keyList=['f', 'j'])

    if keypress[0][0] == 'f':
        drawatpos(tutorialstim[0][0]['deact'],
                  xpos=boxpos['x']['neutral'],
                  ypos=boxpos['y']['high'])
        drawatpos(tutorialstim[1][0]['act'],
                  xpos=boxpos['x']['left'],
                  ypos=boxpos['y']['neutral'])
        drawatpos(tutorialstim[1][1]['deact'],
                xpos=boxpos['x']['right'],
                ypos=boxpos['y']['neutral'])
        win.flip()
        core.wait(1)

        animatechoice(win=win,
                      stim=tutorialstim[1][0]['act'],
                      endpos_x=boxpos['x']['neutral'],
                      endpos_y=boxpos['y']['high'])
        drawatpos(tutorialstim[1][0]['deact'],
                  xpos=boxpos['x']['neutral'],
                  ypos=boxpos['y']['high'])
        win.flip()
        core.wait(1)
        drawatpos(tutorialstim[1][0]['deact'],
                  xpos=boxpos['x']['neutral'],
                  ypos=boxpos['y']['high'])
        drawatpos(rewardstim[1],
                  xpos=boxpos['x']['neutral'],
                  ypos=boxpos['y']['low'])
        win.flip()
        core.wait(2)

    elif keypress[0][0] == 'j':
        drawatpos(tutorialstim[0][0]['deact'],
                  xpos=boxpos['x']['neutral'],
                  ypos=boxpos['y']['high'])
        drawatpos(tutorialstim[1][0]['deact'],
                  xpos=boxpos['x']['left'],
                  ypos=boxpos['y']['neutral'])
        drawatpos(tutorialstim[1][1]['act'],
                xpos=boxpos['x']['right'],
                ypos=boxpos['y']['neutral'])
        win.flip()
        core.wait(1)

        animatechoice(win=win,
                      stim=tutorialstim[1][1]['act'],
                      endpos_x=boxpos['x']['neutral'],
                      endpos_y=boxpos['y']['high'])
        drawatpos(tutorialstim[1][1]['deact'],
                  xpos=boxpos['x']['neutral'],
                  ypos=boxpos['y']['high'])
        win.flip()
        core.wait(1)
        drawatpos(tutorialstim[1][1]['deact'],
                  xpos=boxpos['x']['neutral'],
                  ypos=boxpos['y']['high'])
        drawatpos(rewardstim[1],
                  xpos=boxpos['x']['neutral'],
                  ypos=boxpos['y']['low'])
        win.flip()
        core.wait(2)

elif keypress[0][0] == 'j':
    drawatpos(tutorialstim[0][0]['deact'],
              xpos=boxpos['x']['left'],
              ypos=boxpos['y']['neutral'])
    drawatpos(tutorialstim[0][1]['act'],
            xpos=boxpos['x']['right'],
            ypos=boxpos['y']['neutral'])

    core.wait(0.5)
    win.flip()

    animatechoice(win=win,
                  stim=tutorialstim[0][1]['act'],
                  endpos_x=boxpos['x']['neutral'],
                  endpos_y=boxpos['y']['high'])

    drawatpos(tutorialstim[0][1]['deact'],
              xpos=boxpos['x']['neutral'],
              ypos=boxpos['y']['high'])

    visual.TextStim(win,
        text='Now you will see a pair of the money boxes show up.\n\nChoose between them, like you did before.'
    ).draw()
    win.flip()
    core.wait(5)

    drawatpos(tutorialstim[0][1]['deact'],
              xpos=boxpos['x']['neutral'],
              ypos=boxpos['y']['high'])
    drawatpos(tutorialstim[1][0]['norm'],
              xpos=boxpos['x']['left'],
              ypos=boxpos['y']['neutral'])
    drawatpos(tutorialstim[1][1]['norm'],
            xpos=boxpos['x']['right'],
            ypos=boxpos['y']['neutral'])
    win.flip()
    keypress = event.waitKeys(keyList=['f', 'j'])

    if keypress[0][0] == 'f':
        drawatpos(tutorialstim[0][1]['deact'],
                  xpos=boxpos['x']['neutral'],
                  ypos=boxpos['y']['high'])
        drawatpos(tutorialstim[1][0]['act'],
                  xpos=boxpos['x']['left'],
                  ypos=boxpos['y']['neutral'])
        drawatpos(tutorialstim[1][1]['deact'],
                xpos=boxpos['x']['right'],
                ypos=boxpos['y']['neutral'])
        win.flip()
        core.wait(1)

        animatechoice(win=win,
                      stim=tutorialstim[1][0]['act'],
                      endpos_x=boxpos['x']['neutral'],
                      endpos_y=boxpos['y']['high'])
        drawatpos(tutorialstim[1][0]['deact'],
                  xpos=boxpos['x']['neutral'],
                  ypos=boxpos['y']['high'])
        win.flip()
        core.wait(1)
        drawatpos(tutorialstim[1][0]['deact'],
                  xpos=boxpos['x']['neutral'],
                  ypos=boxpos['y']['high'])
        drawatpos(rewardstim[1],
                  xpos=boxpos['x']['neutral'],
                  ypos=boxpos['y']['low'])
        win.flip()
        core.wait(2)

    elif keypress[0][0] == 'j':
        drawatpos(tutorialstim[0][1]['deact'],
                  xpos=boxpos['x']['neutral'],
                  ypos=boxpos['y']['high'])
        drawatpos(tutorialstim[1][0]['deact'],
                  xpos=boxpos['x']['left'],
                  ypos=boxpos['y']['neutral'])
        drawatpos(tutorialstim[1][1]['act'],
                xpos=boxpos['x']['right'],
                ypos=boxpos['y']['neutral'])

        win.flip()
        core.wait(1)

        animatechoice(win=win,
                      stim=tutorialstim[1][1]['act'],
                      endpos_x=boxpos['x']['neutral'],
                      endpos_y=boxpos['y']['high'])
        drawatpos(tutorialstim[1][1]['deact'],
                  xpos=boxpos['x']['neutral'],
                  ypos=boxpos['y']['high'])
        win.flip()
        core.wait(1)
        drawatpos(tutorialstim[1][1]['deact'],
                  xpos=boxpos['x']['neutral'],
                  ypos=boxpos['y']['high'])
        drawatpos(rewardstim[1],
                  xpos=boxpos['x']['neutral'],
                  ypos=boxpos['y']['low'])
        win.flip()
        core.wait(2)

#Screen 28
visual.TextStim(win,
    text='Just like the money boxes, these boxes are somewhat unpredictable.',
    pos=[0, textypos['top']]
).draw()
drawatpos(tutorialstim[0][0]['norm'],
          xpos=boxpos['x']['left'],
          ypos=boxpos['y']['neutral'])
drawatpos(tutorialstim[0][1]['norm'],
          xpos=boxpos['x']['right'],
          ypos=boxpos['y']['neutral'])
visual.TextStim(win,
    text='Press any key',
    pos=[0, textypos['bottom']]
).draw()
win.flip()
event.waitKeys()

visual.TextStim(win,
    text='For instance, this one might lead to the purple boxes 7 times out of 10, and to the turquoise boxes 3 out of 10 times.',
    pos=[0, textypos['top']]
).draw()
drawatpos(tutorialstim[0][0]['act'],
          xpos=boxpos['x']['left'],
          ypos=boxpos['y']['neutral'])
drawatpos(tutorialstim[0][1]['deact'],
          xpos=boxpos['x']['right'],
          ypos=boxpos['y']['neutral'])
visual.TextStim(win,
    text='Press any key',
    pos=[0, textypos['bottom']]
).draw()
win.flip()
event.waitKeys()

visual.TextStim(win,
    text='Whereas this one might lead to the turquoise boxes 7 out of 10 times, and to the purple boxes 3 out of 10 times.',
    pos=[0, textypos['top']]
).draw()
drawatpos(tutorialstim[0][0]['deact'],
          xpos=boxpos['x']['left'],
          ypos=boxpos['y']['neutral'])
drawatpos(tutorialstim[0][1]['act'],
          xpos=boxpos['x']['right'],
          ypos=boxpos['y']['neutral'])
visual.TextStim(win,
    text='If these were the chances, and the box with the most money were a turquoise box, then at the first step you would want to choose the highlighted box above.\n\n'+
    'Again, what matters is the box colour and symbol, not what side it appears on.\n\n' +
    'Press any key',
    pos=[0, textypos['bottom']]
).draw()
win.flip()
event.waitKeys()

visual.TextStim(win,
    text='Unlike the chances of finding money in the other boxes, the chances of these boxes leading to different coloured money boxes do NOT change over time.',
    pos=[0, textypos['top']]
).draw()
drawatpos(tutorialstim[0][0]['norm'],
          xpos=boxpos['x']['left'],
          ypos=boxpos['y']['neutral'])
drawatpos(tutorialstim[0][1]['norm'],
          xpos=boxpos['x']['right'],
          ypos=boxpos['y']['neutral'])
visual.TextStim(win,
    text='Of course, you will still have to figure out what they are.\n\n'+
    'Press any key',
    pos=[0, textypos['bottom']]
).draw()
win.flip()
event.waitKeys()

visual.TextStim(win,
    text='Note that when you choose a purple or turquoise box, your chance of winning money depends only on its colour and symbol, not which orange box you chose to get it.\n\n' + 'The choice you make between the orange boxes is still important because it can help you get whichever pair of money boxes contains more money.',
    pos=[0, textypos['top']]
).draw()
drawatpos(tutorialstim[0][0]['norm'],
          xpos=boxpos['x']['left'],
          ypos=boxpos['y']['neutral'])
drawatpos(tutorialstim[0][1]['norm'],
          xpos=boxpos['x']['right'],
          ypos=boxpos['y']['neutral'])
visual.TextStim(win,
    text='Of course, the best money box will change over time.\n\n'+
    'Press any key',
    pos=[0, textypos['bottom']]
).draw()
win.flip()
event.waitKeys()

# Screen 29
visual.TextStim(win,
    text='This may all sound complicated, so lets review.\n\n' +
    'Press "c" to continue',
    pos=[0, textypos['top']]
).draw()
win.flip()
event.waitKeys(keyList=['c'])

# Screen 30
visual.TextStim(win,
    text='These boxes are two games of figuring out which one has a better chance of money.\n\n' +
    'For each box, the chances of winning money changes slowly over time in a random way.',
    pos=[0, textypos['top']]
).draw()

drawatpos(tutorialstim[1][0]['norm'],
          xpos=boxpos['x']['left'],
          ypos=boxpos['y']['neutral']+0.1*monitor_height)
drawatpos(tutorialstim[1][1]['norm'],
        xpos=boxpos['x']['right'],
        ypos=boxpos['y']['neutral']+0.1*monitor_height)
drawatpos(tutorialstim[2][0]['norm'],
          xpos=boxpos['x']['left'],
          ypos=boxpos['y']['neutral']-0.35*monitor_height)
drawatpos(tutorialstim[2][1]['norm'],
        xpos=boxpos['x']['right'],
        ypos=boxpos['y']['neutral']-0.35*monitor_height)

visual.TextStim(win,
    text='Press any key',
    pos=[0, -0.6*monitor_height]
).draw()
win.flip()
event.waitKeys()

# Screen 31
visual.TextStim(win,
    text='On top of that game is another one of figuring out which box is better.\n\n' +
    'This is also like what you played before, except with these boxes.',
    pos=[0, textypos['top']]
).draw()
drawatpos(tutorialstim[0][0]['norm'],
          xpos=boxpos['x']['left'],
          ypos=boxpos['y']['neutral'])
drawatpos(tutorialstim[0][1]['norm'],
          xpos=boxpos['x']['right'],
          ypos=boxpos['y']['neutral'])
visual.TextStim(win,
    text='You dont win money directly: you win the chance to win money in the other game. That is, a better box will take you to a game with a better chance of winning money.\n\n'+
    'Press any key',
    pos=[0, textypos['bottom']]
).draw()
win.flip()
event.waitKeys()

# Screen 32
visual.TextStim(win,
    text='Lets put it all together into an example game.\n\nIn this practice you wont be winning real money.\n\nYou will do the task for 50 trials, which is less than 10 minutes.\n\n' +
    'Press any key to continue',
    pos=[0, textypos['top']]
).draw()
win.flip()
event.waitKeys()

visual.TextStim(win,
    text='If you take too long to make a choice, the trial will abort.\n\nIn this case, you will see the red Xs on the screen and a new trial will start.',
    pos=[0, textypos['top']]
).draw()
drawatpos(tutorialstim[0][0]['spoiled'],
          xpos=boxpos['x']['left'],
          ypos=boxpos['y']['neutral'])
drawatpos(tutorialstim[0][1]['spoiled'],
          xpos=boxpos['x']['right'],
          ypos=boxpos['y']['neutral'])
visual.TextStim(win,
    text='Dont feel rushed, but please try to enter a choice on every trial.\n\n'+
    'Press any key',
    pos=[0, textypos['bottom']]
).draw()
win.flip()
event.waitKeys()

# Screen 33
visual.TextStim(win,
    text='Good luck! Remember that "f" selects left and "j" selects right.\n\nPress "c" to start the practice.',
    pos=[0, textypos['top']]
).draw()
win.flip()
event.waitKeys(keyList=['c'])

"""
================================================================================

    PRACTICE TRIALS

================================================================================
"""

np.random.seed(seed=333)
# Assign reward and transition probabilities to stimuli
stimset = activate_stimuli(step1_stim=tutorialstim[0],
                           step2_stimA=tutorialstim[1],
                           step2_stimB=tutorialstim[2])

for t in range(ntrials):

    # First level


    # Transition
    # Second level


win.close()
core.quit()
