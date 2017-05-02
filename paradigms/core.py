from .BDF import *

class Experiment(object):
    """
    Core object defining an experiment

    Attributes
    ----------
    paradigms : OrderedDict
        Ordered dictionary of paradigms included
    label : str
        The experiment label

    Methods
    -------
    run(self)
        Runs the experiment
    """
    def __init__(self, label='anon_experiment'):
        self.label = label

class Paradigm(object):
    """
    Core object defining an experimental paradigm

    Attributes
    ----------
    blocks : list
        List of block objects
    label : str
        Experiment label

    Methods
    -------
    run(self)
        Runs the experiment
    """
    def __init__(self, blocks=None, label='anon_paradigm'):
        self.label = label
        self.blocks = blocks

    def run(self):
        pass


class Block(object):
    """
    Core object defining a block of trials

    Attributes
    ----------
    trials : OrderedDict
        Ordered dictionary of Trial objects
    n_trials : int > 0
        Number of trials in the block
    strict_count : bool
    trial_order : {'ordered', 'random', 'interleaved', [TODO] fill this in}
        How trials are to be presented. If 'ordered', then the order in which trials are listed in the `trials` attribute will be maintained. If `random`, then each trial will be sampled at random.
    label : str
        Label for the block

    Methods
    -------
    run(self)
        Runs the block of trials
    getsequence(self)
        Generates a trial sequence
    """
    def __init__(self, trials, iti, n_trials, strict_count=False, trial_order='ordered', label='anon_block'):

        self.trials = trials
        self.n_trials = n_trials
        self.strict_count = strict_count
        self.trial_order = trial_order
        self.label = label

    def run(self):
        """
        Runs the block of trials

        Returns
        -------
        BlockData

        """
        pass

    def getsequence(self):
        """ Generates a trial sequence """
        pass

class Trial(object):
    """
    Core object defining a trial

    Attributes
    ---------
    time_limit : float > 0
        The maximum amount of time allowed for a trial
    label : str
        Label of the trial

    Methods
    -------
    run(self)
        Runs the trial
    """
    def __init__(self, time_limit, label='anon_trial'):
        self.time_limit = time_limit
        self.label = label

    def run(self):
        """
        Runs the trial

        Returns
        -------
        TrialData
        """
        trial_data = TrialData()

        return trial_data
