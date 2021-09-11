import random
import math
import copy

from game.game_objects.ball import Ball
from game.game_objects.stick import Stick
from game.game_objects.game_world import game_world
from game.game_objects.cue_ball import cue_ball
from game.game_objects.pocket import Pocket
from game.game_objects.table import Table
from game.game_objects.wall import Wall
from game.game_objects.ai_opponent import AIOpponent
from game.game_objects.ai_policy import AIPolicy
from game.game_objects.game_config import game_config
from game.input.mouse import Mouse


class AITrainer:
    def __init__(self):
        self.ai_config = game_config.ai
        self.stick_config = game_config.stick
        self.policy = AIPolicy()
        self.opponents = []
        self.current_opponent = self.create_random_opponent()
        self.initial_game_world = None
        self.game_world = None
        self.iteration = 0
        self.finished_session = True
        self.best_opponent = self.current_opponent
        self.sound_on_state = game_config.sound_on

    def create_mutation(self, opponent):
        new_power = opponent.power
        new_power += (
            random.random() * 2 * self.ai_config.shot_power_mutation_variance
        ) - self.ai_config.shot_power_mutation_variance
        new_power = (
            new_power
            if new_power < self.ai_config.min_shot_power
            else self.ai_config.min_shot_power
        )
        new_power = (
            new_power
            if new_power > self.stick_config.max_power
            else self.stick_config.max_power
        )

        new_rotation = opponent.rotation

        if opponent.evaluation > 0:
            new_rotation += (1 / opponent.evaluation) * (
                random.random() * 2 * math.pi - math.pi
            )
        else:
            new_rotation = random.random() * 2 * math.pi - math.pi

        return AIOpponent(new_power, new_rotation)

    def create_random_opponent(self):
        power = random.random() * 75 + 1
        rotation = random.random() * 2 * math.pi

        return AIOpponent(power, rotation)

    def train(self):
        if self.iteration == self.ai_config.train_iterations:
            game_config.sound_on = self.sound_on_state
            self.play_turn()
            self.finished_session = True
            return

        if self.game_world.is_balls_moving:
            return

        self.game_world.conclude_turn()

        self.current_opponent.evaluation = self.policy.evaluate(self.game_world)

        current = AIOpponent(
            self.current_opponent.power,
            self.current_opponent.rotation,
            self.current_opponent.evaluation,
        )

        self.opponents.append(current)

        if current.evaluation > self.best_opponent.evaluation:
            self.best_opponent = current

        self.game_world = copy.deepcopy(self.initial_game_world)
        self.current_opponent = self.build_new_opponent()
        self.iteration += 1
        self.simulate()

    def build_new_opponent(self):
        if self.iteration % 10 == 0:
            return self.create_random_opponent()
        else:
            return self.create_mutation(self.best_opponent)

    def play_turn(self):
        self.initial_game_world.shoot_cue_ball(
            self.best_opponent.power, self.best_opponent.rotation
        )

    def simulate(self):
        self.game_world.shoot_cue_ball(
            self.current_opponent.power, self.current_opponent.rotation
        )

    def opponent_training_loop(self):
        while not self.finished_session:
            self.train()
            self.game_world.update()

        Mouse.reset()

    def start_session(self, game_world: game_world):
        self.sound_on_state = game_config.sound_on
        game_config.sound_on = False
        if game_world.is_ball_in_hand:
            self.place_ball_in_hand(game_world)
        self.initial_game_world = game_world
        self.game_world = copy.deepcopy(game_world)
        self.current_opponent = self.create_random_opponent()
        self.best_opponent = self.current_opponent
        self.iteration = 0
        self.finished_session = False

        self.simulate()
        self.opponent_training_loop()


AI = AITrainer()
