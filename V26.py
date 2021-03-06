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
        self.walls=walls()

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
            self.walls.load_wall(window,self.user,self.bullet,self.enemy)

        #Starts the movement
        enemy_list=self.enemy.get_enemies()
        enemies=enemy_list[0]
        enemy_turrets = enemy_list[1]
        #Goes through every enemy to send into the move enemy and fireback methods
        for number in range(4):
            enemy_sprite=enemies[number]
            enemy_turret_sprite=enemy_turrets[number]
            self.enemy.move_enemy(window,self.user,self.bullet,enemy_sprite,enemy_turret_sprite)
            self.enemy.fire_back(window,self.user,self.bullet,enemy_sprite,enemy_turret_sprite)


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
        self.bullet_image.width = 14
        self.bullet_image.height = 22
        self.bullet_image.anchor_x = self.bullet_image.width / 2
        self.bullet_image.anchor_y = 0
        self.speed = 500

        self.bullet_batch = pyglet.graphics.Batch()
        self.bullet_no = -1
        self.bullets = []
        self.new_bullet = pyglet.sprite.Sprite(self.bullet_image, -50, -50, batch=self.bullet_batch)

    def shoot(self):
        self.bullet_no += 1
        self.bullets.append(pyglet.sprite.Sprite(self.bullet_image, -50, -50, batch=self.bullet_batch))
        self.bullet_batch.draw()
        return(self.bullets[self.bullet_no])

    def load_bullet(self,window,user,enemy):
        self.shoot()
        #Shooting
        @window.event
        def on_mouse_press(x, y, button, modifiers):
            if button == mouse.RIGHT:
                current_bullet = bullet.shoot(self)
                positions = user.get_position()
                tank_sprite_x=positions[0]
                tank_sprite_y = positions[1]
                current_bullet.x = tank_sprite_x
                current_bullet.y = tank_sprite_y
                bullet_x = current_bullet.x
                bullet_y = current_bullet.y
                mouse_x = x
                mouse_y = y
                x_length = mouse_x - bullet_x
                y_length = mouse_y - bullet_y
                #Bullet rotation
                if x_length > 0:
                    angle = math.degrees(math.atan(y_length / x_length))
                    angle = 90 - angle
                    current_bullet.rotation = angle
                else:
                    angle = math.degrees(math.atan(y_length / x_length))
                    angle = 270 - angle
                    current_bullet.rotation = angle
                #Bullet movement
                def update(dt):
                    rad = math.radians(current_bullet.rotation)
                    cosAngle = math.cos(rad)
                    sinAngle = math.sin(rad)
                    current_bullet.y += cosAngle * self.speed * dt
                    current_bullet.x += sinAngle * self.speed * dt
                    position_array = [current_bullet.x, current_bullet.y, current_bullet]
                    enemy.collision(position_array)
                pyglet.clock.schedule_interval(update, 1 / 60.0)

