import pyglet
from pyglet.window import mouse
import math

#GAMEPLAY CLASS
class game_play:
    #Names all the other classes to refer back to them
    def __init__(self):
        self.user=user()
        self.bullet = bullet()
        self.enemy=enemy()

    #Creates the window
    def window(self):
        window = pyglet.window.Window(width=1280, height=720, fullscreen=False)
        cursor = window.get_system_mouse_cursor(window.CURSOR_CROSSHAIR)
        window.set_mouse_cursor(cursor)
        self.background=pyglet.image.load("background.jpg")
        self.background.width = 1280
        self.background.height = 720
        self.background_sprite=pyglet.sprite.Sprite(self.background)

        #Loads all 3 classes
        @window.event
        def on_draw():
            window.clear()
            self.background_sprite.draw()
            self.user.load_tank(window,self.bullet,self.enemy)
            self.bullet.load_bullet(window,self.user,self.enemy)
            self.enemy.load_enemy(window,self.user,self.bullet)

        #Starts the movement once
        self.enemy.move_enemy(window,self.user,self.bullet)


#USER CLASS
class user:
    def __init__(self):
        self.tank_image = pyglet.resource.image("tank.png")
        self.tank_image.width = 100
        self.tank_image.height = 100
        self.tank_image.anchor_x = self.tank_image.width / 2
        self.tank_image.anchor_y = self.tank_image.height / 2
        self.tank_sprite = pyglet.sprite.Sprite(self.tank_image, x=1280/ 2, y=720/ 2)

        self.turret_image = pyglet.resource.image("turret.png")
        self.turret_image.width = self.tank_image.width / 3
        self.turret_image.height = (self.tank_image.height / 3) * 2
        self.turret_image.anchor_x = self.turret_image.width / 2
        self.turret_image.anchor_y = self.turret_image.height - 15
        self.turret_sprite = pyglet.sprite.Sprite(self.turret_image, x=self.tank_sprite.x, y=self.tank_sprite.y)

        self.steps = 10

    def load_tank(self,window,bullet,enemy):
        self.tank_sprite.draw()
        self.turret_sprite.draw()

        #Tank Movement
        @window.event
        def on_text_motion(motion):
            if motion == pyglet.window.key.MOTION_DOWN:
                if self.tank_sprite.y>=(self.tank_image.height/2):
                    self.tank_sprite.y -=self.steps
                    self.tank_sprite.rotation=180
            elif (motion == pyglet.window.key.MOTION_UP):
                if self.tank_sprite.y<=720-(self.tank_image.height/2):
                    self.tank_sprite.y += self.steps
                    self.tank_sprite.rotation=0
            elif (motion == pyglet.window.key.MOTION_LEFT):
                if self.tank_sprite.x>=(self.tank_image.width/2):
                    self.tank_sprite.x -= self.steps
                    self.tank_sprite.rotation=270
            elif (motion == pyglet.window.key.MOTION_RIGHT):
                if self.tank_sprite.x<=1280-(self.tank_image.width/2):
                    self.tank_sprite.x +=  self.steps
                    self.tank_sprite.rotation=90
            self.turret_sprite.x = self.tank_sprite.x
            self.turret_sprite.y = self.tank_sprite.y

        #Turret Rotation
        @window.event
        def on_mouse_motion(x, y, dx, dy):
            turret_x = self.turret_sprite.x
            turret_y = self.turret_sprite.y
            mouse_x = x
            mouse_y = y
            x_length = mouse_x - turret_x
            y_length = mouse_y - turret_y
            if x_length > 0:
                angle = math.degrees(math.atan(y_length / x_length))
                angle = 270 - angle
                self.turret_sprite.rotation = angle
            else:
                angle = math.degrees(math.atan(y_length / x_length))
                angle = 90 - angle
                self.turret_sprite.rotation = angle

    #Collision Positions
    def get_position(self):
        position_array=[self.tank_sprite.x,self.tank_sprite.y,self.tank_sprite]
        return (position_array)

