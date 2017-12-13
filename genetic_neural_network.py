"""
    Start a new game and move the car forward one frame without turning.
    Get a reading of the sensors.
    Based on those readings, predict Q values. These predictions show Robocar’s confidence that it should take each of the three actions listed above. The first time through, these will be worthless, but we have to start somewhere.
    Generate a random number. If it’s less than our epsilon (see below), choose a random action. If it’s higher than our epsilon, choose the most confident action returned from our prediction.
    Execute the action (left, right, nothing) and get another sensor reading and our reward.
    We store these things—the original reading, the action we took, the reward we got and the new reading—in an array that we call a buffer.
    Grab a random sample of “reading, action, reward, new reading” from our buffer and learn by building an X, y training set that we “fit” our model to.
    This is the most complicated part of the whole thing, and what I have the most trouble getting my head around. But let me try…
    We set the y value for the iteration to a prediction based on the original reading.
    We make a new prediction based on our new reading (post-action state).
    We take a look at the reward we were given by taking the action. If it’s -500, we’ve run into something, and so we set the y for this iteration and this action to -500. If we didn’t run into anything, we multiply our max predicted Q value by a gamma (to discount it) and set the iteration’s y value for the action we took.
    Go back to step 2 until we run into something.
    When we run into something, decrease our epsilon and go back to step 1.
"""

import keras
import numpy as np


INPUT_LAYER_SIZE = 3
OUTPUT_LAYER_SIZE = 1
