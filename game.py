import pgzrun

game_state = 'menu'




class Animation:
    def __init__(self, frames, speed=0.2):
        self.frames = frames
        self.speed = speed
        self.current_frame = 0
        self.timer = 0
        
    def update(self, dt):
        self.timer += dt
        if self.timer >= self.speed:
            self.timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
    
    def get_current_image(self):

        return self.frames[self.current_frame]
    
walk_anim = Animation(["player_walk1", "player_walk2"], speed=0.15)
player = Actor(walk_anim.get_current_image())
player.x = 400
player.y = 300

def draw():
    screen.fill((20, 20, 30))
    
    if game_state == 'menu':
        screen.draw.text('ZOMBIE APOCALYPSE', center = (400, 150),fontname = 'bloody', fontsize = 60, color = 'red' )
        screen.draw.text('Press ENTER to start', center = (400, 300), fontsize = 30, color = 'white' )
        screen.draw.text('If you scared press ESC to exit', center = (400, 500), fontsize = 20, color = 'gray' )
        
    elif game_state == 'game':
        screen.draw.text('Game running', center = (50, 20), fontsize = 20, color = 'green' )

def on_key_down(key):
    global game_state
    
    if game_state == 'menu':
        if key == keys.RETURN:
            game_state = 'game'
        elif key == keys.ESCAPE:
            exit()
            
    elif game_state == 'game':
        if key == keys.ESCAPE:
            game_state = 'menu'
            
pgzrun.go()

class Player:
    #TODO how plater can move speed and checking borders of map
    # coursor there is where w shot player still shooting
    # can heal get some hp from floor
    pass

class Zombie:
    #TODO randomize of  moving zombie to catch player but have to make some wreid move random move for every one and sometimes dodges
    # about 40 zombies respown one stronger one have X2 hp and X1,3 of DMG
    pass


