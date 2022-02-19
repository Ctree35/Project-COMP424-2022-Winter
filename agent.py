import numpy as np
from copy import deepcopy


class RandomAgent:
    def __init__(self):
        self.name = "RandomAgent"
    
    def step(self, chess_board, my_pos, adv_pos, max_step):
        # Moves (Up, Right, Down, Left)
        ori_pos = deepcopy(my_pos)
        moves = ((-1, 0), (0, 1), (1, 0), (0, -1))
        steps = np.random.randint(0, max_step + 1)
        
        # Random Walk
        for _ in range(steps):
            r, c = my_pos
            dir = np.random.randint(0, 4)
            m_r, m_c = moves[dir]
            my_pos = (r + m_r, c + m_c)
            
            k = 0
            while chess_board[r, c, dir] or my_pos == adv_pos:
                k += 1
                if k > 10:
                    break
                dir = np.random.randint(0, 4)
                m_r, m_c = moves[dir]
                my_pos = (r + m_r, c + m_c)
            
            if k > 10:
                my_pos = ori_pos
                break
                
        # Put Barrier
        # dir = np.random.randint(0, 4)
        r, c = my_pos
        # while chess_board[r, c, dir]:
        #     dir = np.random.randint(0, 4)
        for dir in range(4):
            if chess_board[r, c, dir]:
                continue
            return my_pos, dir
        
        # return my_pos, dir
        