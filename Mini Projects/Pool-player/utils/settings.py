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
    2: "8 Ball",
    3: "Cue Ball"
}

BALL_MASK = ((0, 0, 68), (92, 255, 255))

CUE_MASK = ((10, 0, 142), (151, 106, 255))