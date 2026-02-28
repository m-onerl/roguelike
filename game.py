import pgzrun
import math

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
        self.anim_down = Animation(['player_walk1', 'player_walk2'], speed = 0.15)
        self.anim_up = Animation(['player_walk_back1', 'player_walk_back2'], speed = 0.15)
        self.anim_side_right = Animation(['player_walk_side_right1', 'player_walk_side_right2'], speed = 0.15)
        self.anim_side_left = Animation(['player_walk_side_left1', 'player_walk_side_left2'], speed = 0.15)
        
        self.neutral_down = "player_neutral"
        self.neutral_up = "player_neutral_back"
        self.neutral_side_left = "player_neutral_side_left"
        self.neutral_side_right = "player_neutral_side_right"
        
        self.current_anim = self.anim_down
        self.actor = Actor(self.neutral_down)
        self.actor.x = x
        self.actor.x = x
        self.actor.y = y
        self.speed = 5
        self.hp = 100
        self.max_hp = 100
        self.moving = False
        self.facing_right = True
        self.direction = "down"
        
        
    def update(self, dt):
        self.moving = False
        
        if keyboard.w:
            self.actor.y -= self.speed
            self.moving = True
            self.direction = "up"
            self.current_anim = self.anim_up
        if keyboard.s:
            self.actor.y += self.speed
            self.moving = True
            self.direction = "down"
            self.current_anim = self.anim_down
        if keyboard.a:
            self.actor.x -= self.speed
            self.moving = True
            self.direction = "left"
            self.current_anim = self.anim_side_left
        if keyboard.d:
            self.actor.x += self.speed
            self.moving = True
            self.direction = "right"
            self.current_anim = self.anim_side_right
        
        self.actor.x = max(20, min(WIDTH - 20, self.actor.x))
        self.actor.y = max(20, min(HEIGHT - 20, self.actor.y))
 
        if self.moving:
            self.current_anim.update(dt)
            self.actor.image = self.current_anim.get_current_image()
        else:
            if self.direction == "up":
                self.actor.image = self.neutral_up
            elif self.direction == "down":
                self.actor.image = self.neutral_down
            elif self.direction == "left":
                self.actor.image = self.neutral_side_left
            elif self.direction == "right":
                self.actor.image = self.neutral_side_right
    
            
    def draw(self):
        if self.facing_right:
            self.actor.draw()
        else:
            screen.blit(self.actor.image, (self.actor.x - self.actor.width//2, self.actor.y - self.actor.height//2))


player = Player(400, 300)

class Zombie:
    def __init__(self, x, y):
        self.anim_down = Animation(['zombie_walk1', 'zombie_walk2'], speed = 0.10)
        self.anim_up = Animation(['zombie_walk_back1', 'zombie_walk_back2'], speed = 0.10)
        self.anim_side_right = Animation(['zombie_walk_side_right1', 'zombie_walk_side_right2'], speed = 0.10)
        self.anim_side_left = Animation(['zombie_walk_side_left1', 'zombie_walk_side_left2'], speed = 0.10)
    
        self.courrent_anim = self.anim_down
        self.actor = Actor('zombie_walk1')
        self.actor.x = x 
        self.actor.y = y
        self.speed = 2
        self.hp = 50
        self.dmg = 10
        self.attack_cooldown = 0 
        self.attack_rate = 1.0 
    
    def update(self, dt, player):
        dx = player.actor.x - self.actor.x
        dy = player.actor.y - self.actor.y
        distance = math.sqrt(dx * dx + dy * dy)

        if self.attack_cooldown > 0 :
            self.attack_cooldown -= dt
            
        if distance < 40:
            self.attack(player)
        elif distance > 0:
            dx = dx / distance
            dy = dy / distance
            
            self.actor.x += dx * self.speed
            self.actor.y += dy * self.speed
            
            if abs(dx) > abs(dy):
                if dx > 0:
                    self.direction = "right"
                    self.current_anim = self.anim_side_right
                else:
                    self.direction = "left"
                    self.current_anim = self.anim_side_left
            else:
                if dy > 0:
                    self.direction = "down"
                    self.current_anim = self.anim_down
                else:
                    self.direction = "up"
                    self.current_anim = self.anim_up
            
            self.current_anim.update(dt)
            self.actor.image = self.current_anim.get_current_image()
    
    def attack(self, player):
        if self.attack_cooldown <= 0:
            player.hp -= self.damage
            self.attack_cooldown = self.attack_rate
            print(f"Zombie attacks! Player HP: {player.hp}")
    
    def draw(self):
        self.actor.draw()
        
zombies = [
    Zombie(100, 100),
    Zombie(700, 500),
    Zombie(700, 500),
]
                


def draw():
    screen.fill((20, 20, 30))
    
    if game_state == "menu":
        screen.draw.text('ZOMBIE APOCALYPSE', center = (400, 150),fontname = 'bloody', fontsize = 60, color = 'red' )
        screen.draw.text('Press ENTER to start', center = (400, 300), fontsize = 30, color = 'white' )
        screen.draw.text('If you scared press ESC to exit', center = (400, 500), fontsize = 20, color = 'gray' )
        
    elif game_state == "game":
        player.draw()
        for zombie in zombies:
            zombie.draw()
            
        screen.draw.filled_rect(Rect((10, 10), (200, 20)), 'darkred')
        hp_width = (player.hp / player.max_hp) * 200
        screen.draw.filled_rect(Rect((10, 10), (hp_width, 20)), 'red')
        screen.draw.text(f'HP: {player.hp}/{player.max_hp}', (15, 12), fontsize=16, color='white')
    
        
# function for update of animation
def update(dt):
    global game_state
    if game_state == "game":
        player.update(dt)
        for zombie in zombies:
            zombie.update(dt, player)
            
        if player.hp <= 0:
            game_state = "menu"
            player.hp = player.max_hp
            player.actor.x = 400
            player.actor.y = 300
            
def on_key_down(key):
    global game_state
    if game_state == "menu" and key == keys.RETURN:
        game_state = "game"
    elif key == keys.ESCAPE:
        game_state = "menu" if game_state == "game" else exit()
            
pgzrun.go()

