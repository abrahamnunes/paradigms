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
mygui = gui.DlgFromDict(dictionary=infodict, title='OPSPAN')

subject_id = infodict['Subject ID'].encode('utf8')

if subject_id == '': # If no subject ID entered, quit.
    core.quit()

'''
================================================================================

    EXPERIMENTAL PARAMETERS

================================================================================
'''

span_low      = 3
span_high     = 7

nmathpractice = 15 #As per Unsworth et al. ￼Behavior Research Methods 2005, 37 (3), 498-505
nspaniterations = 3 #3 #As per Unsworth et al. ￼Behavior Research Methods 2005, 37 (3), 498-505

fullscreen = True
if fullscreen is True:
    monitor_width  = 1024.
    monitor_height = 768.
else:
    monitor_width = (1024/768)*700
    monitor_height = 700

'''
================================================================================

    SET UP COMPONENTS

================================================================================
'''

win = visual.Window(
    [monitor_width, monitor_height],
    monitor="testMonitor",
    fullscr=fullscreen,
    units='pix'
    )

equationtext = visual.TextStim(win,
    height=0.05*monitor_height,
    font='DejaVu Sans',
    color=[1, 1, 1]
)
lettertext   = visual.TextStim(win,
    height=0.05*monitor_height,
    font='DejaVu Sans',
    color=[1, 1, 1]
)

# Load operations and letters
equations = np.loadtxt('resources/operations.txt',
                        delimiter='\t',
                        dtype='string'
)

characters = np.loadtxt('resources/consonants.txt',
                        delimiter='\t',
                        dtype='string'
)

'''
===============================================================================

    TEXT AND BUTTON COMPONENTS

===============================================================================
'''

intromessage = visual.TextStim(win,
    text='Thank you for participating in this study.\n\n' +
         'In the following activity, you will be asked to specify whether ' +
         'the equation displayed is true or false. After you respond, a ' +
         'letter will appear. You will be asked to remember that letter ' +
         'after a certain number of trials are completed.\n\n' +
         'Before we begin with the task, we will have some practice.\n\n' +
         'Press any key to continue...'
)

characterpracticemessage = visual.TextStim(win,
    text='First, we will begin by practicing letter recall.\n\n' +
         'You will be presented with a sequence of letters, one at a time.\n' +
         'Once all the letters have been presented, you will see a vertical bar (a cursor), indicating that you should input your answers. Please type in the letters IN THE ORDER THEY APPEARED. If you make a mistake, simply hit "backspace" button. There is no need to separate characters with spaces or commas.\n\n' +
         'Please answer as accurately and quickly as possible.\n\n' +
         'Press any key to continue.'
)

equationpracticemessage = visual.TextStim(win,
    text='Next, we will be practicing solving the equations.\n\n' +
         'You will be presented with an equation such as the following: \n' +
         '(5-1) X 2 = 9\n' +
         'Your job is to determine whether the equation is correct or incorrect.\n\n' +
         'If the equation is CORRECT, press the "j" key.\n' +
         'If the equation is INCORRECT, press the "f" key.\n\n' +
         'Please answer as accurately and quickly as possible.\n\n' +
         'Press any key to continue.'
)

fullpracticemessage = visual.TextStim(win,
    text='Now that you understand the process of solving the equations, we will practice the full task.\n\n' +
         'After you have specified whether the equation displayed is correct or incorrect, a single letter will be displayed for a brief period of time. There will be a series of equation & answer pairs, after which you will be asked to recall the letters IN THE ORDER THEY APPEARED by typing them in. If you make a mistake, simply hit "backspace" button. There is no need to separate characters with spaces or commas.\n\n' +
         'Please answer as quickly as possible, but accuracy is most important.\n\n' +
         'Press any key to continue.'
)

taskmessage = visual.TextStim(win,
    text='Now that you understand how to do the task, we will move on to the actual task itself. It is essentially the same as this last practice session, except that you will not be given any feedback, and the length of sequences you need to remember will vary.\n\n' +
         'Despite not having any feedback from now on, please continue to answer as quickly as possible, but accuracy is most important.\n\n' +
         'Press any key to continue.'
)

