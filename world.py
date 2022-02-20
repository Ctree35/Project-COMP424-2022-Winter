# TODO: refactor code to make it readable (e.g., set consts)
import numpy as np
from agents.random_agent import RandomAgent
from copy import deepcopy


class World:
    def __init__(self):
        # Two players
        # TODO: load agents from agent files
        self.p0 = RandomAgent()
        self.p1 = RandomAgent()
        
        # Moves (Up, Right, Down, Left)
        self.moves = ((-1, 0), (0, 1), (1, 0), (0, -1))
        
        # Random chessboard size
        self.board_size = np.random.randint(5, 10)

        # Index in dim2 represents [Up, Right, Down, Left] respectively
        # Record barriers and boarders for each block
        self.chess_board = np.zeros((self.board_size, self.board_size, 4), dtype=bool)
        
        # Set boarders
        self.chess_board[0, :, 0] = True
        self.chess_board[:, 0, 3] = True
        self.chess_board[-1, :, 2] = True
        self.chess_board[:, -1, 1] = True
        
        # Random start position (symmetric but not overlap)
        self.p0_pos = np.random.randint(0, self.board_size, size=2)
        self.p1_pos = self.board_size - 1 - self.p0_pos
        while np.array_equal(self.p0_pos, self.p1_pos):
            self.p0_pos = np.random.randint(0, self.board_size, size=2)
            self.p1_pos = self.board_size - 1 - self.p0_pos
        # Whose turn to step
        self.turn = 0
        
        # Maximum Steps
        self.max_step = (self.board_size + 1) // 2
    
    def step(self):
        if not self.turn:
            cur_player = self.p0
            cur_pos = self.p0_pos
            adv_pos = self.p1_pos
        else:
            cur_player = self.p1
            cur_pos = self.p1_pos
            adv_pos = self.p0_pos
        
        try:
            # TODO: Check Timeout
            next_pos, dir = cur_player.step(
                deepcopy(self.chess_board),
                tuple(cur_pos),
                tuple(adv_pos),
                self.max_step
            )
            next_pos = np.asarray(next_pos, dtype=cur_pos.dtype)
            if not self.check_boundary(next_pos):
                raise ValueError("End position {} is out of boundary".format(next_pos))
            if not 0 <= dir <= 3:
                raise ValueError("Barrier dir should reside in [0, 3], but your dir is {}".format(dir))
            if not self.check_valid_step(cur_pos, next_pos, dir):
                raise ValueError("End position {} cannot be reached from {}".format(next_pos, cur_pos))
        except TypeError or ValueError as e:
            print(e)
            print("Execute Random Walk!")
            next_pos, dir = self.random_walk(tuple(cur_pos), tuple(adv_pos))
            
        # Print out each step
        print(self.turn, next_pos, dir)
        if not self.turn:
            self.p0_pos = next_pos
        else:
            self.p1_pos = next_pos
        # Set the barrier to True
        r, c = next_pos
        self.chess_board[r, c, dir] = True
        # Set the opposite barrier to True
        move = self.moves[dir]
        self.chess_board[r + move[0], c + move[1], abs(dir - 2)] = True
        # Change turn
        self.turn = 1 - self.turn
        
        return self.check_endgame()
        # TODO: Print out Chessboard for visualization
    
    def check_valid_step(self, start_pos, end_pos, barrier_dir):
        # Endpoint already has barrier or is boarder
        r, c = end_pos
        if self.chess_board[r, c, barrier_dir]:
            return False
        if np.array_equal(start_pos, end_pos):
            return True
        
        # Get position of the adversary
        adv_pos = self.p0_pos if self.turn else self.p1_pos
        
        # BFS
        state_queue = [(start_pos, 0)]
        visited = {tuple(start_pos)}
        is_reached = False
        while state_queue and not is_reached:
            cur_pos, cur_step = state_queue.pop(0)
            r, c = cur_pos
            if cur_step == self.max_step:
                break
            for dir, move in enumerate(self.moves):
                if self.chess_board[r, c, dir]:
                    continue
                
                next_pos = cur_pos + move
                if np.array_equal(next_pos, adv_pos) or tuple(next_pos) in visited:
                    continue
                if np.array_equal(next_pos, end_pos):
                    is_reached = True
                    break
                
                visited.add(tuple(next_pos))
                state_queue.append((next_pos, cur_step + 1))
        
        return is_reached
    
    def check_endgame(self):
        # Union-Find
        father = dict()
        for r in range(self.board_size):
            for c in range(self.board_size):
                father[(r, c)] = (r, c)
                
        def find(pos):
            if father[pos] != pos:
                father[pos] = find(father[pos])
            return father[pos]
        
        def union(pos1, pos2):
            father[pos1] = pos2
        
        for r in range(self.board_size):
            for c in range(self.board_size):
                for dir, move in enumerate(self.moves[1:3]): # Only check down and right
                    if self.chess_board[r, c, dir + 1]:
                        continue
                    pos_a = find((r, c))
                    pos_b = find((r + move[0], c + move[1]))
                    if pos_a != pos_b:
                        union(pos_a, pos_b)
        
        p0_r = find(tuple(self.p0_pos))
        p1_r = find(tuple(self.p1_pos))

        if p0_r == p1_r:
            return False, 0, 0
        p0_score = list(father.values()).count(p0_r)
        p1_score = list(father.values()).count(p1_r)
        return True, p0_score, p1_score
    
    def check_boundary(self, pos):
        r, c = pos
        return 0 <= r < self.board_size and 0 <= c < self.board_size

    def random_walk(self, my_pos, adv_pos):
        ori_pos = deepcopy(my_pos)
        steps = np.random.randint(0, self.max_step + 1)
        # Random Walk
        for _ in range(steps):
            r, c = my_pos
            dir = np.random.randint(0, 4)
            m_r, m_c = self.moves[dir]
            my_pos = (r + m_r, c + m_c)
    
            # Special Case enclosed by Adversary
            k = 0
            while self.chess_board[r, c, dir] or my_pos == adv_pos:
                k += 1
                if k > 10:
                    break
                dir = np.random.randint(0, 4)
                m_r, m_c = self.moves[dir]
                my_pos = (r + m_r, c + m_c)
    
            if k > 10:
                my_pos = ori_pos
                break

        # Put Barrier
        dir = np.random.randint(0, 4)
        r, c = my_pos
        while self.chess_board[r, c, dir]:
            dir = np.random.randint(0, 4)

        return my_pos, dir
    
    
if __name__ == "__main__":
    world = World()
    is_end, p0_score, p1_score = world.step()
    while not is_end:
        is_end, p0_score, p1_score = world.step()
    print(p0_score, p1_score)
