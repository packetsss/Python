from player import Player
from genotype import Genotype


class Population:
    def __init__(self, size):
        self.players = [Player(box2d[i]) for i in range(size)]
        self.generation = 1
        self.fitness_sum = 0
        self.best_player_no = 0
        self.found_winner = False
        self.balls_sunk = 0

    def update(self):
        for i in range(len(self.players)):
            self.players[i].update()

    def calculate_fitness(self):
        for i in range(len(self.players)):
            self.players[i].calculate_fitness(self.balls_sunk)
        self.fitness_sum = 0
        for i in range(len(self.players)):
            self.fitness_sum += self.players[i].fitness
        self.set_best_player()

    def set_fitness_sum(self):
        self.fitness_sum = 0
        for i in range(len(self.players)):
            self.fitness_sum += self.players[i].fitness

    def set_best_player(self):
        max = 0
        max_index = 0
        for i in range(len(self.players)):
            if self.players[i].fitness > max:
                max = self.players[i].fitness
                max_index = i
        self.best_player_no = max_index
        if self.players[max_index].won:
            self.found_winner = True
            for i in range(len(self.players)):
                self.players[i].reset()
            self.balls_sunk = self.players[max_index].balls_sunk()
            reset_worlds()
            for i in range(len(self.players)):
                self.players[i] = self.players[max_index].clone(box2d[i])
            self.increase_shots()
            self.generation += 1

    def select_player(self):
        rand = random(self.fitness_sum)
        running_sum = 0
        for i in range(len(self.players)):
            running_sum += self.players[i].fitness
            if running_sum > rand:
                return self.players[i]

    def mutate(self):
        for i in range(1, len(self.players)):
            self.players[i].DNA.mutate()

    def increase_shots(self):
        for i in range(1, len(self.players)):
            self.players[i].dna.increase_shot_length()

    def natural_selection(self):
        reset_worlds()
        new_players = [Player(box2d[i]) for i in range(len(self.players))]
        new_players[0] = self.players[self.best_player_no].clone(box2d[0])
        for i in range(1, len(self.players)):
            new_players[i] = self.select_player().clone(box2d[i])
            new_players[i].DNA.mutate()
        self.players = new_players.clone()
        self.generation += 1

    def done(self):
        for i in range(1, len(self.players)):
            if not self.players[i].game_over or not self.players[i].balls_stopped():
                return False
        return True