#ENEMY CLASS
class enemy:
    def __init__(self):
        #Creates 1 tank
        self.enemy_image = pyglet.resource.image("enemy.png")
        self.enemy_image.width = 100
        self.enemy_image.height = 100
        self.enemy_image.anchor_x = self.enemy_image.width / 2
        self.enemy_image.anchor_y = self.enemy_image.height / 2
        self.enemy_batch = pyglet.graphics.Batch()
        self.enemies = []
        self.enemy_sprite = pyglet.sprite.Sprite(self.enemy_image, -50, -50, batch=self.enemy_batch)
        #Creates 4 tanks to use
        self.enemies.append(pyglet.sprite.Sprite(self.enemy_image, 190, 75, batch=self.enemy_batch))
        self.enemies.append(pyglet.sprite.Sprite(self.enemy_image, 190, 645, batch=self.enemy_batch))
        self.enemies.append(pyglet.sprite.Sprite(self.enemy_image, 579, 70, batch=self.enemy_batch))
        self.enemies.append(pyglet.sprite.Sprite(self.enemy_image, 574, 645, batch=self.enemy_batch))
        #Creates 1 turret
        self.enemy_turret_image = pyglet.resource.image("enemy_turret.png")
        self.enemy_turret_image.width = self.enemy_image.width / 3
        self.enemy_turret_image.height = (self.enemy_image.height / 3) * 2
        self.enemy_turret_image.anchor_x = self.enemy_turret_image.width / 2
        self.enemy_turret_image.anchor_y = self.enemy_turret_image.height - 15
        self.enemy_turret_batch = pyglet.graphics.Batch()
        self.enemy_turrets = []
        self.enemy__turret_sprite = pyglet.sprite.Sprite(self.enemy_turret_image, x=self.enemy_sprite.x, y=self.enemy_sprite.y, batch=self.enemy_turret_batch)
        #Creates 4 turrets to use
        self.enemy_turrets.append(pyglet.sprite.Sprite(self.enemy_turret_image,x=self.enemies[0].x, y=self.enemies[0].y, batch=self.enemy_turret_batch))
        self.enemy_turrets.append(pyglet.sprite.Sprite(self.enemy_turret_image,x=self.enemies[1].x, y=self.enemies[1].y, batch=self.enemy_turret_batch))
        self.enemy_turrets.append(pyglet.sprite.Sprite(self.enemy_turret_image,x=self.enemies[2].x, y=self.enemies[2].y, batch=self.enemy_turret_batch))
        self.enemy_turrets.append(pyglet.sprite.Sprite(self.enemy_turret_image,x=self.enemies[3].x, y=self.enemies[3].y, batch=self.enemy_turret_batch))

        self.explode_image = pyglet.resource.image("explode.png")
        self.explode_image.width = 150
        self.explode_image.height = 150
        self.explode_image.anchor_x = self.explode_image.width / 2
        self.explode_image.anchor_y = self.explode_image.height / 2
        self.explode = pyglet.sprite.Sprite(self.explode_image, x=1280 / 5, y=720 / 5)
        self.explode.visible = False

        self.tank_speed=4
        self.bullet_speed=200

    def load_enemy(self,window,user,bullet):
        self.enemy_batch.draw()
        self.enemy_turret_batch.draw()
        self.explode.draw()
        for number in range(4):
            enemy_sprite=self.enemies[number]
            enemy_turret_sprite = self.enemy_turrets[number]
            positions = user.get_position()
            turret_x = enemy_turret_sprite.x
            turret_y = enemy_turret_sprite.y
            tank_sprite_x = positions[0]
            tank_sprite_y = positions[1]
            x_length = tank_sprite_x - turret_x
            y_length = tank_sprite_y - turret_y
            if x_length > 0:
                angle = math.degrees(math.atan(y_length / x_length))
                angle = 270 - angle
                enemy_turret_sprite.rotation = angle
            else:
                angle = math.degrees(math.atan(y_length / x_length))
                angle = 90 - angle
                enemy_turret_sprite.rotation = angle

    def move_enemy(self,window,user,bullet,enemy_sprite,enemy_turret_sprite):
        #Sends each enemy into this function
        def tank_move(dt, enemy_sprite,value,direction,enemy_turret_sprite):
            #Moves enemy left or right
            if direction=="y":
                enemy_sprite.y += value
                enemy_turret_sprite.y+=value
            elif direction=="x":
                enemy_sprite.x += value
                enemy_turret_sprite.x += value
            #Checks if it has met a corner
            if enemy_sprite.x<=190 and enemy_sprite.y>=659: # Turn right
                #Ends the up movement and starts going right
                pyglet.clock.unschedule (tank_move)
                pyglet.clock.schedule_interval(tank_move, 1 / 60, enemy_sprite, self.tank_speed, "x", enemy_turret_sprite)
                #Changes direction to right
                enemy_sprite.rotation = 90
            if enemy_sprite.x>=574 and enemy_sprite.y>=659: # Turn down
                pyglet.clock.unschedule (tank_move)
                pyglet.clock.schedule_interval(tank_move, 1 / 60, enemy_sprite, -1 * self.tank_speed, "y",enemy_turret_sprite)
                enemy_sprite.rotation = 180
            if enemy_sprite.x>=574 and enemy_sprite.y<=75: # Turn left
                pyglet.clock.unschedule (tank_move)
                pyglet.clock.schedule_interval(tank_move, 1 / 60, enemy_sprite, -1 * self.tank_speed, "x", enemy_turret_sprite)
                enemy_sprite.rotation = 270
            if enemy_sprite.x<=190 and enemy_sprite.y<=75: #Turn up
                pyglet.clock.unschedule (tank_move)
                pyglet.clock.schedule_interval(tank_move, 1 / 60, enemy_sprite, self.tank_speed, "y",enemy_turret_sprite)
                enemy_sprite.rotation=0
        pyglet.clock.schedule_interval(tank_move, 1/60, enemy_sprite, self.tank_speed, "y",enemy_turret_sprite)

    def fire_back(self,window,user,bullet,enemy_sprite,enemy_turret_sprite):
        def fire(dt):
            current_bullet = bullet.shoot()
            positions = user.get_position()
            current_bullet.x = enemy_sprite.x
            current_bullet.y = enemy_sprite.y
            bullet_x = current_bullet.x
            bullet_y = current_bullet.y
            tank_sprite_x = positions[0]
            tank_sprite_y = positions[1]
            x_length = tank_sprite_x - bullet_x
            y_length = tank_sprite_y - bullet_y
            # Bullet rotation
            if x_length > 0:
                angle = math.degrees(math.atan(y_length / x_length))
                angle = 90 - angle
                current_bullet.rotation = angle
            else:
                angle = math.degrees(math.atan(y_length / x_length))
                angle = 270 - angle
                current_bullet.rotation = angle
            # Bullet movement
            def update(dt):
                rad = math.radians(current_bullet.rotation)
                cosAngle = math.cos(rad)
                sinAngle = math.sin(rad)
                current_bullet.y += cosAngle * self.bullet_speed * dt
                current_bullet.x += sinAngle * self.bullet_speed * dt
                position_array = [current_bullet.x, current_bullet.y, current_bullet]
                #enemy.collision(position_array)
            pyglet.clock.schedule_interval(update, 1 / 60.0)
        pyglet.clock.schedule_interval(fire, 3)


    def collision(self,positions):
        for number in range(4):
            enemy_sprite=self.enemies[number]
            enemy_turret_sprite = self.enemy_turrets[number]
            bullet_sprite_x=positions[0]
            bullet_sprite_y=positions[1]
            bullet_sprite=positions[2]
            if (bullet_sprite_y < (enemy_sprite.y + (self.enemy_image.height / 2))) and (bullet_sprite_y > (enemy_sprite.y - (self.enemy_image.height / 2)))and (bullet_sprite_x < (enemy_sprite.x + (self.enemy_image.width/ 2))) and (bullet_sprite_x > (enemy_sprite.x - (self.enemy_image.width/ 2))):
                enemy_sprite.visible = False
                #self.enemy_turret_sprite.visible = False
                bullet_sprite.visible = False
                self.explode.x = enemy_sprite.x
                self.explode.y = enemy_sprite.y
                self.explode.visible = True

    def get_enemies(self):
        #Creates 2D array of lists to send back to gameplay
        enemy_list=[self.enemies,self.enemy_turrets]
        return (enemy_list)