#BULLET CLASS
class bullet:
    def __init__(self):
        self.bullet_image = pyglet.resource.image("bullet.png")
        self.bullet_image.width = 28
        self.bullet_image.height = 45
        self.bullet_image.anchor_x = self.bullet_image.width / 2
        self.bullet_image.anchor_y = 0
        self.bullet_sprite = pyglet.sprite.Sprite(self.bullet_image, x=1280 / 2, y=(720 * 3) / 4)
        self.bullet_sprite.visible = False

        self.reset_speed=0

    def load_bullet(self,window,user,enemy):
        self.bullet_sprite.draw()

        #Shooting
        @window.event
        def on_mouse_press(x, y, button, modifiers):
            if button == mouse.RIGHT:
                self.bullet_sprite.visible = True
                positions = user.get_position()
                tank_sprite_x=positions[0]
                tank_sprite_y = positions[1]
                self.bullet_sprite.x = tank_sprite_x
                self.bullet_sprite.y = tank_sprite_y
                bullet_x = self.bullet_sprite.x
                bullet_y = self.bullet_sprite.y
                mouse_x = x
                mouse_y = y
                x_length = mouse_x - bullet_x
                y_length = mouse_y - bullet_y
                #Bullet rotation
                if x_length > 0:
                    angle = math.degrees(math.atan(y_length / x_length))
                    angle = 90 - angle
                    self.bullet_sprite.rotation = angle
                else:
                    angle = math.degrees(math.atan(y_length / x_length))
                    angle = 270 - angle
                    self.bullet_sprite.rotation = angle
                
                #Bullet movement
                if self.reset_speed==0:
                    def update(dt):
                        rad = math.radians(self.bullet_sprite.rotation)
                        cosAngle = math.cos(rad)
                        sinAngle = math.sin(rad)
                        self.bullet_sprite.y += cosAngle * 500*dt
                        self.bullet_sprite.x += sinAngle * 500*dt
                        self.reset_speed=self.reset_speed+1
                        position_array = [self.bullet_sprite.x, self.bullet_sprite.y, self.bullet_sprite]
                        enemy.collision(position_array)
                    pyglet.clock.schedule_interval(update, 1 / 60.0)
    
#ENEMY CLASS
class enemy:
    def __init__(self):
        self.enemy_image = pyglet.resource.image("enemy.png")
        self.enemy_image.width = 100
        self.enemy_image.height = 100
        self.enemy_image.anchor_x = self.enemy_image.width / 2
        self.enemy_image.anchor_y = self.enemy_image.height / 2
        self.enemy_sprite = pyglet.sprite.Sprite(self.enemy_image, x=1280 / 5, y=720 / 5)

        self.enemy_turret_image = pyglet.resource.image("enemy_turret.png")
        self.enemy_turret_image.width = self.enemy_image.width / 3
        self.enemy_turret_image.height = (self.enemy_image.height / 3) * 2
        self.enemy_turret_image.anchor_x = self.enemy_turret_image.width / 2
        self.enemy_turret_image.anchor_y = self.enemy_turret_image.height - 15
        self.enemy_turret_sprite = pyglet.sprite.Sprite(self.enemy_turret_image, x=self.enemy_sprite.x, y=self.enemy_sprite.y)

        self.explode_image = pyglet.resource.image("explode.png")
        self.explode_image.width = 150
        self.explode_image.height = 150
        self.explode_image.anchor_x = self.explode_image.width / 2
        self.explode_image.anchor_y = self.explode_image.height / 2
        self.explode = pyglet.sprite.Sprite(self.explode_image, x=1280 / 5, y=720 / 5)
        self.explode.visible = False

        self.count=0

    def load_enemy(self,window,user,enemy):
        self.enemy_sprite.draw()
        self.explode.draw()

    def move_enemy(self,window,user,enemy):
        def tank_move(dt, control,value,direction,turn):
            if direction=="y":
                control.y=control.y+ value
            elif direction=="x":
                control.x=control.x+ value
            self.count=self.count+1
            if turn=="Up":
                if self.count>100: # Turn Right
                    pyglet.clock.unschedule (tank_move)
                    self.count=0
                    pyglet.clock.schedule_interval(tank_move, 1/60, self.enemy_sprite, 2, "y","Right")
            elif turn=="Right":
                if self.count>100: # Turn Down
                    pyglet.clock.unschedule (tank_move)
                    self.count=0
                    pyglet.clock.schedule_interval(tank_move, 1/60, self.enemy_sprite, 2, "x","Down")
            elif turn=="Down":
                if self.count>100: # Turn Left
                    pyglet.clock.unschedule (tank_move)
                    self.count=0
                    pyglet.clock.schedule_interval(tank_move, 1/60, self.enemy_sprite, -2, "y","Left")
            elif turn=="Left":
                if self.count>100: #Turn Up
                    pyglet.clock.unschedule (tank_move)
                    self.count=0
                    pyglet.clock.schedule_interval(tank_move, 1/60, self.enemy_sprite, -2, "x","Up")

        pyglet.clock.schedule_interval(tank_move, 1/60, self.enemy_sprite, 1, "y","Right")

    def collision(self,positions):
        bullet_sprite_x=positions[0]
        bullet_sprite_y=positions[1]
        bullet_sprite=positions[2]
        if (bullet_sprite_y < (self.enemy_sprite.y + (self.enemy_image.height / 2))) and (bullet_sprite_y > (self.enemy_sprite.y - (self.enemy_image.height / 2)))and (bullet_sprite_x < (self.enemy_sprite.x + (self.enemy_image.width/ 2))) and (bullet_sprite_x > (self.enemy_sprite.x - (self.enemy_image.width/ 2))):
            self.enemy_sprite.visible = False
            bullet_sprite.visible = False
            self.explode.x = self.enemy_sprite.x
            self.explode.y = self.enemy_sprite.y
            self.explode.visible = True

#RUNS gameplay
game=game_play()
game.window()
pyglet.app.run()

