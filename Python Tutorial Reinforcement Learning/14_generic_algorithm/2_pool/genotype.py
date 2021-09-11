# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

class Genotype:
    def __init__(self):
        self.shots = [Vec2(random(-1, 1), random(-1, 1))]

    def mutate(self):
        mutation_rate = 0.8  # mutate 80% of the players
        for i in range(len(self.shots)):
            rand = random(1)
            if rand < mutation_rate:  # 80% of the time mutate the player
                if rand < mutation_rate / 5:
                    # 20% of the time change the vector to a random vector
                    self.shots[i] = Vec2(random(-1, 1), random(-1, 1))
                else:
                    # 80% of the time rotate the vector a small amount
                    temp = PVector(self.shots[i].x, self.shots[i].y)
                    temp.rotate(random_gaussian() / 30)
                    self.shots[i] = Vec2(temp.x, temp.y)

    def randomize(self):
        for i in range(len(self.shots)):
            self.shots[i] = Vec2(random(-1, 1), random(-1, 1))

    def clone(self):
        clone = Genotype()
        clone.shots = self.shots.copy()
        return clone

    def increase_shot_length(self):
        new_shots = [
            Vec2(self.shots[i].x, self.shots[i].y) for i in range(len(self.shots))
        ]
        new_shots.append(Vec2(random(-1, 1), random(-1, 1)))
        self.shots = new_shots
