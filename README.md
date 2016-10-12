# Paradigms

This repository collects code for various experimental paradigms.

Currently, I am building only in PsychoPy, but in the future I will likely include Psychtoolbox.

Each task is self-contained into its own directory along with necessary resource files. To run a paradigm, simply load it into the "Coder View" in PsychoPy, then click the "Run" button.

If you need to adjust screen resolution settings, you can do so in the paradigm's main file (at the topmost section of the code).

## Contents
- [OPSPAN](#opspan)
- [Two-Step Task](#two-step)

## Current Paradigms

### <a name="opspan"></a> Operation Span (OPSPAN)

This is a working memory task as described in:

- Unsworth, N. et al. (2005) An automated version of the operation span task. Behav. Res. Methods 37, 498–505

Credit is owed to [Titus von der Malsburg](https://github.com/tmalsburg) for the equations and consonants file, which I took from his OPSPAN implementation [`py-span-task`](https://github.com/tmalsburg/py-span-task). Titus' package is great, and includes an R script to calculate performance.

The PsychoPy implementation I have included attempts to retain as much fidelity as possible to the implementation in Unsworth et al. (2005). Some notable exceptions include:

- Equations were all presented on one line, as in Titus von der Malsburg's version
- Subjects type in the letters they had to memorize, rather than selecting from those placed on a grid
- There is no feedback for number of equations correctly solved. The authors of that paper provided a visual indicator of percentage complete. I omitted this to minimize the number of elements displayed on the screen.

#### Output

The OPSPAN output will be a `.csv` file including the subject ID, which is collected at the outset through a GUI. The column headings are as follows:

| Column Head       | Description   |
| -----------       | ------------  |
| `subject_id`      | The subject's unique id |
| `iteration`       | Each span length is presented for (_n_ iterations). Default is 3 iterations for 5 spans (3-7 characters).
| `span`            | The number of characters in the current trial. As per Unsworth et al. (2005), the default is 3 to 7 |
| `correct`         | Binary. Whether the characters were correctly recalled at the end of a trial. |
| `math_accuracy`   | The percentage of correct answers to equation portions |
| `n_math_timeout`  | Number of equations in which there was a timeout. For the absolute scoring system in Unsworth et al. (2005), if the user times out on an equation during a span trial, the trials should not be counted as correct. |
| `mathrt_mean`     | Mean reaction time for math problems |
| `mathrt_sd`       | Standard deviation of reaction time for math problems |
| `mathrt_max`      | Maximum reaction time during math problems for that given span trial. |

### <a name="two-step"></a> Two-Step task

This is an implementation of the two-step task from the following paper:

- Daw, N.D. et al. (2011) Model-based influences on humans’ choices and striatal prediction errors. Neuron 69, 1204–1215

My implementation does not yet have a training phase, which I am working on adding at the moment.

The default parameters for the task can be set at the top of the twostep.py file.

#### Output

This task produces a `.csv` file with the following column headings

| Column Head   | Description   |
| -----------   | ------------  |
| 'subject_id'  | Subject ID, collected from initial GUI |
| 'step2state'  | The second step state. (First step states are always the same, so they are not listed) |
| 'choice1'     | First step choice |
| 'choice2'     | Second step choice |
| 'reward'      | Reward received at trial |
| 'rt_step1'    | Step 1 choice reaction time |
| 'rt_step2'    | Step 2 choice reaction time |
| 'key_step1'   | Key pressed at step 1 choice. Since the stimuli are randomly alternated between the left and right sides, these keys are recorded in order to determine whether subjects are not pressing the same key for most trials. |
| 'key_step2'   | Key pressed at step 2 choice |
