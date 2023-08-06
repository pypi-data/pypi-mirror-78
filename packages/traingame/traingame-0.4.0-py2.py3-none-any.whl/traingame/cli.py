import typer
from typing import List, Optional
from enum import Enum
import pickle

from traingame.game import Engine, Environment
from .training import eval_genomes, fitness_speed, fitness_distance
import traingame.player
import neat

import pkg_resources
from functools import partial


ai_players = {
    "human": traingame.player.HumanPlayer,
    "naive": traingame.player.NaiveAi,
    "naive2": traingame.player.NaiveAi2,
    "naive3": traingame.player.NaiveAi3,
    "pretrained": traingame.player.PreTrainedAI,
    "pretrainedspeed": traingame.player.PreTrainedSpeedAI,
}


class Track(str, Enum):
    assen = "assen"
    monaco = "monaco"


class AIPlayer(str, Enum):
    human = "human"
    naive = "naive"
    naive2 = "naive2"
    naive3 = "naive3"
    pretrained = "pretrained"
    pretrainedspeed = "pretrainedspeed"


def player(name: Track):
    return ai_players[name.value]()


app = typer.Typer()


@app.command()
def run(track: Track = Track.assen, ai: Optional[List[AIPlayer]] = typer.Option(None)):
    game_engine = Engine(
        headless=False,
        environment=Environment(track.value),
        players=[player(i) for i in ai]
    )
    game_engine.play()
    return


@app.command()
def play(track: Track = Track.assen, ai: Optional[List[AIPlayer]] = typer.Option(None)):
    ai.insert(0, AIPlayer.human)
    run(track=track, ai=ai)
    return


@app.command()
def example(speed: bool = False, checkpoints: int = 0,
            statistics: bool = True, stdout: bool = True,
            save: bool = True, track: Track = Track.assen):

    config_file = "config-feedforwardspeed.cfg" if speed else "config-feedforward.cfg"
    ai = "neatspeed" if speed else "neat"
    fitness = fitness_speed if speed else fitness_distance

    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        pkg_resources.resource_filename("traingame", f"config/{config_file}"))

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    if checkpoints:
        p.add_reporter(neat.Checkpointer(checkpoints))
    if statistics:
        p.add_reporter(neat.StatisticsReporter())
    if stdout:
        p.add_reporter(neat.StdOutReporter(True))

    # Run until a solution is found.
    train_func = partial(eval_genomes, track=track.value, ai=ai, apply_fitness=fitness)
    winner = p.run(train_func)

    # Display the winning genome.
    typer.echo('\nBest genome:\n{!s}'.format(winner))

    # save winner
    if save:
        with open("saves/winner-ctrnn", "wb") as f:
            pickle.dump(winner, f)

    # Show output of the most fit genome against training data.
    # ASSEN = Environment("assen")
    # MONACO = Environment("monaco")
    # res = train_ai(NaiveAi3(), track=ASSEN)
