from psychopy import visual as vis

def loadstimuli(win, stim_set, stim_size):
    """
    Loads stimuli for the task

    Parameters
    ----------
    win : a PsychoPy Window object
    stim_set : {'tutorial', 'task', 'reward', 'plots'}
    stim_size: float
        Size of the stimulus (all are square)

    Returns
    -------
    dict
        Dictionary of stimuli for the task

    Notes
    -----
    Tutorial stim are organized in pairs, with the exception of Stim9
        - Pair 0: Stim 1 & 2
        - Pair 1: Stim 3 & 4
        - Pair 2: Stim 5 & 6
        - Pair 3: Stim 7 & 8
        - Stim 9 is alone and indexed as tutorialstim[4]

    """
    tutorialstim = {
        0: {
            0: {
                'norm': vis.ImageStim(win, image='tutorial/Stim1.PNG', units='pix', size=stim_size),
                'act': vis.ImageStim(win, image='tutorial/Stim1-a.PNG', units='pix', size=stim_size),
                'deact': vis.ImageStim(win, image='tutorial/Stim1-d.PNG', units='pix', size=stim_size),
                'spoiled': vis.ImageStim(win, image='tutorial/Stim1-s.PNG', units='pix', size=stim_size)
            },
            1: {
                'norm': vis.ImageStim(win, image='tutorial/Stim2.PNG', units='pix', size=stim_size),
                'act': vis.ImageStim(win, image='tutorial/Stim2-a.PNG', units='pix', size=stim_size),
                'deact': vis.ImageStim(win, image='tutorial/Stim2-d.PNG', units='pix', size=stim_size),
                'spoiled': vis.ImageStim(win, image='tutorial/Stim2-s.PNG', units='pix', size=stim_size)
            }
        },
        1: {
            0: {
                'norm': vis.ImageStim(win, image='tutorial/Stim3.PNG', units='pix', size=stim_size),
                'act': vis.ImageStim(win, image='tutorial/Stim3-a.PNG', units='pix', size=stim_size),
                'deact': vis.ImageStim(win, image='tutorial/Stim3-d.PNG', units='pix', size=stim_size),
                'spoiled': vis.ImageStim(win, image='tutorial/Stim3-s.PNG', units='pix', size=stim_size)
            },
            1: {
                'norm': vis.ImageStim(win, image='tutorial/Stim4.PNG', units='pix', size=stim_size),
                'act': vis.ImageStim(win, image='tutorial/Stim4-a.PNG', units='pix', size=stim_size),
                'deact': vis.ImageStim(win, image='tutorial/Stim4-d.PNG', units='pix', size=stim_size),
                'spoiled': vis.ImageStim(win, image='tutorial/Stim4-s.PNG', units='pix', size=stim_size)
            }
        },
        2 : {
            0: {
                'norm': vis.ImageStim(win, image='tutorial/Stim5.PNG', units='pix', size=stim_size),
                'act': vis.ImageStim(win, image='tutorial/Stim5-a.PNG', units='pix', size=stim_size),
                'deact': vis.ImageStim(win, image='tutorial/Stim5-d.PNG', units='pix', size=stim_size),
                'spoiled': vis.ImageStim(win, image='tutorial/Stim5-s.PNG', units='pix', size=stim_size)
            },
            1: {
                'norm': vis.ImageStim(win, image='tutorial/Stim6.PNG', units='pix', size=stim_size),
                'act': vis.ImageStim(win, image='tutorial/Stim6-a.PNG', units='pix', size=stim_size),
                'deact': vis.ImageStim(win, image='tutorial/Stim6-d.PNG', units='pix', size=stim_size),
                'spoiled': vis.ImageStim(win, image='tutorial/Stim6-s.PNG', units='pix', size=stim_size)
            }
        },
        3 : {
            0: {
                'norm': vis.ImageStim(win, image='tutorial/Stim7.PNG', units='pix', size=stim_size),
                'act': vis.ImageStim(win, image='tutorial/Stim7-a.PNG', units='pix', size=stim_size),
                'deact': vis.ImageStim(win, image='tutorial/Stim7-d.PNG', units='pix', size=stim_size),
                'spoiled': vis.ImageStim(win, image='tutorial/Stim7-s.PNG', units='pix', size=stim_size)
            },
            1: {
                'norm': vis.ImageStim(win, image='tutorial/Stim8.PNG', units='pix', size=stim_size),
                'act': vis.ImageStim(win, image='tutorial/Stim8-a.PNG', units='pix', size=stim_size),
                'deact': vis.ImageStim(win, image='tutorial/Stim8-d.PNG', units='pix', size=stim_size),
                'spoiled': vis.ImageStim(win, image='tutorial/Stim8-s.PNG', units='pix', size=stim_size)
            }
        },
        4: {
            'norm': vis.ImageStim(win, image='tutorial/Stim9.PNG', units='pix', size=stim_size),
            'act': vis.ImageStim(win, image='tutorial/Stim9-a.PNG', units='pix', size=stim_size),
            'deact': vis.ImageStim(win, image='tutorial/Stim9-d.PNG', units='pix', size=stim_size),
            'spoiled': vis.ImageStim(win, image='tutorial/Stim9-s.PNG', units='pix', size=stim_size)
        }
    }

    taskstim = {
        0: {
            'norm': vis.ImageStim(win, image='behavioural/Stim1.PNG', units='pix', size=stim_size),
            'act': vis.ImageStim(win, image='behavioural/Stim1-a.PNG', units='pix', size=stim_size),
            'deact': vis.ImageStim(win, image='behavioural/Stim1-d.PNG', units='pix', size=stim_size),
            'spoiled': vis.ImageStim(win, image='behavioural/Stim1-s.PNG', units='pix', size=stim_size)
        },
        1: {
            'norm': vis.ImageStim(win, image='behavioural/Stim2.PNG', units='pix', size=stim_size),
            'act': vis.ImageStim(win, image='behavioural/Stim2-a.PNG', units='pix', size=stim_size),
            'deact': vis.ImageStim(win, image='behavioural/Stim2-d.PNG', units='pix', size=stim_size),
            'spoiled': vis.ImageStim(win, image='behavioural/Stim2-s.PNG', units='pix', size=stim_size)
        },
        2: {
            'norm': vis.ImageStim(win, image='behavioural/Stim3.PNG', units='pix', size=stim_size),
            'act': vis.ImageStim(win, image='behavioural/Stim3-a.PNG', units='pix', size=stim_size),
            'deact': vis.ImageStim(win, image='behavioural/Stim3-d.PNG', units='pix', size=stim_size),
            'spoiled': vis.ImageStim(win, image='behavioural/Stim3-s.PNG', units='pix', size=stim_size)
        },
        3: {
            'norm': vis.ImageStim(win, image='behavioural/Stim4.PNG', units='pix', size=stim_size),
            'act': vis.ImageStim(win, image='behavioural/Stim4-a.PNG', units='pix', size=stim_size),
            'deact': vis.ImageStim(win, image='behavioural/Stim4-d.PNG', units='pix', size=stim_size),
            'spoiled': vis.ImageStim(win, image='behavioural/Stim4-s.PNG', units='pix', size=stim_size)
        },
        4: {
            'norm': vis.ImageStim(win, image='behavioural/Stim5.PNG', units='pix', size=stim_size),
            'act': vis.ImageStim(win, image='behavioural/Stim5-a.PNG', units='pix', size=stim_size),
            'deact': vis.ImageStim(win, image='behavioural/Stim5-d.PNG', units='pix', size=stim_size),
            'spoiled': vis.ImageStim(win, image='behavioural/Stim5-s.PNG', units='pix', size=stim_size)
        },
        5: {
            'norm': vis.ImageStim(win, image='behavioural/Stim6.PNG', units='pix', size=stim_size),
            'act': vis.ImageStim(win, image='behavioural/Stim6-a.PNG', units='pix', size=stim_size),
            'deact': vis.ImageStim(win, image='behavioural/Stim6-d.PNG', units='pix', size=stim_size),
            'spoiled': vis.ImageStim(win, image='behavioural/Stim6-s.PNG', units='pix', size=stim_size)
        }
    }

    rewardstim = {
        0 : vis.ImageStim(win, image='tutorial/noreward.png', units='pix', size=stim_size),
        1 : vis.ImageStim(win, image='tutorial/reward.png', units='pix', size=stim_size)
    }

    plots = {
        's1t1': vis.ImageStim(win, image='tutorial/chances_1stim_trial1.png', units='pix', size=stim_size),
        's1t6' : vis.ImageStim(win, image='tutorial/chances_1stim_trial6.png', units='pix', size=stim_size),
        's1t60' : vis.ImageStim(win, image='tutorial/chances_1stim_trial60.png', units='pix', size=stim_size),
        's1t60r' : vis.ImageStim(win, image='tutorial/chances_1stim_trial60_rewards.png', units='pix', size=stim_size),
        's1tw' : vis.ImageStim(win, image='tutorial/chances_1stim_whole.png', units='pix', size=stim_size),
        's1twr' : vis.ImageStim(win, image='tutorial/chances_1stim_whole_rewards.png', units='pix', size=stim_size),
        's2tw' : vis.ImageStim(win, image='tutorial/chances_2stim_whole.png', units='pix', size=stim_size)
    }

    if stim_set == 'tutorial':
        stimuli = tutorialstim
    elif stim_set == 'task':
        stimuli = taskstim
    elif stim_set == 'reward':
        stimuli = rewardstim
    elif stim_set == 'plots':
        stimuli = plots

    return stimuli
