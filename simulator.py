from world import World


class Simulator:
    def __init__(self):
        self.world = World()
    
    def run(self):
        is_end, p0_score, p1_score = self.world.step()
        while not is_end:
            is_end, p0_score, p1_score = self.world.step()
        print(p0_score, p1_score)
