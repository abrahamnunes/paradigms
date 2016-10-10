%===============================================================================
%
%   TWOARMEDBANDIT Runs a four armed bandit task
%       The reward probability associated with each slot machine varies as a
%        Gaussian process over the course of the experiment
%
%===============================================================================

%-------------------------------------------------------------------------------
%
%   Setup
%
%-------------------------------------------------------------------------------

% Close workspace and screen
close all;
clearvars;
sca;

% Default settings for Psychtoolbox
PsychDefaultSetup(2);

% Get screen numbers and if external display available, use it
screens = Screen('Screens');
screenNumber = max(screens);

% Define black and white
white = WhiteIndex(screenNumber);
black = BlackIndex(screenNumber);
grey  = white/2;
inc   = white - grey;

% Open an onscreen window
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, grey);

% Get size of screen window
[screenXpixels, screenYpixels] = Screen('WindowSize', window);

% Query the frame duration
ifi = Screen('GetFlipInterval', window);

% Get center coordinate of the window
[xCenter, yCenter] = RectCenter(windowRect);

% Alpha-blending for anti-aliased lines
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');
