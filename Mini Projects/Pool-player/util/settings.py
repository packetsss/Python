import os
import logging
import warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger('tensorflow').setLevel(logging.FATAL)
warnings.filterwarnings("ignore")

DECODER_DICT_OLD = {
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
    0: "solids",
    1: "strips",
    2: "8-ball",
    3: "cue-ball",
    4: "cue-tip"
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

WIDTH, HEIGHT = 1120, 620
RAIL_DIST = 30
# top-left -> top-right -> bottom-right -> bottom-left -> top-left
DIAMONDS = ((185, RAIL_DIST), (310, RAIL_DIST), (435, RAIL_DIST), (685, RAIL_DIST), (810, RAIL_DIST), (935, RAIL_DIST), (WIDTH - RAIL_DIST, 185), (WIDTH - RAIL_DIST, 310), (WIDTH - RAIL_DIST, 435), (935, HEIGHT - RAIL_DIST), (810, HEIGHT - RAIL_DIST), (685, HEIGHT - RAIL_DIST), (435, HEIGHT - RAIL_DIST), (310, HEIGHT - RAIL_DIST), (185, HEIGHT - RAIL_DIST), (RAIL_DIST, 435), (RAIL_DIST, 310), (RAIL_DIST, 185))
REAL_DIAMONDS = ((424, 228), (584, 227), (743, 230), (1053, 236), (1205, 237), (1354, 240), (1539, 431), (1542, 581), (1543, 734), (1359, 929), (1209, 934), (1053, 936), (738, 942), (576, 946), (414, 948), (208, 747), (213, 585), (214, 424))


# L, R, T, B
DIST_FROM_EDGE_TO_RAIL = 65
RAIL_LOCATION = (DIST_FROM_EDGE_TO_RAIL, WIDTH - DIST_FROM_EDGE_TO_RAIL, DIST_FROM_EDGE_TO_RAIL, HEIGHT - DIST_FROM_EDGE_TO_RAIL)

