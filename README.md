<h1>Resumen</h1>
Consiste en un entorno de battle royale (Varios jugadores entran y pelean hasta que no quede ninguno u ocurra otra condición), con todo lo necesario para entrenar a los "jugadores" con algoritmos de machine learning para lograr que sobrevivan lo más posible.<br>
La idea principal es que se pueden crear jugadores a gusto en el mapa (mapa que todavia no es facilmente personalizable, como para por ejemplo poner obstaculos, pero está en proceso), estos jugadores pueden moverse, ver y disparar según lo vean conveniente, el mapa se puede programar para encogerse a medida que transcurre el tiempo de juego.
Es posible programar el comportamiento de estos jugadores frente a situaciones, o entrenarlo por medio de algoritmos (Que es el foco).<br>
La meta es entrenar a los individuos para que sean progresivamente más habiles. Y explorar algoritmos en estos jugadores para ver cuales les favorecen más.


<h1>Archivos y funcionamiento</h1>
  
* ```main.py```: Archivo principal que se ejecuta y en la que importando las clases Game y Synth se pueden implementar los algoritmos que se deseen para entrenar el comportamiento de los Syths.<br>
    * ```evaluate_synth()```: Función que evalua en cada ciclo, para cada individuo (según los parametros entregados, que son principalmente el rango de visión del individuo y posición) las acciones a realizar, que se incluyen más abajo en ```Main synth's methods```. 
* ```Game```<br>
    * ```Game.py```: Clase que contiene los atributos y funciones del juego, renderizado y parametros globales. Cuando se llama Game.run() simula el juego y retorna la lista de individuos supervivientes en cada iteración. Entre los parametros más importantes se incluyen la lista de individuos y la función de evaluación que evalua el comportamiento en cada ciclo.<br>
      * ```run()```: Función que simula un juego, toma como parametro una función evaluadora, junto con una lista de individuos (Instancias de la clase Synth) y retorna una lista de individuos con sus puntajes correspondientes.
* ```Synth```<br>
    * ```Synth.py```: Clase que representa a los individuos participantes en la simulación, con sus acciones y parametros.<br>
* ```genetic_model```<br>
   * ```genetic_model.py```: Archivo que contiene funciones utilizables para el modelo genético de ejemplo.<br>
* ```data.csv```: Donde se almacenan los datos del juego para futuros analisis y predicciones.<br>
<h1>Synth</h1>
Synth es el nombre que se le da a los individuos en la simulación y que tienen un comportamiento programable para hacer lo que sea en su contexto (Por ejemplo seguir a otros synths, disparar a un synth a cierta distancia al detectarlo o evitar a cualquier individuo al detectarlo). Todos cuentan con cualidades como vida, que al agotarse mueren o munición.<br>
<h2>Sistema de detección</h2>
También tienen un sistema de detección basado en rangos. Si un synth está en alguno de los rangos, se actualiza la lista que contiene las distancias de los synths (obtenible con get_senseDataBuffer() ), Esta lista tiene elementos que representan distancias y tiene tantos elementos como quepan según el ángulo de detección que tenga, cuanto mayor sea el ángulo más parametros tendrá la matriz de detección, que luego se puede utilizar para tomar desiciones.<br><br>

![img](https://github.com/MartinCastillo/IA-Royale/blob/master/captures/5.PNG)<br><br>
![img](https://github.com/MartinCastillo/IA-Royale/blob/master/captures/6.PNG)

<h2>Parametros y atributos de la clase Synth (Todos accedibles desde la función evaluadora)</h2>
  
Needed:<br>
  * coords((x,y) tuple).
  
Optional:<br>
  * lineal_speed(default 8): Speed of movement.
  * rotation_speed(default 8): Speed of rotation.
  * damage_power(default 70): Damage when hit someone.
  * ammo(default 20): If they kill can get rewards in ammo.
  * health(default 100): If they get shot they loose health.
  * shooting_range(default 100): In pixels is the range of the shot.
  * controllable(default False): If its true the synth respons to the keyboard.
  * shooting_timer_max(default 5): Cuanto mayor sea, mas largo es el disparo.
  * delta_angle(default 20): Is the length in degres of the ranges of detecton,
  where place the detected enemies, _sense_data_buffer will have a 360.
  * _weights: Contains the setteable weights for nn

Main synth´s methods:
  * move_forward() move_backwards(),turn_left(),turn_right(): Move the synth.
  * shoot(): Activate the state of shoot, that has to decrease.
  * get_senseDataBuffer(): Get _sense_data_buffer that is a list that contains the
  distances of detected enemies in ranges, if more than two enemies are in the same
  range is used the nearest, if in the range are no enemies the range has False.
  * set_weights(): Get _weights atribute.
  * get_weights(weights) Set _weights atribute.
  * get_kills(): Get kills that the individual has done.
  * set_controllable(bool): Sets the controllable atribute.
  * restore_stats(): Restore health and ammo to its starting points.

<h1>Capturas</h1>
  
  ![img](https://github.com/MartinCastillo/IA-Royale/blob/master/captures/1.PNG)
  ![img](https://github.com/MartinCastillo/IA-Royale/blob/master/captures/2.PNG)
  ![img](https://github.com/MartinCastillo/IA-Royale/blob/master/captures/3.PNG)
  ![img](https://github.com/MartinCastillo/IA-Royale/blob/master/captures/4.PNG)
