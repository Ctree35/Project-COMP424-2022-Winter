from world import World
from time import sleep

test_world = World()
test_world.render()
sleep(2)
is_end, p0_score, p1_score = test_world.step()
test_world.render()
while not is_end:
    sleep(2)
    is_end, p0_score, p1_score = test_world.step()
    test_world.render()
print(p0_score, p1_score)
