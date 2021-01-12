import pygame
import math
import numpy as np
from random import choice

class Synth:
    """
    -------------------------------------------------------------------------------
    Params:
    Needed:
    -coords((x,y) tuple)
    Optional(optional parameters are setteable with set_all(**kargs)):
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
    -------------------------------------------------------------------------------
    Main synth´s methods:
    -render(window,**kargs): render synth in the window with params
    -move_forward() move_backwards(),turn_left(),turn_right(): move
    the synth acording to the speed,each frame
    -shoot():activate the state of shoot, that has to decrease
    -normalizate_shootingRange_position_angle(width,height): update 3 fratures
    of the synth, the counter of the shooting(if its 0 stops shooting),
    sets the position in the range of width and height,set angle
    betwen 0 and 360
    -check_keyboard(): update the movement of  the synth  with the keyboard if,
    is controllable
    -add_ammo(amount): add ammo to the synth, can be used as reward with kills
    -synth1.evaluate_shooting(synth2), if the synth1 is shooting and synth2 is in the
    way, decrease the health of synth2 and if is inferior to 0 syint2.is_alive()
    returns False
    -get_senseDataBuffer(): get _sense_data_buffer that is a list that contains the
    distances of detected enemies in ranges, if more than two enemies are in the same
    range is used the nearest
    -set_controllable(bool): sets the controllable atribute
    -set_model(),get_model(weights) set _model atribute
    -------------------------------------------------------------------------------
    """
    def __init__(self,coords,**kargs):
        self.set_all(**kargs)
        self._coords = coords
        pygame.font.init()
        self.font=pygame.font.Font('freesansbold.ttf', 9)
        self._sense_data_buffer = [False for x in range(360//self.delta_angle)]
        self._shooting_timer = 0
        self._kills = 0;
        self._model=None;
        self._alive = True
        self._ray_colition_point=None; #For rendering shooting ray, is the point were the ray colides

    def set_all(self,**kargs):
        self.name = kargs.get('name',None)
        if(self.name is None):#Por defecto nombre aleatorio
            self.name = ''.join(map(str, [choice('abcdefg') for _ in range(5)]))
        self.shooting_timer_max = kargs.get('shooting_timer_max',5)
        self.size = kargs.get('size',40)
        self.angle = kargs.get('angle',0)
        self.delta_angle = kargs.get('delta_angle',20) #Used for detecting the distances to enemies
        self.lineal_speed = kargs.get('lineal_speed',8)
        self.rotation_speed=kargs.get('rotation_speed',8)
        self.shooting_range=kargs.get('shooting_range',100)
        self.damage_power = kargs.get('damage_power',70)
        self.ammo = kargs.get('ammo',20)
        self.health=kargs.get('health',100)
        self.controllable=kargs.get('controllable',False)

    def x_y_components(self,module,angle):
        #Get x and y components of point with polar coordinates (module,angle)
        angle_to_rad = lambda a: a*math.pi/180
        dy=module*math.sin(angle_to_rad(angle))
        dx=module*math.cos(angle_to_rad(angle))
        return np.array([dx,dy])

    def render(self,window,**kargs):
        """
        Render synth in the given window
        ---------------------------------
        -Nedeed:
        window: window to render
        -Optional(boleans):
        render_text: render synth´s information over them (health,ammo,kills,name)
        render_synth_details: graphic details, like a marker if the synth is controllable or not
        just things for aesthetic
        render_rays: Render the rays when the synths shoot
        render_detection_ranges: render the lines that separate the ranges of detection used
        to get sense_data_buffer atribute of the synth
        ---------------------------------
        """
        if(kargs.get('render_detection_ranges',False)):
            for ray_number in range(360//self.delta_angle):
                #Resta delta_angle//2 para que un rango quede al frente
                ray_angle = self.angle+ray_number*self.delta_angle - self.delta_angle//2
                dxdy = self.x_y_components(self.shooting_range,ray_angle)
                pygame.draw.line(window,(223,192,100),self._coords,self._coords+dxdy,2)
        if(kargs.get('render_synth_details',True)):
            if(self.controllable):
                pygame.draw.circle(window,(51,49,84),self._coords,self.size,1)
            pygame.draw.circle(window,(173,59,85),self._coords,self.size//2)
            pygame.draw.circle(window,(38,39,45),self._coords,self.size//2,1)
            dxdy = self.x_y_components(self.size//2,self.angle)
            pygame.draw.line(window,(103,76,96),self._coords,(self._coords+dxdy),6)
        else:
            pygame.draw.circle(window,(38,39,45),self._coords,self.size//2,1)
        if(kargs.get('render_rays',True)):
            if(self._shooting_timer>0):
                #Si render_synth_details esta encendida aprovecha dxdy para el renderizado del laser
                dxdy_weapon = dxdy if (kargs.get('render_synth_details',True)) else 0
                dxdy_ray = self.x_y_components(self.shooting_range,self.angle)
                #_ray_colition_point es el punto en el que el rayo colisiona en el objetivo, si no colisiona es None
                #y por ende el rayo termina a una distanca normal
                if(self._ray_colition_point is not None):
                    ray_end_point=self._ray_colition_point
                else:
                    ray_end_point = self._coords+dxdy_ray
                pygame.draw.line(window,(178,0,27),self._coords+dxdy_weapon,ray_end_point,3)
        if(kargs.get('render_text',False)):
            text_str = "''{}'' /Ammo: {} Health: {}/Kills: {}".format(self.name,self.ammo,
                int(self.health),self._kills
                )
            text = self.font.render(text_str,True, (255,182,138), (38,39,45))
            text_w,text_h = self.font.size(text_str)
            window.blit(text, self._coords-[text_w//2,(text_h+self.size//2)])

    #Movement functions
    def move_forward(self):
        self._coords += self.x_y_components(self.lineal_speed,self.angle).astype(int)
    def move_backwards(self):
        self._coords -= self.x_y_components(self.lineal_speed,self.angle).astype(int)
    def turn_right(self):
        self.angle += self.rotation_speed
    def turn_left(self):
        self.angle -= self.rotation_speed
    def turn_left_forward(self):
        turn_left() ; move_forward()
    def turn_right_forward(self):
        turn_right() ; move_forward()
    def shoot(self):
        #Set _shooting_timer to its heiger value (shooting_timer_max) decrease with
        #update_shooting_range,(and normalizate_shootingRange_position_angle)
        if(self.ammo>0):
            self._shooting_timer = self.shooting_timer_max
            self.ammo-=1
            return True
        return False
    def check_keyboard(self):
        #update synth position with keyboard
        if(self.controllable):
            keys=pygame.key.get_pressed()
            if(keys[pygame.K_UP]):
                self.move_forward()
            if(keys[pygame.K_DOWN]):
                self.move_backwards()
            if(keys[pygame.K_RIGHT]):
                self.turn_right()
            if(keys[pygame.K_LEFT]):
                self.turn_left()
            if(keys[pygame.K_q]):
                self.shoot()

    #normalizate functions
    def update_shooting_range(self):
        if(self._shooting_timer):
            self._shooting_timer-=1
    def set_position_in_range(self,width,height):
        #Se obtine el módiulo, para que si se pasa aparezca del otro lado
        self._coords = np.array([self._coords[0]%width,self._coords[1]%height])
    def set_angle_in_range(self):
        #Mantine ángulo de synth entre 0 y 360
        self.angle=self.angle%360
    def normalizate_shootingRange_position_angle(self,width,height):
        #set_position_in_range,update_shooting_range and set_angle_in_range in a single function
        self.set_position_in_range(width,height)
        self.update_shooting_range()
        self.set_angle_in_range()

    #Getters setters
    def set_controllable(self,stat):
        self.controllable = stat
    def is_controllable(self):
        return self.controllable
    def get_size(self):
        return self.size
    def get_coords(self):
        return self._coords
    def set_coords(self,coords):
        self._coords = np.array(coords)
    def set_angle(self,angle):
        self.angle = angle
    def get_senseDataBuffer(self):
        return self._sense_data_buffer
    def get_shootingRange(self):
        return self.shooting_range
    def get_name(self):
        return self.name
    def add_ammo(self,amount):
        self.ammo+=amount
    def add_kills(self,amount):
        self._kills+=amount
    def get_kills(self):
        return self._kills
    def set_model(self,model):
        self._model=model
    def get_model(self):
        return self._model

    #Shooting functions
    def checkCollision(self,P1,P2,Q,r):
        #Sheck if given two points and a circunference (centre, radius) the segment betwen the two
        #points intercects the circunference, and if it does return the pint in the circunference
        #that colide, otherwise instead of a point retuns None
        V = P2-P1
        a = V.dot(V)
        b = 2 * V.dot(P1 - Q)
        c = P1.dot(P1) + Q.dot(Q) - 2 * P1.dot(Q) - r**2
        disc = b**2 - 4 * a * c
        if disc < 0:
            return False,None
        sqrt_disc = math.sqrt(disc)
        t1 = (-b + sqrt_disc) / (2 * a)
        t2 = (-b - sqrt_disc) / (2 * a)
        if not((0 <= t1 <= 1) or (0 <= t2 <= 1)):
            return False,None
        t = max(0, min(1, - b / (2 * a)))
        return True,P1 + t * V

    def evaluate_shooting(self,target):
        #If the instance that execute this function is succesfully shooting (_shooting_timer>0)
        #and the target, another instance, is in the way, target is gets hurt (target.get_hurt())
        #cant shoot itself (target!=self)
        if(self._shooting_timer>0)and(target!=self):
            p1 = self._coords
            p2 = self.x_y_components(self.shooting_range,self.angle)+p1
            q = target.get_coords()
            r = target.get_size()/2
            is_colision,_ray_colition_point = self.checkCollision(p1,p2,q,r)
            self._ray_colition_point = _ray_colition_point #used in render
            if(is_colision):
                target.get_hurt(self.damage_power/self.shooting_timer_max)
    def get_hurt(self,damage):
        self.health -= damage
        if(self.health<=0):
            self._alive=False
    def is_alive(self):
        return self._alive

    #_sense_data_buffer functions
    def update_sense_data_buffer(self,synt2):
        #Añade la distanca a synt2, en uno de (360/delta_angle-1) rangos si es menor,
        #según el angulo relativo de synt2 a este synth,cada iteración se deberia ocupar
        #restart_sense_data_buffer() para evitar usar detecciones de iteraciones antiguas
        #el resultado se refleja en  sense_data_buffer
        synth2_coords = synt2.get_coords()
        vector_betwen = synth2_coords - self._coords#Vector de este synth al otro
        distance = math.hypot(vector_betwen[0],vector_betwen[1])
        #Le resta delta_angle//2 para que uno de los rangos quede al frente
        theta = 180*math.atan2(vector_betwen[1],vector_betwen[0])/math.pi-self.delta_angle/2
        angle_ray = (self.angle - theta)%360
        #edondea hacia abajo
        range_index = int(angle_ray/self.delta_angle)
        if(int(angle_ray)==360):
            range_index-=1
        if(self._sense_data_buffer[range_index]<distance):
            self._sense_data_buffer[range_index]=distance

    def restart_sense_data_buffer(self):
        #Set _sense_data_buffer all to False
        self._sense_data_buffer =  [False for x in range(360//self.delta_angle)]
