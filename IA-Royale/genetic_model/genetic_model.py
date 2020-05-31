#Contine funciones para administrar la población-synths-individuos
from Synth.Synth import Synth
import numpy as np
from random import randint,uniform
from keras.models import Sequential
from keras.layers import Dense,Activation

def create_model(n_inputs):
    model = Sequential()
    model.add(Dense(n_inputs,input_shape = (n_inputs,)))
    model.add(Dense(20,input_shape = (n_inputs,)))
    model.add(Dense(15,input_shape = (20,)))
    model.add(Dense(1,input_shape = (15,)))
    model.add(Activation('sigmoid'))
    model.compile(loss='mse',optimizer='adam',metrics=['accuracy'])
    return model

def pick_random_coords(map_size):
    rx = randint(0,map_size[0]) ; ry = randint(0,map_size[1])
    return(rx,ry)

def generate_population(size,map_size,**kargs):
    #-size=number of individuals, -map_size=size of the game´map, the range of the coords,
    #-**kargs parameters given when creating the Synth objects, angle and coords are random
    p = []
    n_inputs = 360//kargs['delta_angle']
    for _ in range(size):
        p.append(Synth(pick_random_coords(map_size), angle= randint(0,360),**kargs))
        p[_].set_model(create_model(n_inputs))
    return p

def restart_population(population,map_size,**kargs):
    #restore health and ammo of the synth and pick randomly the coords
    for p in population:
        p.set_all(**kargs)
        p.set_coords(pick_random_coords(map_size))
        p.set_angle(randint(0,360))
    return population

def model_crossover(parent1,parent2,**kargs):
    model1 = parent1.get_model()
    model2 = parent2.get_model()
    weight1 = model1.get_weights()
    weight2 = model2.get_weights()
    new_weight1=weight1
    new_weight2=weight1
    gene = randint(0,len(new_weight1)-1)
    new_weight1[gene] = weight2[gene]
    new_weight2[gene] = weight1[gene]
    model1.set_weights(new_weight1)
    model2.set_weights(new_weight2)
    new_parent1 = Synth((0,0),**kargs)
    new_parent2 = Synth((0,0),**kargs)
    new_parent1.set_model(model1)
    new_parent2.set_model(model2)
    return new_parent1,new_parent2

def model_mutate(individual,mutate_probability):
    gens_to_modify = 2
    modified = 0
    model = individual.get_model()
    weights = model.get_weights()
    for i in range(len(weights)-1):
        if(uniform(0,1)<mutate_probability)and(gens_to_modify):
            weights[i] = weights[i]*uniform(0,2)
            modified += 1
    model.set_weights(weights)
    individual.set_model(model)
