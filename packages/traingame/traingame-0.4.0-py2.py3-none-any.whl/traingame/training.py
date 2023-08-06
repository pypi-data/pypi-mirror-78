from traingame.game import Engine, Environment
from traingame.player import NeatAI, NeatSpeedAI
import neat


def fitness_distance(genomes, engine):
    scores = engine.get_scores()
    max_score = engine.track.distance_matrix.max()
    for idx, (genome_id, genome) in enumerate(genomes):
        genome.fitness = max_score - scores[idx]


def fitness_speed(genomes, engine):
    scores = engine.get_scores()
    max_score = engine.track.distance_matrix.max()
    for idx, (genome_id, genome) in enumerate(genomes):
        try:
            life_span = engine.players[idx].ending_tick - engine.players[idx].starting_tick
        except AttributeError:
            life_span = engine.tick - engine.players[idx].starting_tick
        genome.fitness = (max_score - scores[idx]) - (life_span - (max_score / 2.) / 1.)


def eval_genomes(genomes, config, track="assen", ai="neatspeed", apply_fitness=fitness_speed):
    if ai == "neat":
        AI = NeatAI
    elif ai == "neatspeed":
        AI = NeatSpeedAI
    else:
        raise ValueError("Unknown AI: not configure for {}".format(ai))

    ai_players = []
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        ai_players.append(AI(net))

    track = Environment(track)
    max_score = track.distance_matrix.max()
    game_engine = Engine(
        headless=False,
        environment=track,
        players=ai_players,
        tick_limit=max_score * 2
    )
    game_engine.play()

    apply_fitness(genomes, game_engine)

    scores = game_engine.get_scores()
    for idx, (genome_id, genome) in enumerate(genomes):
        try:
            life_span = game_engine.players[idx].ending_tick - game_engine.players[idx].starting_tick
        except AttributeError:
            life_span = game_engine.tick - game_engine.players[idx].starting_tick
        genome.fitness = (max_score - scores[idx]) - (life_span - (max_score / 2.) / 1.)
