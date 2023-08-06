from traingame.game import Engine, Environment
from traingame.player import NeatSpeedAI
import neat


def eval_genomes(genomes, config, track="assen"):
    ai_players = []
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        ai_players.append(NeatSpeedAI(net))

    track = Environment(track)
    max_score = track.distance_matrix.max()
    game_engine = Engine(
        headless=False,
        environment=track,
        players=ai_players,
        tick_limit=max_score * 2
    )
    game_engine.play()
    scores = game_engine.get_scores()
    for idx, (genome_id, genome) in enumerate(genomes):
        try:
            life_span = game_engine.players[idx].ending_tick - game_engine.players[idx].starting_tick
        except AttributeError:
            life_span = game_engine.tick - game_engine.players[idx].starting_tick
        genome.fitness = (max_score - scores[idx]) - (life_span - (max_score / 2.) / 1.)
