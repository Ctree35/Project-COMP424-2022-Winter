from world import World
from time import sleep

test_world = World(display_ui=True, display_delay=0.4)
is_end, p0_score, p1_score = test_world.step()
while not is_end:
    is_end, p0_score, p1_score = test_world.step()
print(p0_score, p1_score)