congratsmessage = visual.TextStim(win,
    text='Excellent job!'
)

#fastermessage = visual.TextStim(win,
#    text='You must answer faster!'
#)

incorrectanswermessage = visual.TextStim(win,
    text='Incorrect answer. Keep trying!'
)

completemessage = visual.TextStim(win,
    text='Congratulations! You have successfully completed this task.\n\n'
)

truebutton = visual.Rect(win,
    height=0.12*monitor_height,
    width=0.12*monitor_width,
    pos=[0.25*monitor_width, -0.25*monitor_height]
)

falsebutton = visual.Rect(win,
    height=0.12*monitor_height,
    width=0.12*monitor_width,
    pos=[-0.25*monitor_width, -0.25*monitor_height]
)

truebuttontext = visual.TextStim(win,
    text='True',
    pos=[0.25*monitor_width, -0.25*monitor_height],
    height=0.05*monitor_height
)

falsebuttontext = visual.TextStim(win,
    text='False',
    pos=[-0.25*monitor_width, -0.25*monitor_height],
    height=0.05*monitor_height
)

'''
===============================================================================

    FUNCTIONS

===============================================================================
'''

def check_equation_answer(keyin,answer):
    if keyin == 'j' and answer == 'y':
        score = 1
    elif keyin == 'f' and answer == 'n':
        score = 1
    else:
        score = 0
    return score

def drawequation(equations):
    equationindex = rnd.randint(np.size(equations, axis=0)-1, size=1)[0]
    answer = equations[equationindex, 1]
    equationtext.text = equations[equationindex, 0].decode('utf8')
    equationtext.draw()
    return answer, equationtext.text


def getcharacterinput():
    linecursor = visual.Line(win, units='pix', start=[0, -0.05*monitor_height], end=[0, 0.05*monitor_height])
    response = visual.TextStim(win, text='',units='pix', height=0.07*monitor_height)

    linecursor.draw()
    win.flip()

    enterkey = False
    while enterkey is False:
        keys = event.waitKeys(
            keyList=['q','w','e','r','t','y','u','i','o','p',
                     'a','s','d','f','g','h','j','k','l',
                     'z','x','c','v','b','n','m','return','backspace']
            )
        if keys[0] != 'return':
            if keys[0] != 'backspace':
                response.text = response.text + ' ' + keys[0]
                response.draw()

                linecursor.start = linecursor.start + [0.03*monitor_height, 0]
                linecursor.end = linecursor.end + [0.03*monitor_height, 0]
                linecursor.draw()
                win.flip()
            else:
                response.text = response.text[0:len(response.text)-2]
                response.draw()

                if len(response.text) > 0:
                    linecursor.start = linecursor.start - [0.03*monitor_height, 0]
                    linecursor.end = linecursor.end - [0.03*monitor_height, 0]
                    linecursor.draw()
                else:
                    linecursor.start = [0, -0.05*monitor_height]
                    linecursor.end   = [0, 0.05*monitor_height]
                    linecursor.draw()
                win.flip()
        else:
            enterkey = True

    return response.text

def drawbuttons(keysel=None):
    buttonfillcolors = {'truebutton'  : [0.02, 0.5, -0.32],
                        'falsebutton' : [0.82, -0.34, -0.422],
                        'selected'    : [-1, -0.48, 0.99]}

    if keysel == 'j':
        truebutton.fillColor = buttonfillcolors['selected']
        falsebutton.fillColor = buttonfillcolors['falsebutton']
    elif keysel == 'f':
        truebutton.fillColor = buttonfillcolors['truebutton']
        falsebutton.fillColor = buttonfillcolors['selected']
    else:
        truebutton.fillColor = buttonfillcolors['truebutton']
        falsebutton.fillColor = buttonfillcolors['falsebutton']
    truebutton.draw()
    falsebutton.draw()
    truebuttontext.draw()
    falsebuttontext.draw()

'''
===============================================================================

    RUN EXPERIMENT

===============================================================================
'''

'''
-------------------------------------------------------------------------------

    INTRODUCTION

-------------------------------------------------------------------------------
'''


intromessage.draw()
win.flip()
event.waitKeys()

