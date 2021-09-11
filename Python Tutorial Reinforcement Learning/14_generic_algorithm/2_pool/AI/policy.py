# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

import numpy as np
import random


class AIPolicy:
    def __init__(self):
        pass

    def evaluate(self, game_world):
        evaluation = 1

        for i in range(len(game_world.balls)):
            for j in range(i + 1, len(game_world.balls)):
                first_ball = game_world.balls[i]
                second_ball = game_world.balls[j]

                evaluation += (
                    first_ball.position.dist_from(second_ball.position)
                    * game_config.ai.ball_distance_bonus
                )

        if game_world.is_turn_valid:
            evaluation += game_config.ai.valid_turn_bonus
            evaluation += (
                game_config.ai.pocketed_ball_bonus
                * game_world.num_of_pocketed_balls_on_turn
            )

            if game_world.is_game_over:
                evaluation += game_config.ai.game_won_bonus
        else:
            evaluation = evaluation - game_config.ai.invalid_turn_penalty

            if game_world.is_game_over:
                evaluation -= game_config.ai.game_loss_penalty

        return evaluation
