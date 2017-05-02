import numpy as np
from psychopy import visual

def drawatpos(stim, xpos, ypos):
    stim.pos = (xpos, ypos)
    stim.draw()

def animatechoice(win, stim, endpos_x, endpos_y, animate_duration=0.4):
    endpos = [endpos_x, endpos_y]
    startpos = stim.pos
    nframes = int(np.floor(animate_duration/win.monitorFramePeriod))
    ddist = (endpos - startpos)/nframes
    for frame in range(nframes):
        stim.pos = stim.pos + ddist
        stim.draw()
        win.flip()
