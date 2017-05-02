import pandas as pd

class ParadigmData(object):
    """
    Object representing behavioural data for a paradigm
    """
    def __init__(self):
        pass

class SubjectData(object):
    """
    Object representing behavioural data for a subject

    Attributes
    ----------
    subject_id : str
        Identification of the subject
    covariates : pandas.DataFrame
        Subject level covariates

    Methods
    -------
    convert(self, format)
        Converts behavioural data object to different formats

    """
    def __init__(self, subject_id, covariates):
        self.subject_id = subject_id
        self.blocks = []
        pass

    def append_block(self, newblock):
        """
        Adds a block of data to the paradigm
        """

        self.blocks.append(newblock)



class BlockData(BehaviouralData):
    """
    Object representing data from a block of trials

    Attributes
    ----------
    block_id : str
        Block identifier
    """
    def __init__(self, block_id='anon_block'):
        self.block_id = block_id
        self.trials = []
        pass

    def append_trial(self, newtrial):
        """
        Appends data from a trial to the block

        Parameters
        ----------
        newtrial : TrialData
            Data from a trial to be added to the list

        """

        self.trials.append(newtrial)


class TrialData(BehaviouralData):
    """
    Object representing data from a single trial

    Attributes
    ----------
    trial_id : str
        Trial identifier
    """
    def __init__(self, trial_id='anon_trial'):
        self.trial_id = trial_id
        pass
