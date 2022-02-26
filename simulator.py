from world import World
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--player_1", type=str, default="random_agent")
    parser.add_argument("--player_2", type=str, default="random_agent")
    parser.add_argument("--board_size", type=int, default=None)
    parser.add_argument("--display", action="store_true", default=False)
    parser.add_argument("--display_delay", type=float, default=0.4)
    args = parser.parse_args()
    return args


class Simulator:
    """
    Entry point of the game simulator.

    Parameters
    ----------
    args : argparse.Namespace
    """

    def __init__(self, args):
        self.world = World(
            player_1=args.player_1,
            player_2=args.player_2,
            board_size=args.board_size,
            display_ui=args.display,
            display_delay=args.display_delay,
        )

    def run(self):
        is_end, p0_score, p1_score = self.world.step()
        while not is_end:
            is_end, p0_score, p1_score = self.world.step()
        print(p0_score, p1_score)


if __name__ == "__main__":
    args = get_args()
    simulator = Simulator(args)
    simulator.run()
