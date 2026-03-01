import pgzrun
import math

# window size
WIDTH = 800
HEIGHT = 600

# starting state of game 
game_state = 'menu'
music_on = True

# Menu buttons
btn_start = Rect((300, 250), (200, 50))
btn_music = Rect((300, 320), (200, 50))
btn_exit = Rect((300, 390), (200, 50))


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
    
    def reset(self):
        self.current_frame = 0
        self.timer = 0


class Weapon:
    def __init__(self, owner):
        self.owner = owner
        self.actor = Actor('baseball')
        self.angle = 0
        self.distance = 10  
        self.offset_y = -10
        self.is_swinging = False
        self.swing_speed = 600 
        self.swing_angle = 0
        self.swing_max = 360 
        self.damage = 25
        self.hit_zombies = []  
        
    def start_swing(self):
        if not self.is_swinging:
            self.is_swinging = True
            self.swing_angle = 0
            self.hit_zombies = []  
            try:
                sounds.swing.play()
            except:
                pass
    
    def update(self, dt):
        if self.is_swinging:

            self.swing_angle += self.swing_speed * dt
            if self.swing_angle >= self.swing_max:
                self.is_swinging = False
                self.swing_angle = 0
        
            rad = math.radians(self.swing_angle)
            self.actor.x = self.owner.actor.x + math.cos(rad) * self.distance
            self.actor.y = self.owner.actor.y + math.sin(rad) * self.distance
            self.actor.angle = -self.swing_angle + 90  
        else:

            self.actor.x = self.owner.actor.x
            self.actor.y = self.owner.actor.y + self.offset_y
            self.actor.angle = 30 
 
    def check_hit(self, zombies):
        if not self.is_swinging:
            return
        
        for zombie in zombies:
            if zombie in self.hit_zombies:
                continue 
                
            dx = self.actor.x - zombie.actor.x
            dy = self.actor.y - zombie.actor.y
            dist = math.sqrt(dx * dx + dy * dy)
            
            if dist < 10:  
                zombie.hp -= self.damage
                self.hit_zombies.append(zombie)
                try:
                    sounds.hit.play()
                except:
                    pass
    
    def draw(self):
        self.actor.draw()
 
class Player:
    def __init__(self, x, y):
        self.anim_down = Animation(['player/player_walk1', 'player/player_walk2'], speed=0.15)
        self.anim_up = Animation(['player/player_walk_back1', 'player/player_walk_back2'], speed=0.15)
        self.anim_side_right = Animation(['player/player_walk_side_right1', 'player/player_walk_side_right2'], speed=0.15)
        self.anim_side_left = Animation(['player/player_walk_side_left1', 'player/player_walk_side_left2'], speed=0.15)
        
        # using neutral + walk1 as frames
        self.idle_down = Animation(['player/player_neutral', 'player/player_walk1'], speed=0.6)
        self.idle_up = Animation(['player/player_neutral_back', 'player/player_walk_back1'], speed=0.6)
        self.idle_side_left = Animation(['player/player_neutral_side_left', 'player/player_walk_side_left1'], speed=0.6)
        self.idle_side_right = Animation(['player/player_neutral_side_right', 'player/player_walk_side_right1'], speed=0.6)
        
        self.current_anim = self.anim_down
        self.current_idle = self.idle_down
        self.actor = Actor('player/player_neutral')
        self.actor.x = x
        self.actor.y = y
        self.speed = 5
        self.hp = 100
        self.max_hp = 100
        self.moving = False
        self.direction = "down"

        self.weapon = Weapon(self)
        
    def attack(self):
        self.weapon.start_swing()
        
    def update(self, dt):
        self.moving = False
        
        if keyboard.w:
            self.actor.y -= self.speed
            self.moving = True
            self.direction = "up"
            self.current_anim = self.anim_up
            self.current_idle = self.idle_up
        if keyboard.s:
            self.actor.y += self.speed
            self.moving = True
            self.direction = "down"
            self.current_anim = self.anim_down
            self.current_idle = self.idle_down
        if keyboard.a:
            self.actor.x -= self.speed
            self.moving = True
            self.direction = "left"
            self.current_anim = self.anim_side_left
            self.current_idle = self.idle_side_left
        if keyboard.d:
            self.actor.x += self.speed
            self.moving = True
            self.direction = "right"
            self.current_anim = self.anim_side_right
            self.current_idle = self.idle_side_right
        
        self.actor.x = max(20, min(WIDTH - 20, self.actor.x))
        self.actor.y = max(20, min(HEIGHT - 20, self.actor.y))
 
        if self.moving:
            self.current_anim.update(dt)
            self.actor.image = self.current_anim.get_current_image()
        else:
            self.current_idle.update(dt)
            self.actor.image = self.current_idle.get_current_image()

        self.weapon.update(dt)
    
            
    def draw(self):
        self.actor.draw()
        self.weapon.draw()


player = Player(400, 300)


