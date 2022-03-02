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

    def reset(self, swap_players=False):
        """
        Reset the game

        Parameters
        ----------
        swap_players : bool
            if True, swap the players
        """
        if swap_players:
            player_1, player_2 = self.args.player_2, self.args.player_1
        else:
            player_1, player_2 = self.args.player_1, self.args.player_2
        self.world = World(
            player_1=player_1,
            player_2=player_2,
            board_size=self.args.board_size,
            display_ui=self.args.display,
            display_delay=self.args.display_delay,
            autoplay=self.args.autoplay,
        )
        if self.world.initial_end:
            logger.warning("Initialization failed! Reset the world again!")
            self.reset()

    def run(self, swap_players=False):
        self.reset(swap_players=swap_players)
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
            for i in tqdm(range(self.args.autoplay_runs)):
                swap_players = i % 2 == 0
                p0_score, p1_score = self.run(swap_players=swap_players)
                if swap_players:
                    p0_score, p1_score = p1_score, p0_score
                if p0_score > p1_score:
                    p1_win_count += 1
                elif p0_score < p1_score:
                    p2_win_count += 1
                else:  # Tie
                    p1_win_count += 1
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
