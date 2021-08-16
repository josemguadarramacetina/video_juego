"""
 Platformer Game
"""
import arcade
 
# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

#Constant used to scale sprites from their original size
CHARACTER_SCALING=1.75
TILE_SCALING =0.35
COIN_SCALING =0.75


PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20

#How many pixels to keep as a minimum margin between the character
# and the edge of the screen
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # These are 'lists' that keep track of our srpites. Each srpit should go in a list
        self.coin_list = None
        self.wall_list = None
        self.player_list = None

        # Separate variable that holds the player sprite
        self.player_sprite = None
        #Our physics engine
        self.physics_engine =None
        
        #Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0
        #Keep track of the score
        self.score = 0
        
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        #Load sounds
        self.collect_coin_sound = arcade.load_sound(r"C:\Users\mnjos\proyectos\juego2\personajes\coin.wav")
        self.jump_sound = arcade.load_sound(r"C:\Users\mnjos\proyectos\juego2\personajes\jump.wav")

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        #Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        #Keep track of the score
        self.score = 0

        # Create the spirit lists       
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)

        # Set up the player, specifically placing it a these coordinates.
        image_source = r"C:\Users\mnjos\proyectos\juego2\personajes\Scientist_idle.png"
        self.player_sprite=arcade.Sprite(image_source,CHARACTER_SCALING)
        self.player_sprite.center_x=0
        self.player_sprite.center_y=120
        self.player_list.append(self.player_sprite)
        #Create the ground
        #This shows using a loop to place multiple sprites horizontally
        for x in range(0,250,64):
            wall=arcade.Sprite(r"C:\Users\mnjos\proyectos\juego2\personajes\grassMid2.png",1)
            wall.center_x=x
            wall.center_y=32
            self.wall_list.append(wall)
        #Put some crates on the ground
        #This shows using a coordinate list to place sprites
        coordinate_list=[[-16,96],
                         [256,96],
                         [512,96],
                         [768,96]]
        for coordinate in coordinate_list:
            #add a crate on the ground
            wall=arcade.Sprite(r"C:\Users\mnjos\proyectos\juego2\personajes\box_crate.png",TILE_SCALING)
            wall.position=coordinate
            self.wall_list.append(wall)


        #Use a loop to place some coins for our character

        for x in range(128,1250,256):
            coin = arcade.Sprite(r"C:\Users\mnjos\proyectos\juego2\personajes\Star_Coin.png",0.035)
            coin.center_x = x
            coin.center_y = 96
            self.coin_list.append(coin)
        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                         self.wall_list,
                                                         GRAVITY)
    def on_draw(self):
        """ Render the screen. """
        #Clear the screen to the background color
        arcade.start_render()
        # Code to draw the screen goes here
        #Draw your sprites
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()

        #Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.BLACK, 24)

    def on_key_press(self,key,modifiers):
        
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y=PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x=-PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED


    def on_key_release(self,key,modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self,delta_time):
        """Movement and game logic"""

        #Move the player with the physics engine
        self.physics_engine.update()

        #See if we hit any coins
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                             self.coin_list)
        for coin in coin_hit_list:
            #Remove the coin
            coin.remove_from_sprite_lists()
            #play sound
            arcade.play_sound(self.collect_coin_sound)
            #Add one to the score
            self.score += 1
            
        # -- Manage Scrolling ---
        # Track if we need to change the viewport

        changed = False
        #Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        #Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        #Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True


        #Scroll down
        bottom_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        if changed:
            #Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            #Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH +self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
