from world import World, PLAYER_1_NAME, PLAYER_2_NAME
import argparse
from utils import all_logging_disabled
import logging
from tqdm import tqdm

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

logger = logging.getLogger(__name__)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--player_1", type=str, default="random_agent")
    parser.add_argument("--player_2", type=str, default="random_agent")
    parser.add_argument("--board_size", type=int, default=None)
    parser.add_argument("--display", action="store_true", default=False)
    parser.add_argument("--display_delay", type=float, default=0.4)
    parser.add_argument("--autoplay", action="store_true", default=False)
    parser.add_argument("--autoplay_runs", type=int, default=1000)
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
        self.args = args

    def reset(self):
        """
        Reset the game
        """
        self.world = World(
            player_1=self.args.player_1,
            player_2=self.args.player_2,
            board_size=self.args.board_size,
            display_ui=self.args.display,
            display_delay=self.args.display_delay,
            autoplay=self.args.autoplay,
        )

    def run(self):
        self.reset()
        is_end, p0_score, p1_score = self.world.step()
        while not is_end:
            is_end, p0_score, p1_score = self.world.step()
        logger.info(
            f"Run finished. Player {PLAYER_1_NAME}: {p0_score}, Player {PLAYER_2_NAME}: {p1_score}"
        )
        return p0_score, p1_score

    def autoplay(self):
        """
        Run multiple simulations of the gameplay and aggregate win %
        """
        p1_win_count = 0
        p2_win_count = 0
        if self.args.display:
            logger.warning("Since running autoplay mode, display will be disabled")
        self.args.display = False
        with all_logging_disabled():
            for _ in tqdm(range(self.args.autoplay_runs)):
                p0_score, p1_score = self.run()
                if p0_score > p1_score:
                    p1_win_count += 1
                else:
                    p2_win_count += 1

        logger.info(
            f"Player {PLAYER_1_NAME} win percentage: {p1_win_count / self.args.autoplay_runs}"
        )
        logger.info(
            f"Player {PLAYER_2_NAME} win percentage: {p2_win_count / self.args.autoplay_runs}"
        )


if __name__ == "__main__":
    args = get_args()
    simulator = Simulator(args)
    if args.autoplay:
        simulator.autoplay()
    else:
        simulator.run()