#Walls CLASS
class walls:
    def __init__(self):
        self.wall_image = pyglet.resource.image("wall.png")
        self.wall_image.anchor_x = self.wall_image.width / 2
        self.wall_image.anchor_y = self.wall_image.height / 2

        self.wall_image.width = 20
        self.wall_image.height = 450
        self.wall_sprite_main1 = pyglet.sprite.Sprite(self.wall_image, x=300, y=360)
        self.wall_sprite_main2 = pyglet.sprite.Sprite(self.wall_image, x=1080, y=360)

        self.wall_image.width = 20
        self.wall_image.height = 240
        self.wall_image.anchor_x = 0
        self.wall_sprite_left1 = pyglet.sprite.Sprite(self.wall_image, x=500, y=360+100)
        self.wall_sprite_left2 = pyglet.sprite.Sprite(self.wall_image, x=500, y=360-100)
        self.wall_sprite_right1 = pyglet.sprite.Sprite(self.wall_image, x=1040, y=360+100)
        self.wall_sprite_right2 = pyglet.sprite.Sprite(self.wall_image, x=1040, y=360-100)
        self.wall_sprite_left1.rotation = 90
        self.wall_sprite_left2.rotation = 90
        self.wall_sprite_right1.rotation = 90
        self.wall_sprite_right2.rotation = 90

    def load_wall(self, window, user,bullet, enemy):
        self.wall_sprite_main1.draw()
        self.wall_sprite_main2.draw()
        self.wall_sprite_left1.draw()
        self.wall_sprite_left2.draw()
        self.wall_sprite_right1.draw()
        self.wall_sprite_right2.draw()


#RUNS gameplay
game=game_play()
game.window()
pyglet.app.run()

