# Human Input agent
from agents.agent import Agent
from store import register_agent


@register_agent("human_agent")
class HumanAgent(Agent):
    def __init__(self):
        super(HumanAgent, self).__init__()
        self.name = "HumanAgent"
        self.dir_map = {
            "u": 0,
            "r": 1,
            "d": 2,
            "l": 3,
        }

    def step(self, chess_board, my_pos, adv_pos, max_step):
        text = input("Your move (x,y,dir): ")
        assert len(text.split(",")) == 3
        x, y, dir = text.split(",")
        x, y = int(x), int(y)
        assert 0 <= x < chess_board.shape[0]
        assert 0 <= y < chess_board.shape[1]
        if dir not in self.dir_map:
            raise ValueError("Invalid direction, should be one of u,r,d,l")
        my_pos = (x, y)
        return my_pos, self.dir_map[dir]