class Zombie:
    def __init__(self, x, y):
        self.anim_down = Animation(['enemy/zombie_walk1', 'enemy/zombie_walk2'], speed=0.10)
        self.anim_up = Animation(['enemy/zombie_walk_back1', 'enemy/zombie_walk_back2'], speed=0.10)
        self.anim_side_right = Animation(['enemy/zombie_walk_side_right1', 'enemy/zombie_walk_side_right2'], speed=0.10)
        self.anim_side_left = Animation(['enemy/zombie_walk_side_left1', 'enemy/zombie_walk_side_left2'], speed=0.10)
        
        # using existing walk frames
        self.idle_anim = Animation(['enemy/zombie_walk1', 'enemy/zombie_walk2'], speed=0.4)
    
        self.current_anim = self.anim_down
        self.actor = Actor('enemy/zombie_walk1')
        self.actor.x = x 
        self.actor.y = y
        self.radius = 30
        self.speed = 2
        self.hp = 50
        self.damage = 5
        self.attack_cooldown = 0 
        self.attack_rate = 0.5 
    
    def update(self, dt, target_player, all_zombies):
        dx = target_player.actor.x - self.actor.x
        dy = target_player.actor.y - self.actor.y
        distance = math.sqrt(dx * dx + dy * dy)

        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
            
        if distance < 30:
            self.attack(target_player)
            self.idle_anim.update(dt)
            self.actor.image = self.idle_anim.get_current_image()
        elif distance > 0:
            dx = dx / distance
            dy = dy / distance

            new_x = self.actor.x + dx * self.speed
            new_y = self.actor.y + dy * self.speed

            can_move = True
            for other in all_zombies:
                if other is self:
                    continue
                    
                dist_to_other = math.sqrt(
                    (new_x - other.actor.x) ** 2 + 
                    (new_y - other.actor.y) ** 2
                )
                
                if dist_to_other < self.radius * 2:
                    can_move = False
                    push_dx = self.actor.x - other.actor.x
                    push_dy = self.actor.y - other.actor.y
                    push_dist = math.sqrt(push_dx * push_dx + push_dy * push_dy)
                    if push_dist > 0:
                        self.actor.x += (push_dx / push_dist) * 0.5
                        self.actor.y += (push_dy / push_dist) * 0.5
                    break
            
            if can_move:
                self.actor.x = new_x
                self.actor.y = new_y
            
            if abs(dx) > abs(dy):
                if dx > 0:
                    self.current_anim = self.anim_side_right
                else:
                    self.current_anim = self.anim_side_left
            else:
                if dy > 0:
                    self.current_anim = self.anim_down
                else:
                    self.current_anim = self.anim_up
            
            self.current_anim.update(dt)
            self.actor.image = self.current_anim.get_current_image()
    
    def attack(self, target_player):
        if self.attack_cooldown <= 0:
            target_player.hp -= self.damage
            self.attack_cooldown = self.attack_rate
            try:
                sounds.hit.play()
            except:
                pass
    
    def draw(self):
        self.actor.draw()
        #  HP bar above zombie
        bar_width = 40
        bar_height = 5
        hp_ratio = self.hp / 50
        screen.draw.filled_rect(
            Rect((self.actor.x - bar_width/2, self.actor.y - 30), (bar_width, bar_height)),
            'darkred'
        )
        screen.draw.filled_rect(
            Rect((self.actor.x - bar_width/2, self.actor.y - 30), (bar_width * hp_ratio, bar_height)),
            'red'
        )

        
zombies = [
    Zombie(100, 100),
    Zombie(400, 200),
    Zombie(700, 500),
]


def draw():
    screen.fill((20, 20, 30))
    
    if game_state == "menu":
        screen.draw.text('ZOMBIE APOCALYPSE', fontname = 'bloody.ttf', center=(400, 150), fontsize=60, color='red')
        
        screen.draw.filled_rect(btn_start, 'darkred')
        screen.draw.text('START GAME', center=btn_start.center, fontsize=24, color='white')
        
        screen.draw.filled_rect(btn_music, 'darkgreen' if music_on else 'gray')
        music_text = 'MUSIC: ON' if music_on else 'MUSIC: OFF'
        screen.draw.text(music_text, center=btn_music.center, fontsize=24, color='white')
        
        screen.draw.filled_rect(btn_exit, 'darkblue')
        screen.draw.text('EXIT', center=btn_exit.center, fontsize=24, color='white')
        
    elif game_state == "game":
        player.draw()
        for zombie in zombies:
            zombie.draw()
            
        screen.draw.filled_rect(Rect((10, 10), (200, 20)), 'darkred')
        hp_width = (player.hp / player.max_hp) * 200
        screen.draw.filled_rect(Rect((10, 10), (hp_width, 20)), 'red')
        screen.draw.text(f'HP: {player.hp}/{player.max_hp}', (15, 12), fontsize=16, color='white')
        
        #  hint
        screen.draw.text('WASD - move | SPACE - attack | ESC - menu', (10, HEIGHT - 30), fontsize=16, color='gray')

    
def update(dt):
    global game_state, zombies
    if game_state == "game":
        player.update(dt)
        

        player.weapon.check_hit(zombies)

        for zombie in zombies[:]:  
            zombie.update(dt, player, zombies)
            if zombie.hp <= 0:
                zombies.remove(zombie)
                try:
                    sounds.kill.play()
                except:
                    pass
            
        if player.hp <= 0:
            try:
                sounds.gameover.play()
            except:
                pass
            game_state = "menu"
            reset_game()


def reset_game():
    global zombies
    player.hp = player.max_hp
    player.actor.x = 400
    player.actor.y = 300
    zombies = [
        Zombie(100, 100),
        Zombie(400, 200),
        Zombie(700, 500),
    ]


def on_mouse_down(pos):
    global game_state, music_on
    if game_state == "menu":
        if btn_start.collidepoint(pos):
            game_state = "game"
            try:
                sounds.start.play()
            except:
                pass
        elif btn_music.collidepoint(pos):
            music_on = not music_on
            try:
                if music_on:
                    music.play('background')
                else:
                    music.stop()
            except:
                pass
        elif btn_exit.collidepoint(pos):
            exit()


def on_key_down(key):
    global game_state
    if key == keys.ESCAPE:
        if game_state == "game":
            game_state = "menu"
        else:
            exit()

    if key == keys.SPACE and game_state == "game":
        player.attack()

try:
    music.play('background')
    music.set_volume(0.5)
except:
    print("Music not available")
    music_on = False

pgzrun.go()