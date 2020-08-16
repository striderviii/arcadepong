"""
PONG
"""
import arcade
import os
import math
import random
import time

game_folder = os.path.dirname(__file__)

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Pong"

BLACK = (0, 0, 0)

# Ball speed
velocity = 7

def getAsset(baseFolder, assetName):
    """
    Use double backspace for windows
    Enter entire folder directory after main directory

    """
    # Finds base directory of file
    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, baseFolder, assetName)
    # Returns directory path
    return img_folder

# Returns a random degree, includes the negative.
# Change range to effect angle of starting ball
def degree():
    return random.randrange(15, 45)

# Finds the y value to determine how the ball will choose an angle
def find_y(degree, velo_x):
    return round(math.tan(math.radians(degree)) * velo_x * flip_coin(), 1)

# Random chance generator to create a positive or negative number
def flip_coin():
    if random.choice([1, 2, 3, 4, 5, 6]) > 3:
        return -1
    else:
        return 1



class MyGame(arcade.Window):
    """ -------- Main Game Class -------"""

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # These are 'lists' that keep track of our sprites. Each sprite
        # should go into a list.

        self.ball_list = None

        self.paddle_list = None

        # Set background color

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        # Ball Attributes

        self.vel_x = None
        self.vel_y = None

    def paddle_setup(self, screen_pos):

        # Set up Player paddle
        # Top Half
        self.paddle_top = arcade.Sprite(game_folder + "\\paddle.png", .25)
        self.paddle_top.center_x = screen_pos

        top_hit_box_pointlist = [(-34.5,     -65), (34.5,    -65),
                                    (34.5, 209.0) ,(-34.5, 209.0)]

        self.top_hit_box = self.paddle_top.set_hit_box(top_hit_box_pointlist)

        # Bottom Half
        self.paddle_bottom = arcade.Sprite(game_folder + "\\paddle.png", .25)
        self.paddle_bottom.center_x = screen_pos

        bottom_hit_box_pointlist = [(-34.5, -209.0), (34.5, -209.0),
                                     (34.5,    65), (-34.5,   65)]

        self.bottom_hit_box = self.paddle_bottom.set_hit_box(bottom_hit_box_pointlist)
        self.paddle_list.append(self.paddle_top)
        self.paddle_list.append(self.paddle_bottom)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        # Set up ball start and direction

        ballAngle = degree() # Pulls random angle
        print(ballAngle)
        # Randomly decides which side to go

        self.vel_x = velocity * flip_coin()

        self.vel_y = find_y(ballAngle, self.vel_x) * flip_coin()

        # Create the sprite lists
        self.ball_list = arcade.SpriteList()
        self.paddle_list = arcade.SpriteList()

        self.player_paddle = self.paddle_setup(150)

        #ai_paddle = self.paddle_setup(850)








        # Set up ball
        self.ball = arcade.Sprite(game_folder + "\\ball.png", .25)
        self.ball.center_x = SCREEN_WIDTH//2
        self.ball.center_y = SCREEN_HEIGHT//2
        self.ball.change_x = self.vel_x
        self.ball.change_y = self.vel_y

        self.ball.set_hit_box(self.ball.get_hit_box())


        #self.paddle_list.append(self.paddle)
        self.ball_list.append(self.ball)

    def on_draw(self):
        # Clear the screen to the background color
        arcade.start_render()

        # Draw your sprite list
        self.ball_list.draw()
        self.paddle_list.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        # Connects mouse mothing to y value of paddle
        #self.paddle.change_y = y
        self.player_paddle.paddle_top.center_y = y
        #self.paddle_bottom.center_y = y

    def on_update(self, delta_time):

        # Moving ball
        self.ball_list.update()

        # Ball and wall collisions

        if self.ball.left < 0 or self.ball.right > SCREEN_WIDTH:
            self.ball.change_x = self.ball.change_x * -1

        if self.ball.bottom < 0 or self.ball.top > SCREEN_HEIGHT:
            self.ball.change_y = self.ball.change_y * -1


        paddle_speed = self.paddle_top.center_y - 325
        paddle_velocity = self.speed(paddle_speed, delta_time)
        #print(paddle_velocity)

        #print(self.ball.velocity)
        #print(math.dist(self.paddle.position, self.paddle.position))
        #x = delta_time
        #print(x)


        # Ball and paddle collisions
        if self.paddle_top.collides_with_sprite(self.ball) == True and self.paddle_bottom.collides_with_sprite(self.ball) ==True:
            self.ball.change_x = self.ball.change_x * -1
            print("HIT BOTH!")


        elif self.paddle_top.collides_with_sprite(self.ball) == True:
            self.ball.change_x = self.ball.change_x * -1
            if self.ball.change_y < 0:
                self.ball.change_y = self.ball.change_y * -1
            print("HIT TOP!")

        elif self.paddle_bottom.collides_with_sprite(self.ball) == True:
            self.ball.change_x = self.ball.change_x * -1
            if self.ball.change_y > 0:
                self.ball.change_y = self.ball.change_y * -1
            print("HIT BOTTOM!")




    def speed(self, end_point, delta_time):
        if end_point < 0:
            end_point = end_point * -1

        return round((end_point / delta_time) * .0001, 3)














        #print(None)

        #print(self.paddle.velocity)
        #print(self.ball.velocity)

        # x = self.paddle.get_hit_box()
        # print(x)












def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()