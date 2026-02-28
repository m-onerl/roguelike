import pgzrun

WIDTH = 800
HEIGHT = 600

game_state = 'menu'


class Animation:
    def __init__(self, frames, speed = 0.2):
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
    
    def reset(self):
        self.current_frame = 0
        self.timer = 0

 
class Player:
    def __init__(self, x, y):
        self.walk_anim = Animation(['player_walk1', 'player_walk2', 'player_walk3', 'player_walk4'], speed = 0.15)
        self.actor = Actor(self.walk_anim.get_current_image())
        self.actor.x = x
        self.actor.y = y
        self.speed = 5
        self.moving = False
        self.facing_right = True
    
    def update(self, dt):
        self.moving = False
        
        if keyboard.w:
            self.actor.y -= self.speed
            self.moving = True
        if keyboard.s:
            self.actor.y += self.speed
            self.moving = True
        if keyboard.a:
            self.actor.x -= self.speed
            self.moving = True
            self.facing_right = False
        if keyboard.d:
            self.actor.x += self.speed
            self.moving = True
            self.facing_right = True

        self.actor.x = max(20, min(WIDTH - 20, self.actor.x))
        self.actor.y = max(20, min(HEIGHT - 20, self.actor.y))
 
        if self.moving:
            self.walk_anim.update(dt)
            self.actor.image = self.walk_anim.get_current_image()

        if self.facing_right:
            self.actor.angle = 0
        else:
            self.actor.angle = 0  
            
    def draw(self):
        if self.facing_right:
            self.actor.draw()
        else:
            screen.blit(self.actor.image, (self.actor.x - self.actor.width//2, self.actor.y - self.actor.height//2))


player = Player(400, 300)

class Zombie:
    #TODO randomize of  moving zombie to catch player but have to make some wreid move random move for every one and sometimes dodges
    # about 40 zombies respown one stronger one have X2 hp and X1,3 of DMG
    pass



def draw():
    screen.fill((20, 20, 30))
    
    if game_state == 'menu':
        screen.draw.text('ZOMBIE APOCALYPSE', center = (400, 150),fontname = 'bloody', fontsize = 60, color = 'red' )
        screen.draw.text('Press ENTER to start', center = (400, 300), fontsize = 30, color = 'white' )
        screen.draw.text('If you scared press ESC to exit', center = (400, 500), fontsize = 20, color = 'gray' )
        
    elif game_state == 'game':
        screen.draw.text('Game running', center = (50, 20), fontsize = 20, color = 'green' )
        player.draw()
        
# function for update of animation
def update(dt):
    if game_state == "game":
        player.update(dt)
        
def on_key_down(key):
    global game_state
    if game_state == "menu" and key == keys.RETURN:
        game_state = "game"
    elif key == keys.ESCAPE:
        game_state = "menu" if game_state == "game" else exit()
            
pgzrun.go()
