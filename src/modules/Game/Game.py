import pygame
import numpy as np
class Game:
    def __init__(self,**kargs):
        """
        All settealbe with set_all(**kargs)
        --------------------------------------------------------------------------------
        -General configurations (setteable with set_general_configuration(**kargs) ):
        °ammo_reward (default 0) = (int) reward given to a synth if kills someone, in ammo.
        °area_reduction_delay(default False) =(int) The smaller, the fastest the area reduces its size.
        °starting_map_size ((x,y), tuple): starting map size.
        °map_min_size (default map_size/3) = (x,y) int tuple, minimum of the map´s size.
        °population_reduction_fraction (default 0.5) = proportion of synths alive to quit the game.
        °prompt_messages(default False) = if its true prompt in terminal messages like kills or
        number of synths alive.
        --------------------------------------------------------------------------------
        -Render configurations (boleans) (set_render_configuration(**kargs) ):
        °render(default True) : if its true render the game
        °render_text (default True): render synth´s information over them (health,ammo,kills,name).
        °render_synth_details (default True): graphic details, like a marker if the synth is
        controllable or not just things for aesthetic.
        °render_rays (default True): Render the rays when the synths shoot.
        °render_detection_ranges (default False): render the lines that separate the ranges of
        detection used to get sense_data_buffer atribute of the synth.
        --------------------------------------------------------------------------------
        """
        self.set_all(**kargs)
        self._map_size = self.starting_map_size
        self._run_counter = 1 #Counter of game cycles
        pygame.font.init()
        pass
    def set_general_configuration(self,**kargs):
        #General configuration
        self.render = kargs.get('render',True)
        self.ammo_reward = kargs.get('ammo_reward',0)
        self.starting_map_size = np.array(kargs.get('starting_map_size',(600,600)))
        self.area_reduction_delay = kargs.get('area_reduction_delay',False)
        self.map_min_size = kargs.get('map_min_size',self.starting_map_size//3)
        self.population_reduction_fraction = kargs.get('population_reduction_fraction',0.5)
        self.prompt_messages = kargs.get('prompt_messages',False)
    def set_render_configuration(self,**kargs):
        #Render configuration
        self.render = kargs.get('render',True)
        self.render_text = kargs.get('render_text',True)
        self.render_synth_details = kargs.get('render_synth_details',True)
        self.render_rays = kargs.get('render_rays',True)
        self.render_detection_ranges = kargs.get('render_detection_ranges',False)
    def set_all(self,**kargs):
        self.set_render_configuration(**kargs)
        self.set_general_configuration(**kargs)


    def render_game(self,window,synths,text_str=None):
        """
        ---------------------------------
        -Needed:
        °window: window to render
        °_map_size: limited area´s rectangle
        °synths: synth's list to render
        -Optional:
        °text_str: text to print int the screen corner
        -Configurations (boleans) (setteable with  the set_render_configuration()):
        °render_text: render synth´s information over them (health,ammo,kills,name)
        °render_synth_details: graphic details, like a marker if the synth is
        controllable or not just things for aesthetic
        °render_rays: Render the rays when the synths shoot
        °render_detection_ranges: render the lines that separate the ranges of
        detection used to get sense_data_buffer atribute of the synth
        ---------------------------------
        """
        #Background and synths
        window_size = np.array(window.get_size())
        map_size = np.array(self._map_size)
        pygame.draw.rect(window,(156,69,68),(0,0,*map_size))
        for synth in synths:
            synth.render(window,render_detection_ranges=self.render_detection_ranges,render_synth_details=
                self.render_synth_details,render_rays=self.render_rays,render_text=self.render_text)
        #Rectangle
        pygame.draw.rect(window,(106,29,47),(0,map_size[0],*window_size))
        pygame.draw.rect(window,(106,29,47),(map_size[1],0,map_size[0],window_size[1]))
        pygame.draw.rect(window,(38,39,45),(0,0,*map_size),2)
        #Text
        if(text_str is not None):
            tamaño = 7*(window_size[0]//100)
            font = pygame.font.Font('freesansbold.ttf', tamaño)
            #text = font.render(text,True, (255,182,138), (38,39,45))
            text = font.render(text_str,True,(88,0,0),(255,64,64))
            text_size = font.size(text_str)
            window.blit(text, window_size-text_size)
        #Evalua si debe sacar el juego
        pygame.time.Clock().tick(27)
        pygame.display.update()
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self._run_counter = 0

    def update_synths(self,synths,behavioral_function):
        (width,height) = self._map_size
        #Update the state of each synth, controls its behave, if live or die, interactions
        #via keyboard update te sense_data_buffer of each synth and apply
        #normalizate_shootingRange_position_angle for keeping synth angle betwen 0 and 360
        #and its position in te area limit
        """Bucle entre pares de synth, donde se aplican relaciones como matar o detectar distancias"""
        killed_counter = 0
        for sx,synth in enumerate(synths):
            synth.normalizate_shootingRange_position_angle(width,height)
            synth.restart_sense_data_buffer()
            for tx,target in enumerate(synths):
                if(tx!=sx):
                    #Evaluate detecton of target by synth
                    synth.update_sense_data_buffer(target)
                    #Evaluate if synth killed target
                    synth.evaluate_shooting(target)
                    if(not target.is_alive())and(target in synths):
                        killed_counter+=1
                        synths.remove(target)
                        synth.add_ammo(self.ammo_reward)
                        synth.add_kills(1)
                        if(self.prompt_messages):
                            print("{} was killed / {} alive".format(target.name,len(synths)))
            if(self.render):
                synth.check_keyboard()
            """Here is declared the behave of the synth"""
            behavioral_function(synth)
        return synths

    def run(self,synths,behavioral_function,render=None,text=None):
        """
        --------------------------------------------------------------------------------
        Takes a list of synths and a behavioral_function and runs the game, return the
        winer-winers or survivor-survivors, and a bolean that indicate if the program
        clossed normally.
        -Needed:
        °synths = Synth object list.
        °behavioral_function = Actions that each synth do every cycle(e.g the ia) when
        its called recive a Synth object as parameter.
        -Optional:
        °render (default True) : if its true render the game
        --------------------------------------------------------------------------------
        """
        self._map_size = self.starting_map_size.copy()
        if(render is not None):
            self.render = render
        starting_population_size = len(synths)
        if(self.render):
            window = pygame.display.set_mode(self._map_size)
            pygame.display.set_caption("IA-Royale")
            pygame.time.Clock()
            pygame.init()
        #main loop
        self._run_counter = 1
        while self._run_counter:
            self._run_counter+=1
            #Behave
            synths_alive = self.update_synths(synths=synths,behavioral_function=behavioral_function)
            if(self.render):
                self.render_game(window,synths,text)
            #Reducir area
            if(self.area_reduction_delay):
                if(self._run_counter%self.area_reduction_delay==0)and(self._map_size>self.map_min_size).any():
                    self._map_size-=1
            if(len(synths)/starting_population_size<=self.population_reduction_fraction):
                break
        pygame.quit()
        if(self._run_counter==0):
            return synths_alive,False
        return synths_alive,True
