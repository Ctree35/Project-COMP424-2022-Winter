## UI Placeholder
import matplotlib.pyplot as plt


class UIEngine:
    def __init__(self, grid_size=(5, 5)) -> None:
        self.grid_size = grid_size

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
        self.plot_box(1, 1, self.grid_size[0] + self.grid_size[1], color="black")

    def render(self):
        plt.figure()
        self.plot_grid()
        self.plot_game_boundary()


if __name__ == "__main__":
    engine = UIEngine((5, 5))
    engine.render()
    plt.show()
