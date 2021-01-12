"""
-------------------------------------------------------------------------------
'Synths' refer to the agents-bots-individuals
-------------------------------------------------------------------------------
Synth´s setteable atributes(parameters):
Needed:
-coords((x,y) tuple)
Optional:
-lineal_speed(default 8): speed of movement
-rotation_speed(default 8): speed of rotation
-damage_power(default 70): damage when hit someone
-ammo(default 20): if they kill can get rewards in ammo
-health(default 100): -if they get shot they loose health
-shooting_range(default 100): in pixels is the range of the shot
-controllable(default False): if its true the synth respons to the keyboard
-shooting_timer_max(default 5): cuanto mayor sea, mas largo es el disparo
-delta_angle(default 20): Is the length in degres of the ranges of detecton,
where place the detected enemies, _sense_data_buffer will have a 360//delta_angle
length
-_weights: contains the setteable weights for nn

-------------------------------------------------------------------------------
Main synth´s methods:
-move_forward() move_backwards(),turn_left(),turn_right(): move the synth
-shoot():activate the state of shoot, that has to decrease
-get_senseDataBuffer(): get _sense_data_buffer that is a list that contains the
distances of detected enemies in ranges, if more than two enemies are in the same
range is used the nearest, if in the range are no enemies the range has False
-set_weights(): get _weights atribute
-get_weights(weights) set _weights atribute
-get_kills(): get kills that the individual has done
-set_controllable(bool): sets the controllable atribute
-restore_stats(), restore health and ammo to its starting points
-------------------------------------------------------------------------------
ALL THE PARAMETES OF THE GAME.RUN FUNCTIONS AND OTHERS IN help(Game.run) or help(Synth)
In evaluate_synth(synth) function given as parameter to game.run, is determined the
behave of the synth.
-------------------------------------------------------------------------------
"""
from random import uniform,randint
import numpy as np
#local imports
from modules.Game.Game import Game
from modules.genetic_model.genetic_model import generate_population,model_crossover,model_mutate,restart_population
#Default stats of individuals
synth_stats = {'health':100,'ammo':1000,'delta_angle':30}
starting_map_size = (700,700)
mutate_probability = 0.7
population_size = 300
population_reduction_fraction = 80/100
iters = 1
def evaluate_synth(synth):
    """evaluate_synth"""
    if(not synth.is_controllable()):
        #synth.get_senseDataBuffer(), values are in pixels, so are from 0 to max(map_size)
        #maximum of each range is max(starting_map_size)
        nn_inputs = synth.get_senseDataBuffer()
        nn_inputs = np.array(nn_inputs)/max(starting_map_size)
        nn_inputs = np.atleast_2d(nn_inputs)
        output = synth.get_model().predict(nn_inputs,1)[0]
        #Son 4 acciones posibles adelante derecha izquierda y disparar
        actions = [synth.shoot,synth.move_forward,synth.turn_right,synth.turn_left]
        steps = 1/len(actions)
        i = True
        while i:
            for _ in range(len(actions)):
                if(_*steps<output<=(_+1)*steps)and(randint(0,2)):
                    actions[_]()
                    i = False

if(__name__=='__main__'):
    """Genera población"""
    population = generate_population(population_size,starting_map_size,**synth_stats)
    game = Game(ammo_reward=8, population_reduction_fraction=population_reduction_fraction,
        area_reduction_delay=2,prompt_messages=False, starting_map_size=starting_map_size,
        render_text=False,render_synth_details=False)
    for _ in range(iters):
        render = True
        #Te falta hacer un parametro de temporizador, el tiempo máximo de juego
        """eliminación (juego)"""
        population, ret = game.run(population,evaluate_synth,render=render,text="Ronda: {}".format(_))
        if(not ret):
            break
        print(len(population))
        """cruce"""
        sorted_population = sorted(population,key=lambda x:x.get_kills(),reverse=True)
        for (ix1,individual1) in enumerate(sorted_population):
            for (ix2,individual2) in enumerate(sorted_population):
                #Cruza hasta que haya suficientes para restaurar el tamaño de la población,
                #deben ser diferentes, es solo provisional, deberías hacer que la probabilidad sea
                #mayor con más kills, pero debe haber aletoriedad
                if(ix1!=ix2)and(len(population)<population_size):
                    new_individual = model_crossover(individual1,individual2)[0]
                    if(uniform(0,1)<mutate_probability):
                        model_mutate(new_individual,mutate_probability)
                    population.append(new_individual)
        population = restart_population(population,starting_map_size,**synth_stats)
    pass
