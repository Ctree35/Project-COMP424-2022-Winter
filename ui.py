## UI Placeholder
from turtle import down
import matplotlib.pyplot as plt


class UIEngine:
    def __init__(self, grid_width=5) -> None:
        self.grid_size = (grid_width, grid_width)
        plt.figure()
        # plt.axis([0, 0, 0, 10])
        plt.ion()

    # [x1,x2] -> [y1,y2]
    def plot_box(
        self,
        x,
        y,
        w,
        text="",
        set_left_wall=False,
        set_right_wall=False,
        set_top_wall=False,
        set_bottom_wall=False,
        color="silver",
    ):
        # left wall
        plt.plot([x, x], [y, y + w], "-", lw=2, color="red" if set_left_wall else color)
        # top wall
        plt.plot(
            [x + w, x],
            [y + w, y + w],
            "-",
            lw=2,
            color="red" if set_top_wall else color,
        )
        # right wall
        plt.plot(
            [x + w, x + w],
            [y, y + w],
            "-",
            lw=2,
            color="red" if set_right_wall else color,
        )
        # bottom wall
        plt.plot(
            [x, x + w], [y, y], "-", lw=2, color="red" if set_bottom_wall else color
        )
        if len(text) > 0:
            plt.text(x + w / 2, y + w / 2, text, ha="center", va="center")

    def plot_grid(self):
        for x in range(1, self.grid_size[0] * 2 + 1, 2):
            for y in range(1, self.grid_size[1] * 2 + 1, 2):
                self.plot_box(x, y, 2)

    def plot_game_boundary(
        self,
    ):
        # start y=3 as the y in the range ends in 3
        self.plot_box(1, 3, self.grid_size[0] + self.grid_size[1], color="black")

    def plot_grid_with_board(
        self, chess_board, player_1_pos=None, player_2_pos=None, debug=False
    ):
        x_pos = 0
        for y in range(self.grid_size[1] * 2 + 1, 1, -2):
            y_pos = 0
            for x in range(1, self.grid_size[0] * 2 + 1, 2):
                up_wall = chess_board[x_pos, y_pos, 0]
                right_wall = chess_board[x_pos, y_pos, 1]
                down_wall = chess_board[x_pos, y_pos, 2]
                left_wall = chess_board[x_pos, y_pos, 3]

                # Display text
                text = ""
                if player_1_pos is not None:
                    if player_1_pos[0] == x_pos and player_1_pos[1] == y_pos:
                        text += "A"
                if player_2_pos is not None:
                    if player_2_pos[0] == x_pos and player_2_pos[1] == y_pos:
                        text += "B"

                if debug:
                    text += " " + str(x_pos) + "," + str(y_pos)

                self.plot_box(
                    x,
                    y,
                    2,
                    set_left_wall=left_wall,
                    set_right_wall=right_wall,
                    set_top_wall=up_wall,
                    set_bottom_wall=down_wall,
                    text=text,
                )
                y_pos += 1
            x_pos += 1

    def render(self, chess_board, p1_pos, p2_pos, debug=False):
        """
        Render the board along with player positions
        Arguments:

        - chess_board: 3D array of pieces
        - p1_pos: position of player 1
        - p2_pos: position of player 2
        - debug: if True, display the position of each piece

        """
        plt.clf()
        self.plot_grid_with_board(chess_board, p1_pos, p2_pos, debug=debug)
        self.plot_game_boundary()
        plt.pause(0.1)


if __name__ == "__main__":
    engine = UIEngine((5, 5))
    engine.render()
    plt.show()
