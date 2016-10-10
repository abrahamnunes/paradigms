close all;
clearvars;
sca;

PsychDefaultSetup(2);

rng('shuffle');

screenNumber = max(Screen('Screens'));

white = WhiteIndex(screenNumber);
black = BlackIndex(screenNumber);
grey = white/2;

[window, windowRect] = PsychImaging('OpenWindow', screenNumber, grey, [], 32, 2);

Screen('Flip', window);

ifi = Screen('GetFlipInterval', window);

Screen('TextSize', window, 60);

topPriorityLevel = MaxPriority(window);

[xCenter, yCenter] = RectCenter(windowRect);

Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');

%Interstimulus interval info

isiTimeSecs = 1;
isiTimeFrames = round(isiTimeSecs/ifi);

waitframes = 1;

%Keyboard info (keys to listen for)

escapeKey = KbName('ESCAPE');
leftKey   = KbName('LeftArrow');
rightKey  = KbName('RightArrow');
downKey   = KbName('DownArrow');

%Colors in words

wordList = {'Red', 'Green', 'Blue'};
rgbColors = [1 0 0; 0 1 0; 0 0 1];
condMatrixBase = [sort(repmat([1 2 3], 1, 3)); repmat([1 2 3], 1, 3)];
trialsPerCondition = 1;
condMatrix = repmat(condMatrixBase, 1, trialsPerCondition);

[~, numTrials] = size(condMatrix);

shuffler = Shuffle(1:numTrials);
condMatrixShuffled = condMatrix(:, shuffler);

%Responsematrix

respMat = nan(4, numTrials);

%trial loop

for trial = 1:numTrials
    wordNum = condMatrixShuffled(1, trial);
    colorNum = condMatrixShuffled(2, trial);

    theWord = wordList(wordNum);
    theColor = rgbColors(colorNum, :);
    respToBeMade = true;

    if trial == 1
        DrawFormattedText(window, 'Name the color \n\n Press Any Key To Begin', 'center', 'center', black);
        Screen('Flip', window);
        KbStrokeWait;
    end

    Screen('DrawDots', window, [xCenter; yCenter], 10, black, [], 2);
    vbl = Screen('Flip', window);

    for frame = 1:isiTimeFrames-1
        Screen('DrawDots', window, [xCenter; yCenter], 10, black, [], 2);
        vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);
    end

    tStart = GetSecs;
    while respToBeMade == true
        DrawFormattedText(window, char(theWord), 'center', 'center', theColor);

        [keyIsDown, secs, keyCode] = KbCheck;
        if keyCode(escapeKey)
            ShowCursor;
            sca;
            return
        elseif keyCode(leftKey)
            response = 1;
            respToBeMade = false;
        elseif keyCode(downKey)
            response = 2;
            respToBeMade = false;
        elseif keyCode(rightKey)
            response = 3;
            respToBeMade = false;
        end

        vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);
    end

    tEnd = GetSecs;
    rt = tEnd - tStart;
    respMat(1, trial) = wordNum;
    respMat(2, trial) = colorNum;
    respMat(3, trial) = response;
    respMat(4, trial) = rt;

end

DrawFormattedText(window, 'Experiment Finished \n\n Press Any Key to Exit', 'center', 'center', black);
Screen('Flip', window);

KbStrokeWait;
sca;
