import sys, logging, os, random, math, open_color, arcade

#check to make sure we are running the right version of Python
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

#turn on logging, in case we have to leave ourselves debugging messages
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MARGIN = 30
SCREEN_TITLE = "Bullet exercise"

NUM_ENEMIES = 5
STARTING_LOCATION = (400,100)
BULLET_DAMAGE = 10
ENEMY_HP = 100
HIT_SCORE = 10
KILL_SCORE = 100

class Bullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        ''' 
        initializes the bullet
        Parameters: position: (x,y) tuple
            velocity: (dx, dy) tuple
            damage: int (or float)
        '''
        super().__init__("assets/bullet.png", 0.5)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage

    def update(self):
        '''
        Moves the bullet
        '''
        self.center_x += self.dx
        self.center_y += self.dy

class EnemyBullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        ''' 
        initializes the bullet
        Parameters: position: (x,y) tuple
            velocity: (dx, dy) tuple
            damage: int (or float)
        '''
        super().__init__("assets/bullet_enemy.png", 0.5)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage

    def update(self):
        '''
        Moves the enemy bullet
        '''
        self.center_x += self.dx
        self.center_y += self.dy


    
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/narwhal.png", 0.5)
        (self.center_x, self.center_y) = STARTING_LOCATION

class Enemy(arcade.Sprite):
    def __init__(self, position):
        '''
        initializes a penguin enemy
        Parameter: position: (x,y) tuple
        '''
        super().__init__("assets/penguin.png", 0.5)
        self.hp = ENEMY_HP
        (self.center_x, self.center_y) = position


        


class Window(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.set_mouse_visible(True)
        arcade.set_background_color(open_color.blue_4)
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.player = Player()
        self.score = 0
        self.timer = 0
        self.damage_indicator = " "
        self.damage_timer = 0

    def setup(self):
        '''
        Set up enemies
        '''
        for i in range(NUM_ENEMIES):
            x = 120 * (i+1) + 40
            y = 500
            enemy = Enemy((x,y))
            self.enemy_list.append(enemy)            

    def update(self, delta_time):
        self.bullet_list.update()
        self.enemy_bullet_list.update()
        self.player.update()
        #Extra credit one:
        if (len(self.enemy_list) == 0):
            exit()
        for e in self.enemy_list:
            # check for collision
            # check_for_collision_with_list registers hits many times from one bullet. This system only registers a hit once.
            for b in self.bullet_list:
                if (b.center_y == e.center_y + 5 and ((b.center_x >= e.center_x - 45) and (b.center_x <= e.center_x + 45))):
                    self.score += HIT_SCORE
                    e.hp -= BULLET_DAMAGE
                    if (e.hp <= 0):
                        e.kill()
                        self.score += KILL_SCORE

        #Coding enemy bullets. They will not fire if the player is killed.
        self.timer += 1
        if(self.timer > 60 and self.score >= 0):
            for e in self.enemy_list:
                x = e.center_x
                y = e.center_y - 15
                enemyBullet = EnemyBullet((x,y),(0,-10),BULLET_DAMAGE)
                self.enemy_bullet_list.append(enemyBullet)
            self.timer = 0
        #Coding the player damage
        for b in self.enemy_bullet_list:
                if (b.center_y == self.player.center_y + 5 and ((b.center_x >= self.player.center_x - 45) and (b.center_x <= self.player.center_x + 45))):
                    self.score -= HIT_SCORE * 3
                    self.damage_indicator = str(HIT_SCORE * -3)
                    self.damage_timer = 0
        self.damage_timer += 1
        if(self.damage_timer > 70):
            self.damage_indicator = " "
        #self.player.kill doesnt seem to work, so I kind of simulated it everywhere else
        if (self.score < 0):
            self.player.kill()
                


    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(str(self.score), 20, SCREEN_HEIGHT - 40, open_color.white, 16)
        #Added to simulate the kill() that won't work
        if(self.score >= 0):
            self.player.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()
        self.enemy_bullet_list.draw()
        arcade.draw_text(self.damage_indicator, self.player.center_x, 150, (255, 0, 0), 16)

    def on_mouse_motion(self, x, y, dx, dy):
        '''
        The player moves left and right with the mouse
        '''
        self.player.center_x = x

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and self.score >= 0:
            #fire a bullet
            x = self.player.center_x
            y = self.player.center_y + 15
            bullet = Bullet((x,y),(0,10),BULLET_DAMAGE)
            self.bullet_list.append(bullet)
            

def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()