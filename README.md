<h1>Resumen<h1>

<h1>Archivos y funcionamiento<h1>
  
* ```/main.py```: Archivo principal que corre<br>
* ```/Game```: <br>
    * ```/Game.py```: <br>
* ```/Synth```: <br>
    * ```/Synth.py```: <br>
* ```/genetic_model```: <br>
   * ```/genetic_model.py```: <br>
* ```/data.csv```: Donde se almacenan los datos del juego.<br>

<h1>Parameters<h1>
  
Needed:
* coords((x,y) tuple)
Optional:
* lineal_speed(default 8): speed of movement
* rotation_speed(default 8): speed of rotation
* damage_power(default 70): damage when hit someone
* ammo(default 20): if they kill can get rewards in ammo
* health(default 100): -if they get shot they loose health
* shooting_range(default 100): in pixels is the range of the shot
* controllable(default False): if its true the synth respons to the keyboard
* shooting_timer_max(default 5): cuanto mayor sea, mas largo es el disparo
* delta_angle(default 20): Is the length in degres of the ranges of detecton,
where place the detected enemies, _sense_data_buffer will have a 360//delta_angle
length
* _weights: contains the setteable weights for nn

Main synth´s methods:
* move_forward() move_backwards(),turn_left(),turn_right(): move the synth
* shoot():activate the state of shoot, that has to decrease
* get_senseDataBuffer(): get _sense_data_buffer that is a list that contains the
distances of detected enemies in ranges, if more than two enemies are in the same
range is used the nearest, if in the range are no enemies the range has False
* set_weights(): get _weights atribute
* get_weights(weights) set _weights atribute
* get_kills(): get kills that the individual has done
* set_controllable(bool): sets the controllable atribute
* restore_stats(), restore health and ammo to its starting points

<h1>Capturas<h1>
  
  ![img](https://github.com/MartinCastillo/IA-Royale/blob/master/captures/1.PNG)
  ![img](https://github.com/MartinCastillo/IA-Royale/blob/master/captures/2.PNG)
  ![img](https://github.com/MartinCastillo/IA-Royale/blob/master/captures/3.PNG)
  ![img](https://github.com/MartinCastillo/IA-Royale/blob/master/captures/4.PNG)
  ![img](https://github.com/MartinCastillo/IA-Royale/blob/master/captures/5.PNG)
  ![img](https://github.com/MartinCastillo/IA-Royale/blob/master/captures/6.PNG)
