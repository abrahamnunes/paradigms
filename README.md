# Paradigms

A Python package built atop PsychoPy that facilitates efficient development and running of behavioural experiments.

## Installing Paradigms

In your terminal or console, enter

``` bash

pip install git+https://github.com/ComputationalPsychiatry/paradigms.git

```

## Using Paradigms

### Structure of a Behavioural Experiment

The core structure of a behavioural experiment is as follows:

+ `Experiment`
    + `Paradigm`
        + `Block`
            + `Trial`

This hierarchical structure makes development relatively straightforward.

First, one defines the procedures inherent in a single `Trial`, then composes these trials into a `Block`. Blocks of trials are then composed into a behavioural `Paradigm`. Finally, if one is implementing a battery of tasks, an `Experiment` may be defined (even if it only contains one `Paradigm`).

### Defining a Trial

The `Trial` class offers a framework within which to define a specific trial for your own experiment. To create a trial for your specific behavioural paradigm, you must write a class that inherits the base `Trial` object. Within your trial object, you must create a function called `procedure()` in which the operations to carry out the trial are represented, and one called `ITI()` in which the procedure of the intertrial interval is specified.

You can also add additional functions within this subclass that are called in the `procedure()` function. So long as `procedure()` and `ITI()` are defined, the rest is up to you.

``` python

class MyTrial(Trial):
    def procedure(self):
        pass

    def ITI(self):
        pass

```

### Composing Trials into a Block

Blocks are more abstract than trials of an experiment, and so one does not need to define a subclass, as above in the `Trial` example. Rather, one simply instantiates a block with the trials desired:

``` python

my_block = Block(trials=[MyTrial()],
                 n_trials=100,
                 strict_count=False,
                 trial_order='random',
                 label='My Block')

```

### Composing Blocks into a Paradigm

This step follows in much the same fashion as composition of a `Block`, except that instead of putting together trials, one is putting together blocks.

``` python

my_paradigm = Paradigm(blocks=[my_block], label='My Paradigm')

```

### Defining an Experiment

While at face value, the `Experiment` object may seem redundant, it is an important space within which do define the "hyperparameters" which include equipment specifications, subject identification, etc.

``` python

my_experiment = Experiment(paradigms=[my_paradigm])

```

## The Behavioural Data Format (BDF)

We have created a general structure for representing the results of behavioural experiments, and implemented it in a fashion that facilitates easy output into various formats (i.e. Pandas DataFrame objects, CSV), and especially facilitates interoperability with our model fitting package, [`Fitr`](https://github.com/ComputationalPsychiatry/fitr).

Data stored in BDF can also be rendered in a text file that is easy to read (trial by trial) and includes valuable data in a header section.

Moreover, BDF offers useful functions for screening behavioural data for anomalies, so that bad data can be screened out prior to the analysis phase of your project.
