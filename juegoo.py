import pygame, random, math

# Inicializar pygame
pygame.init()
pygame.mixer.init()

# Colores
WHITE = (255,255,255); BLACK = (0,0,0)
RED = (255,50,50); GREEN = (50,255,50)
BLUE = (50,150,255); YELLOW = (255,255,0)
ORANGE = (255,180,50)

# Pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Purificador Hero")
clock = pygame.time.Clock()
FPS = 60
font = pygame.font.SysFont("Arial", 28)

# ----------- VARIABLES ----------- 
game_state = "MENU"  # MENU, GAME, SHOP, GAME_OVER
level = 1
score = 0
coins = 0
pollution = 0
MAX_MONSTERS = 8
game_over = False

# Mejoras
player_speed = 6
suction_range = 80
skin_color = BLUE

# ----------- CLASES -----------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50,50), pygame.SRCALPHA)
        pygame.draw.circle(self.image, skin_color, (25,25),25)
        pygame.draw.circle(self.image, WHITE, (18,18),8)
        self.rect = self.image.get_rect(center=(WIDTH//2,HEIGHT-70))
        self.speed = player_speed
        self.suction = False

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0: self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH: self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0: self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT: self.rect.y += self.speed
        self.suction = keys[pygame.K_SPACE]

class Monster(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        size = random.randint(20,40)
        self.image = pygame.Surface((size,size),pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED,(size//2,size//2),size//2)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0,WIDTH-size)
        self.rect.y = random.randint(0,HEIGHT-200)
        self.speedx = random.choice([-2,-1,1,2]) + level//2
        self.speedy = random.choice([-2,-1,1,2]) + level//2

    def update(self):
        self.rect.x += self.speedx; self.rect.y += self.speedy
        if self.rect.left<0 or self.rect.right>WIDTH: self.speedx *= -1
        if self.rect.top<0 or self.rect.bottom>HEIGHT-50: self.speedy *= -1

# ----------- FUNCIONES ----------
def beep():
    try:
        import winsound
        winsound.Beep(600,50)
    except: pass

def draw_bar(surf,x,y,pct,color):
    pct = max(0,min(100,pct))
    BAR_LENGTH, BAR_HEIGHT = 200,20
    fill = (pct/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surf,color,fill_rect)
    pygame.draw.rect(surf,BLACK,outline_rect,2)

def show_text(text,size,color,y):
    f = pygame.font.SysFont("Arial",size)
    label = f.render(text,True,color)
    rect = label.get_rect(center=(WIDTH//2,y))
    screen.blit(label,rect)

def spawn_monsters(group,all_sprites):
    for _ in range(MAX_MONSTERS):
        m = Monster(); group.add(m); all_sprites.add(m)

def reset_game():
    global score,pollution,game_over,MAX_MONSTERS
    score = 0; pollution = 0; game_over = False
    MAX_MONSTERS = 6 + level*2

def create_player():
    p = Player()
    p.speed = player_speed
    return p

# ----------- SPRITES INICIALES -----------
all_sprites = pygame.sprite.Group()
monsters = pygame.sprite.Group()
player = create_player()
all_sprites.add(player)
spawn_monsters(monsters,all_sprites)

# ----------- LOOP PRINCIPAL -----------
running = True
while running:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if game_state=="MENU":
                if e.key==pygame.K_1:
                    game_state="GAME"; reset_game()
                    all_sprites.empty(); monsters.empty()
                    player=create_player(); all_sprites.add(player); spawn_monsters(monsters,all_sprites)
                if e.key==pygame.K_2: game_state="SHOP"
                if e.key==pygame.K_3: running=False
            elif game_state=="SHOP":
                if e.key==pygame.K_1 and coins>=5: coins-=5; player_speed+=1
                if e.key==pygame.K_2 and coins>=5: coins-=5; suction_range+=10
                if e.key==pygame.K_3 and coins>=10: coins-=10; skin_color=(random.randint(50,255),random.randint(50,255),random.randint(50,255))
                if e.key==pygame.K_ESCAPE: game_state="MENU"
            elif game_state=="GAME_OVER":
                if e.key==pygame.K_RETURN: game_state="MENU"

    # -------- ESTADOS --------
    if game_state=="MENU":
        screen.fill((180,230,255))
        show_text("PURIFICADOR HERO",60,BLACK,100)
        
        # Botones con cuadritos de color
        btn_jugar = pygame.Rect(WIDTH//2-100,230,200,50)
        btn_tienda = pygame.Rect(WIDTH//2-100,300,200,50)
        btn_salir  = pygame.Rect(WIDTH//2-100,370,200,50)
        pygame.draw.rect(screen, ORANGE, btn_jugar)
        pygame.draw.rect(screen, ORANGE, btn_tienda)
        pygame.draw.rect(screen, ORANGE, btn_salir)
        show_text("JUGAR",40,WHITE,255)
        show_text("TIENDA",40,WHITE,325)
        show_text("SALIR",40,WHITE,395)

        # Detectar clic del mouse
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if mouse_click[0]:
            if btn_jugar.collidepoint(mouse_pos):
                game_state="GAME"; reset_game()
                all_sprites.empty(); monsters.empty()
                player=create_player(); all_sprites.add(player); spawn_monsters(monsters,all_sprites)
            elif btn_tienda.collidepoint(mouse_pos):
                game_state="SHOP"
            elif btn_salir.collidepoint(mouse_pos):
                running=False

    elif game_state=="SHOP":
        screen.fill((200,240,200))
        show_text("TIENDA",60,BLACK,80)
        show_text(f"Monedas: {coins}",40,YELLOW,150)
        show_text("1. +1 Velocidad (5c)",35,BLACK,250)
        show_text("2. +10 Rango (5c)",35,BLACK,300)
        show_text("3. Skin Aleatoria (10c)",35,BLACK,350)
        show_text("ESC: Volver",30,RED,500)

    elif game_state=="GAME":
        if not game_over:
            monsters.update()
            player.update(keys)
            for m in monsters:
                dist = math.hypot(player.rect.centerx-m.rect.centerx,player.rect.centery-m.rect.centery)
                if player.suction and dist<suction_range:
                    beep(); m.kill(); score+=1; coins+=1
            pollution += 0.05*(len(monsters)/MAX_MONSTERS)
            if pollution>=100: game_over=True
            if len(monsters)==0:
                level+=1; reset_game()
                all_sprites.empty(); monsters.empty()
                player=create_player(); all_sprites.add(player); spawn_monsters(monsters,all_sprites)

        screen.fill((180,230,255))
        pygame.draw.rect(screen,(200,180,120),(0,HEIGHT-50,WIDTH,50))
        all_sprites.draw(screen)
        draw_bar(screen,WIDTH-220,10,pollution,RED)
        screen.blit(font.render(f"Puntos:{score}",True,BLACK),(10,10))
        screen.blit(font.render(f"Nivel:{level}",True,BLACK),(10,40))
        screen.blit(font.render(f"Monedas:{coins}",True,YELLOW),(10,70))

        # Botón regresar al menú
        btn_menu = pygame.Rect(WIDTH-120, 10, 110,40)
        pygame.draw.rect(screen, ORANGE, btn_menu)
        screen.blit(font.render("MENÚ",True,WHITE),(WIDTH-105,15))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if mouse_click[0] and btn_menu.collidepoint(mouse_pos):
            game_state="MENU"
            all_sprites.empty(); monsters.empty()
            player=create_player(); all_sprites.add(player)

    elif game_state=="GAME_OVER":
        screen.fill((255,200,200))
        show_text("¡PERDISTE! Aula contaminada",50,RED,200)
        show_text("Presiona ENTER para volver al menú",30,BLACK,400)

    pygame.display.flip()

pygame.quit()
