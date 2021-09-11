# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

from genotype import Genotype


class Player:
    def __init__(self, world):
        self.DNA = Genotype()
        self.up_to_shot = 0
        self.fitness = 0
        self.white_ball = Ball(200, 600, world, (255))
        self.white_ball.is_white = True
        self.balls = [
            Ball(200, 216, world, (240, 0, 0)),
            Ball(200 - 14, 216 - 16, world, (0, 140, 0)),
            Ball(200 + 14, 216 - 16, world, (0, 0, 240)),
            Ball(200 - (2 * 14), 216 - (2 * 16), world, (253, 211, 0)),
            Ball(200, 216 - (2 * 16), world, (0)),
            Ball(200 + (2 * 14), 216 - (2 * 16), world, (255, 119, 10)),
            Ball(200 - (3 * 14), 216 - (3 * 16), world, (253, 137, 168)),
            Ball(200 - (14), 216 - (3 * 16), world, (101, 1, 105)),
            Ball(200 + (14), 216 - (3 * 16), world, (90, 0, 0)),
            Ball(200 + (3 * 14), 216 - (3 * 16), world, (122, 234, 242)),
            Ball(200 - (4 * 14), 216 - (4 * 16), world, (55, 93, 93)),
            Ball(200 - (2 * 14), 216 - (4 * 16), world, (128, 128, 0)),
            Ball(200, 216 - (4 * 16), world, (186, 85, 211)),
            Ball(200 + (2 * 14), 216 - (4 * 16), world, (244, 164, 96)),
            Ball(200 + (4 * 14), 216 - (4 * 16), world, (0, 255, 150)),
        ]
        self.game_over = False
        self.won = False
        self.World = world

    def update(self):
        for i in self.balls:
            i.update()
        self.white_ball.update()
        if not self.game_over and self.balls_stopped():
            self.shoot()
        if self.white_ball.is_in_hole():
            self.game_over = True
        if self.game_finished():
            self.game_over = True

    def show(self):
        self.white_ball.show()
        for i in self.balls:
            i.show()

    def calculate_fitness(self, balls_sunk_previously):
        self.fitness = 0
        if self.white_ball.is_in_hole():
            return
        total_distance = 0
        balls_sunk = 0
        for i in self.balls:
            if not i.is_in_hole():
                total_distance += i.distance_to_closest_hole()
            else:
                balls_sunk += 1
                if i.is_black and not self.black_ball_is_last():
                    self.fitness = 0
                    self.game_over = True
                    return
        if total_distance == 0:
            self.fitness = 1000
        else:
            self.fitness = (
                (1 + (balls_sunk - balls_sunk_previously))
                * (1 + (balls_sunk - balls_sunk_previously))
            ) / (total_distance)

    def balls_stopped(self):
        for i in self.balls:
            if not i.is_stopped():
                return False
        return True

    def game_finished(self):
        for i in self.balls:
            if not i.is_in_hole():
                return False
        return True

    def shoot(self):
        if self.up_to_shot >= len(self.DNA.shots) or self.game_over:
            self.game_over = True
            return
        self.white_ball.apply_force(self.dna.shots[self.up_to_shot])
        self.up_to_shot += 1

    def clone(self, world):
        clone = Player(world)
        clone.DNA = self.DNA.clone()
        return clone