'''
-------------------------------------------------------------------------------

    CHARACTER PRACTICE

-------------------------------------------------------------------------------
'''

characterpracticemessage.draw()
win.flip()
event.waitKeys()

spanseq = np.linspace(span_low, span_high, (span_high-span_low)+1)

#show empty screen for a second (so that trials don't start immediately)
win.flip()
core.wait(1.0)

ncorrect = 0
for i in range(0, len(spanseq)):
    shuffle(characters)
    answer = '';
    for t in range(0, int(spanseq[i])):
        lettertext.text = characters[t]
        answer = answer + ' ' + characters[t]
        lettertext.draw()
        win.flip()
        core.wait(0.8)

        win.flip()
        core.wait(1.0)

    response = getcharacterinput()
    if response == answer:
        ncorrect = ncorrect + 1
        congratsmessage.draw()
        win.flip()
        core.wait(1.0)

        if ncorrect == len(spanseq):
            break
    else:
        incorrectanswermessage.draw()
        win.flip()
        core.wait(1.0)

'''
-------------------------------------------------------------------------------

    EQUATION PRACTICE

-------------------------------------------------------------------------------
'''

equationpracticemessage.draw()
win.flip()
event.waitKeys()

#show empty screen for a second (so that trials don't start immediately)
win.flip()
core.wait(1.0)

equation_rt_array = np.empty(nmathpractice);

ncorrect = 0
while ncorrect < nmathpractice:
    answer, eqtext = drawequation(equations)
    drawbuttons()

    equation_rt_starttime = core.getTime()
    win.flip()
    keys = event.waitKeys(keyList=['f', 'j'], timeStamped=True)
    if keys is not None:
        drawbuttons(keys[0][0])
        equationtext.text = eqtext
        equationtext.draw()
        win.flip()
        core.wait(0.4)
        if check_equation_answer(keys[0][0], answer) > 0:
            equation_rt_array[ncorrect] = keys[0][1] - equation_rt_starttime
            ncorrect += 1
            congratsmessage.draw()
            win.flip()
            core.wait(1.5)
        else:
            incorrectanswermessage.draw()
            win.flip()
            core.wait(1.5)

equation_rt_mean = np.mean(equation_rt_array)
equation_rt_sd   = np.std(equation_rt_array)
equationduration = equation_rt_mean + 2.5*equation_rt_sd


'''
-------------------------------------------------------------------------------

    FULL PRACTICE

-------------------------------------------------------------------------------
'''

fullpracticemessage.draw()
win.flip()
event.waitKeys()

ntrialscorrect = 0
for i in range(0, 3):
    #show empty screen for a second (so that trials don't start immediately)
    win.flip()
    core.wait(1.0)

    shuffle(characters)
    answer = '';

    for t in range(0, 2):

        eqanswer, eqtext = drawequation(equations)
        drawbuttons()

        equation_rt_starttime = core.getTime()
        win.flip()
        keys = event.waitKeys(maxWait=equationduration, keyList=['f', 'j'], timeStamped=True)

        if keys is not None:
            trialincorrect = 0
            drawbuttons(keys[0][0])
            equationtext.text = eqtext
            equationtext.draw()
            win.flip()
        else:
            trialincorrect = 1


        core.wait(1.0)

        lettertext.text = characters[t]
        answer = answer + ' ' + characters[t]
        lettertext.draw()
        win.flip()
        core.wait(0.8)

        win.flip()
        core.wait(1.0)

    response = getcharacterinput()
    if response == answer:
        ntrialscorrect = ntrialscorrect + 1

    ntrialscorrect = ntrialscorrect - trialincorrect

practicecompletemessage = visual.TextStim(win,
    text='You responded correctly to ' + str(ntrialscorrect) + ' out of 3 trials',
    units='pix',
    height = 0.05*monitor_height
)

practicecompletemessage.draw()
win.flip()
core.wait(2.0)

'''
-------------------------------------------------------------------------------

    FULL TASK

-------------------------------------------------------------------------------
'''

taskmessage.draw()
win.flip()
event.waitKeys()

