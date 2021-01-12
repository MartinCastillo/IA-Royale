from modules.Game.Game import Game
from modules.Synth.Synth import Synth
def evaluate_synth(synth):
    pass

if(__name__=='__main__'):
    game = Game()
    population = [Synth((100,100),controllable=True)]
    population, ret = game.run(population,evaluate_synth,render=True)
