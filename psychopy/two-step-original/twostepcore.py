from psychopy import core, event, gui
from psychopy import visual as vis
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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

class Trials(object):
    """
    Stimuli that are activated for the task

    Attributes
    ----------
    subject_id : str
        Subject identifier
    win : psychopy window object
    state_a_stim : dict
        Pair of stimuli for the first step
    state_b_stim : dict
        One pair of stimuli for the second step
    state_c_stim : dict
        The other pair of stimuli for the second step
    reward_stim : dict
        Reward and non-reward stimuli
    ntrials : int > 0
        Number of trials to create
    block : int > 0
        Which block of trials this will be (for naming output files)
    boxpos : dict
        Dictionary specifying box positions
    tutorial : bool
        Whether this is for tutorial (sets reward probabilities the same for all subjects).
    ptrans : float on interval [0, 1]
        The major transition probability. Minor transition probability will be 1-ptrans
    preward_low : float on interval [0, 1]
        Lower bound on reward probability
    preward_high : float on interval [0, 1]
        Upper bound on reward probability
    preward_sd : float
        Standard deviation of Gaussian random walk
    tlimitchoice : float > 0
        Time limit for choices (in seconds)
    t_transition : float > 0
        Duration of transitions
    ititime : float > 0
        Average duration (seconds) of intertrial interval (mean of exp distrib)

    """
    def __init__(self, subject_id, win, state_a_stim, state_b_stim, state_c_stim, reward_stim, ntrials, block, boxpos, tutorial=False, ptrans=0.7, preward_low=0.25, preward_high=0.75, preward_sd=0.025, tlimitchoice=3, t_transition=0.4, ititime=1):
        self.subject_id = subject_id
        self.block = block
        self.win = win
        self.states = {
            0 : {
                'id' : 0,
                0 : {
                    'id' : 0,
                    'stim': state_a_stim[0],
                    'ptrans': [ptrans, 1-ptrans]
                },
                1 : {
                    'id' : 1,
                    'stim': state_a_stim[1],
                    'ptrans': [1-ptrans, ptrans]
                }
            },
            1 : {
                'id' : 1,
                0 : {
                    'id' : 0,
                    'stim': state_b_stim[0],
                    'preward' : []
                },
                1 : {
                    'id' : 1,
                    'stim': state_b_stim[1],
                    'preward' : []
                }
            },
            2 : {
                'id' : 2,
                0 : {
                    'id' : 0,
                    'stim': state_c_stim[0],
                    'preward' : []
                },
                1 : {
                    'id' : 1,
                    'stim': state_c_stim[1],
                    'preward' : []
                }
            }
        }
        self.reward_stim = reward_stim
        self.boxpos = boxpos

        self.preward_low = preward_low
        self.preward_high = preward_high
        self.preward_sd = preward_sd
        self.ntrials = ntrials
        self.tutorial = tutorial
        self.tlimitchoice = tlimitchoice
        self.t_transition = t_transition
        self.ititime = ititime

        self._initrewardpaths()

        # Set counters and data arrays
        self.t = 0 # current trial
        self.step1_lrsequence = []
        self.step2_lrsequence = []

        self.trial_aborted = False # whether last trial was aborted
        self.curr_stim = {} # current stimuli (left and right)
        self.a1 = 999 # Placeholder for the choice at step 1
        self.a2 = 999 # Placeholder for the choice at step 2
        self.s2 = 999 # Placeholder for the state at step 2

        self.data = {
            'trial'    : [], # Trial index
            'aborted'  : [],
            'a1'       : [], # First step choice
            'a1_key'   : [], # Keypress at first step
            'rt1'      : [], # Reaction time at step 1
            's2'       : [], # Second step state
            'a2'       : [], # Second step choice
            'a2_key'   : [], # Keypress at second step
            'rt2'      : [], # Reaction time at step 2
            'r'        : [], # Trial rewarded (1) or not (0)
            'trans_cr' : []  # Common (1) or rare (0) transition
        }

    def _initrewardpaths(self):

        if self.tutorial is True:
            np.random.seed(seed=12345)

        for i in [1, 2]:
            for j in [0, 1]:
                self.states[i][j]['preward'].append(np.random.uniform(self.preward_low, self.preward_high))

                for t in range(self.ntrials-1):
                    self.states[i][j]['preward'].append(np.maximum(np.minimum(self.states[i][j]['preward'][-1] + self.preward_sd*np.random.normal(0, 1), self.preward_high), self.preward_low))

    def _updaterewardpaths(self):

            for i in [1, 2]:
                for j in [0, 1]:
                    self.states[i][j]['preward'].append(np.maximum(np.minimum(self.states[i][j]['preward'][-1] + self.preward_sd*np.random.normal(0, 1), self.preward_high), self.preward_low))

    def step1(self):
        # Randomize stimuli to L/R
        self.step1_lrsequence.append(np.random.multinomial(1,
                                                           pvals=[0.5, 0.5]))

        self.curr_stim = {
            'selected' : None,
            'f' : self.states[0][self.step1_lrsequence[self.t][0]],
            'j' : self.states[0][self.step1_lrsequence[self.t][1]]
        }

        drawatpos(stim=self.curr_stim['f']['stim']['norm'],
                  xpos=self.boxpos['x']['left'],
                  ypos=self.boxpos['y']['neutral'])
        drawatpos(stim=self.curr_stim['j']['stim']['norm'],
                  xpos=self.boxpos['x']['right'],
                  ypos=self.boxpos['y']['neutral'])
        self.win.flip()

        # Collect the response
        starttime = core.getTime()
        keys=event.waitKeys(maxWait=self.tlimitchoice, keyList=['f','j'], timeStamped=True)
        if keys is None:
            self.abort_trial(step=1)
        else:
            self.trial_aborted = False

            step1_key = keys[0][0]
            self.a1 = self.curr_stim[step1_key]['id']
            step1_rt = keys[0][1] - starttime

            # Store data
            self.data['a1'].append(self.a1)
            self.data['a1_key'].append(step1_key)
            self.data['rt1'].append(step1_rt)

            # Highlight selected choice
            self.curr_stim['selected'] = self.curr_stim[step1_key]
            drawatpos(stim=self.curr_stim['selected']['stim']['act'],
                      xpos=self.curr_stim['selected']['stim']['norm'].pos[0],
                      ypos=self.curr_stim['selected']['stim']['norm'].pos[1])
            self.win.flip()
            core.wait(0.2)

    def step2(self):
        # Randomize stimuli to L/R
        self.step2_lrsequence.append(np.random.multinomial(1,
                                                           pvals=[0.5, 0.5]))

        # Assign stimuli to L and R sides
        self.curr_stim['f'] = self.states[self.s2][self.step2_lrsequence[self.t][0]]

        self.curr_stim['j'] = self.states[self.s2][self.step2_lrsequence[self.t][1]]

        drawatpos(stim=self.curr_stim['selected']['stim']['deact'],
                  xpos=self.boxpos['x']['neutral'],
                  ypos=self.boxpos['y']['high'])
        drawatpos(stim=self.curr_stim['f']['stim']['norm'],
                  xpos=self.boxpos['x']['left'],
                  ypos=self.boxpos['y']['neutral'])
        drawatpos(stim=self.curr_stim['j']['stim']['norm'],
                  xpos=self.boxpos['x']['right'],
                  ypos=self.boxpos['y']['neutral'])
        self.win.flip()

        # Collect the response
        starttime = core.getTime()
        keys=event.waitKeys(maxWait=self.tlimitchoice, keyList=['f','j'], timeStamped=True)
        if keys is None:
            self.abort_trial(step=2)
        else:
            self.trial_aborted = False

            step2_key = keys[0][0]
            self.a2 = self.curr_stim[step2_key]['id']
            step2_rt = keys[0][1] - starttime

            # Store data
            self.data['a2'].append(self.a2)
            self.data['a2_key'].append(step2_key)
            self.data['rt2'].append(step2_rt)

            # Highlight selected choice
            self.curr_stim['selected'] = self.curr_stim[step2_key]
            drawatpos(stim=self.curr_stim['selected']['stim']['act'],
                      xpos=self.curr_stim['selected']['stim']['norm'].pos[0],
                      ypos=self.curr_stim['selected']['stim']['norm'].pos[1])
            self.win.flip()
            core.wait(0.2)

    def state_transition(self):
        """ Generates state 2 step and animates present choice """

        # Generate transition
        p_trans = self.states[0][self.a1]['ptrans']
        self.s2 = int(np.argmax(np.random.multinomial(1, pvals=p_trans)) + 1)
        self.data['s2'].append(self.s2)

        # Determine whether it is a common or rare transition
        if int(self.s2-1) == np.argmax(p_trans):
            self.data['trans_cr'].append(1)
        else:
            self.data['trans_cr'].append(0)

        # Animate choice
        animatechoice(win=self.win,
                      stim=self.curr_stim['selected']['stim']['act'],
                      endpos_x=self.boxpos['x']['neutral'],
                      endpos_y=self.boxpos['y']['high'],
                      animate_duration=self.t_transition)

        drawatpos(stim=self.curr_stim['selected']['stim']['deact'],
                  xpos=self.boxpos['x']['neutral'],
                  ypos=self.boxpos['y']['high'])
        self.win.flip()
        core.wait(0.2)

    def sample_reward(self):
        """ Returns reward and performs animation """

        p_reward = self.states[self.s2][self.a2]['preward'][self.t]
        rewarded = np.random.binomial(1, p=p_reward)
        self.data['r'].append(rewarded)

        # Animate choice
        animatechoice(win=self.win,
                      stim=self.curr_stim['selected']['stim']['act'],
                      endpos_x=self.boxpos['x']['neutral'],
                      endpos_y=self.boxpos['y']['high'],
                      animate_duration=self.t_transition)

        drawatpos(stim=self.curr_stim['selected']['stim']['deact'],
                  xpos=self.boxpos['x']['neutral'],
                  ypos=self.boxpos['y']['high'])
        self.win.flip()
        core.wait(0.2)

        drawatpos(stim=self.curr_stim['selected']['stim']['deact'],
                  xpos=self.boxpos['x']['neutral'],
                  ypos=self.boxpos['y']['high'])

        drawatpos(stim=self.reward_stim[rewarded],
                  xpos=self.boxpos['x']['neutral'],
                  ypos=self.boxpos['y']['low'])
        self.win.flip()
        core.wait(2.0)


    def abort_trial(self, step):
        self.trial_aborted = True
        self.data['aborted'][self.t] = 1
        self.t += 1
        self.ntrials += 1
        self._updaterewardpaths()

        if step == 1:
            # If we abort on first trial, maintain size of step2 sequence
            self.step2_lrsequence.append(np.array([-1, -1]))

            # Store data
            self.data['a1'].append(-1)
            self.data['a1_key'].append('ABORTED')
            self.data['rt1'].append(np.nan)
            self.data['s2'].append(-1)
            self.data['trans_cr'].append('ABORTED')
            self.data['a2'].append(-1)
            self.data['a2_key'].append('ABORTED')
            self.data['rt2'].append(np.nan)
            self.data['r'].append(np.nan)
        elif step == 2:
            self.data['a2'].append(-1)
            self.data['a2_key'].append('NA')
            self.data['rt2'].append(np.nan)
            self.data['r'].append(np.nan)

        drawatpos(stim=self.curr_stim['f']['stim']['spoiled'],
                  xpos=self.boxpos['x']['left'],
                  ypos=self.boxpos['y']['neutral'])
        drawatpos(stim=self.curr_stim['j']['stim']['spoiled'],
                  xpos=self.boxpos['x']['right'],
                  ypos=self.boxpos['y']['neutral'])
        self.win.flip()
        core.wait(2.0)

    def iti(self):
        """ Intertrial interval """
        self.win.flip()
        core.wait(np.random.exponential(self.ititime))

    def run(self):
        """ Runs iterations of the steps in trials """

        # Run experiment
        while self.t < self.ntrials:
            self.data['trial'].append(self.t)
            self.data['aborted'].append(0)
            self.iti()
            self.step1()

            if self.trial_aborted is False:
                self.state_transition()
                self.step2()

            if self.trial_aborted is False:
                self.sample_reward()
                self.t += 1

    def savedata(self):

        # Save data
        self.data['subject_id'] = [self.subject_id]*len(self.data['trial'])
        self.data['rprob_10'] = self.states[1][0]['preward']
        self.data['rprob_11'] = self.states[1][1]['preward']
        self.data['rprob_20'] = self.states[2][0]['preward']
        self.data['rprob_21'] = self.states[2][1]['preward']

        df = pd.DataFrame.from_dict(self.data)

        # Now process data into theory-free analysis form
        df_inc = df.ix[df.aborted == 0, :]
        last_a = df_inc.a1[:-1]
        curr_a = df_inc.a1[1:]
        tf_df = pd.DataFrame(data = {
            'subject_id'    : df_inc.subject_id[:-1].values,
            'stay'          : np.equal(last_a, curr_a).astype(int),
            'last_trans'    : df_inc.trans_cr[:-1].values,
            'last_rewarded' : df_inc.r[:-1].values,
            'rt2'           : df_inc.rt2[1:].values
            }, index=None)

        if self.tutorial is True:
            df.to_csv('twostep-raw-tut-' + self.subject_id + '-block-' + str(self.block) + '.csv',
                      index=False)
            tf_df.to_csv('twostep-tf-tut-' + self.subject_id + '-block-' + str(self.block) + '.csv',
                         index=False)
        else:
            df.to_csv('twostep-raw-'   + self.subject_id + '-block-' + str(self.block) + '.csv', index=False)
            tf_df.to_csv('twostep-tf-' + self.subject_id + '-block-' + str(self.block) + '.csv', index=False)

    def plotrewardpaths(self):
        fig, ax = plt.subplots()
        for i in [1, 2]:
            for j in [0, 1]:
                ax.plot(np.arange(self.ntrials), self.states[i][j]['preward'], label='Option (' + str(i) + ', ' + str(j) + ')')
        ax.set_title('Step 2 Reward Probabilities, Subject ' + self.subject_id)
        ax.set_ylabel('Reward Probability')
        ax.set_xlabel('Trial')
        plt.legend()
        plt.savefig('rewardpaths.png')


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
        0 : {
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
            }
        },
        1 : {
            0: {
                'norm': vis.ImageStim(win, image='behavioural/Stim3.PNG', units='pix', size=stim_size),
                'act': vis.ImageStim(win, image='behavioural/Stim3-a.PNG', units='pix', size=stim_size),
                'deact': vis.ImageStim(win, image='behavioural/Stim3-d.PNG', units='pix', size=stim_size),
                'spoiled': vis.ImageStim(win, image='behavioural/Stim3-s.PNG', units='pix', size=stim_size)
            },
            1: {
                'norm': vis.ImageStim(win, image='behavioural/Stim4.PNG', units='pix', size=stim_size),
                'act': vis.ImageStim(win, image='behavioural/Stim4-a.PNG', units='pix', size=stim_size),
                'deact': vis.ImageStim(win, image='behavioural/Stim4-d.PNG', units='pix', size=stim_size),
                'spoiled': vis.ImageStim(win, image='behavioural/Stim4-s.PNG', units='pix', size=stim_size)
            }
        },
        2 : {
            0: {
                'norm': vis.ImageStim(win, image='behavioural/Stim5.PNG', units='pix', size=stim_size),
                'act': vis.ImageStim(win, image='behavioural/Stim5-a.PNG', units='pix', size=stim_size),
                'deact': vis.ImageStim(win, image='behavioural/Stim5-d.PNG', units='pix', size=stim_size),
                'spoiled': vis.ImageStim(win, image='behavioural/Stim5-s.PNG', units='pix', size=stim_size)
            },
            1: {
                'norm': vis.ImageStim(win, image='behavioural/Stim6.PNG', units='pix', size=stim_size),
                'act': vis.ImageStim(win, image='behavioural/Stim6-a.PNG', units='pix', size=stim_size),
                'deact': vis.ImageStim(win, image='behavioural/Stim6-d.PNG', units='pix', size=stim_size),
                'spoiled': vis.ImageStim(win, image='behavioural/Stim6-s.PNG', units='pix', size=stim_size)
            }
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
