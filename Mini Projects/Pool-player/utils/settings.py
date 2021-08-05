import os
import logging
import warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger('tensorflow').setLevel(logging.FATAL)
warnings.filterwarnings("ignore")

DECODER_DICT = {
    2: 11,
    7: 16,
    11: 5,
    4: 13,
    9: 3,
    8: 2,
    12: 6,
    6: 15,
    4: 13,
    0: 1,
    3: 12,
    10: 4,
    15: 9,
    1: 10,
    14: 8,
    5: 14,
    13: 7,
}

DECODER_DICT = {
    0: "Solid",
    1: "Strips",
    2: "8-Ball",
    3: "Cue-Ball"
}

BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0) 
GREEN = (0, 255, 0) 
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0) 
MAGENTA = (0, 255, 255) 
CYAN = (255, 0, 255)

BALL_MASK = ((0, 0, 68), (92, 255, 255))
BALL_MASK_2 = ((102, 28, 56), (144, 255, 255))
BALL_MASK_3 = ((78, 78, 0), (108, 255, 255))

CUE_MASK = ((15, 0, 159), (74, 111, 255))

