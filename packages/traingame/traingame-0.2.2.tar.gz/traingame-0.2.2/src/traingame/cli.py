import typer
from typing import List, Optional
from enum import Enum
import pickle

from traingame.game import Engine, Environment
from .training import eval_genomes
import traingame.player
import neat

import pkg_resources


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
def hello(name: str):
    typer.echo(f"Hello {name}")


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        typer.echo(f"Goodbye {name}. Have a good day.")
    else:
        typer.echo(f"Bye {name}!")


@app.command()
def play(track: Track = Track.assen, ai: Optional[List[AIPlayer]] = typer.Option(None)):
    ai.insert(0, AIPlayer.human)
    typer.echo(track)
    typer.echo(ai)
    game_engine = Engine(
        headless=False,
        environment=Environment(track.value),
        players=[player(i) for i in ai]
    )
    game_engine.play()
    return


@app.command()
def example():
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        pkg_resources.resource_filename("traingame", "config/config-feedforwardspeed.cfg"))

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.Checkpointer(5))
    p.add_reporter(neat.StatisticsReporter())
    p.add_reporter(neat.StdOutReporter(True))

    # Run until a solution is found.
    winner = p.run(eval_genomes)

    # Display the winning genome.
    typer.echo('\nBest genome:\n{!s}'.format(winner))

    # save winner
    with open("saves/winner-ctrnn", "wb") as f:
        pickle.dump(winner, f)

    # Show output of the most fit genome against training data.
    # ASSEN = Environment("assen")
    # MONACO = Environment("monaco")
    # res = train_ai(NaiveAi3(), track=ASSEN)