#show empty screen for a second (so that trials don't start immediately)
win.flip()
core.wait(1.0)

#Create order of spans (with repmat) then shuffle them
spanorder = np.linspace(span_low, span_high, (span_high-span_low)+1)
shuffle(spanorder)

#Create matrices to store data
data = np.empty([len(spanorder)*nspaniterations, 8]) #[iteration, span, %mathaccuracy, nmathtimeout, correct, mathrt_mean, mathrt_sd, mathrt_max]

datarowindex = 0
# LOOP OVER SPAN LENGTHS
for span in range(0, len(spanorder)):
    # LOOP OVER ITERATIONS OF EACH SPAN
    ntrialscorrect = 0
    for iteration in range(0, nspaniterations):
        shuffle(characters)
        charanswer = '';

        # Store some data about the trials
        data[datarowindex, 0] = iteration + 1
        data[datarowindex, 1] = spanorder[span]

        # Initialize arrays & values for trial level data (to then be summarized)
        mathcorrect = np.empty(int(spanorder[span]))
        mathrt = np.empty(int(spanorder[span]))
        nmathtimeout = 0

        #LOOP OVER EQUATIONS/LETTERS
        for t in range(0, int(spanorder[span])):

            eqanswer, eqtext = drawequation(equations)
            drawbuttons()

            win.flip()
            mathrt_start = core.getTime()
            keys = event.waitKeys(maxWait=equationduration, keyList=['f', 'j'], timeStamped=True)

            if keys is not None:
                mathrt[t] = keys[0][1] - mathrt_start
                mathcorrect[t] = check_equation_answer(keys[0][0], eqanswer)
                drawbuttons(keys[0][0])
                equationtext.text = eqtext
                equationtext.draw()
                win.flip()
            else:
                mathcorrect[t] = 0
                nmathtimeout = nmathtimeout + 1

            core.wait(1.0)

            lettertext.text = characters[t]
            charanswer = charanswer + ' ' + characters[t]
            lettertext.draw()
            win.flip()
            core.wait(0.8)

            win.flip()
            core.wait(1.0)

        response = getcharacterinput()
        if response == charanswer:
            trialcorrect = 1
        else:
            trialcorrect = 0

        ntrialscorrect = ntrialscorrect + trialcorrect #update for feedback

        # STORE SOME DATA ABOUT THE TRIAL
        data[datarowindex, 2] = np.mean(mathcorrect)#%mathaccuracy,
        data[datarowindex, 3] = nmathtimeout #nmathtimeout,
        data[datarowindex, 4] = trialcorrect #correct,
        data[datarowindex, 5] = np.mean(mathrt) #mathrt_mean,
        data[datarowindex, 6] = np.std(mathrt) #mathrt_sd
        data[datarowindex, 7] = np.max(mathrt)#mathrt_max

        #Increment the index of data storage by 1
        datarowindex = datarowindex + 1

    trialcompletemessage = visual.TextStim(win,
        text='You responded correctly to ' + str(ntrialscorrect) + ' out of ' + str(nspaniterations) + ' trials',
        units='pix',
        height = 0.05*monitor_height
    )

    trialcompletemessage.draw()
    win.flip()
    core.wait(2.0)

'''
================================================================================

    CONVERT AND STORE DATA

================================================================================
'''

# Create data frame
df = pd.DataFrame({ #[subject_id, iteration, span, %mathaccuracy, nmathtimeout, correct, mathrt_mean, mathrt_sd, mathrt_max]
    'subject_id'     : subject_id,
    'iteration'      : data[:,0],
    'span'           : data[:,1],
    'math_accuracy'  : data[:,2],
    'n_math_timeout' : data[:,3],
    'correct_raw'    : data[:,4], # not corrected for math timeouts
    'mathrt_mean'    : data[:,5],
    'mathrt_sd'      : data[:,6],
    'mathrt_max'     : data[:,7]
})

# Write to csv
df.to_csv('opspandata' + subject_id +'.csv', sep='\t', encoding='utf-8')

'''
================================================================================

    CONCLUSION MESSAGE

================================================================================
'''

completemessage.draw()
win.flip()
core.wait(5.0)

win.close()
core.quit()
