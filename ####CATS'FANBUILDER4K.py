import pygame, sys, json, os, math, random, copy

pygame.init()

# ---------------- CONFIG ----------------
W, H = 1280, 720
FPS = 60
TILE = 32

# Brand Info
BRAND_NAME = "AC'S SMBX2"
VERSION = "V0.1.2[A]"
COPYRIGHT = "© AC Computers 1999-2026  Regedit 2000-2026"

# SMBX2 Editor Color Scheme
C_BG_DARK = (30, 30, 30)
C_PANEL = (45, 45, 48)
C_PANEL_DARK = (37, 37, 40)
C_PANEL_LIGHT = (56, 56, 60)
C_BORDER = (22, 22, 24)
C_TEXT = (220, 220, 220)
C_TEXT_DIM = (140, 140, 145)
C_ACCENT = (0, 122, 204)
C_ACCENT_HOVER = (28, 151, 234)
C_TAB_ACTIVE = (60, 60, 65)
C_TAB_INACTIVE = (45, 45, 48)
C_GRID_MAJOR = (80, 80, 85)
C_GRID_MINOR = (50, 50, 55)
C_SKY = (92, 148, 252)
C_SKY_GRAD = (156, 192, 254)
C_SUCCESS = (46, 160, 67)
C_BUTTON = (55, 55, 60)
C_BUTTON_HOVER = (70, 70, 75)
C_MENU_BG = (20, 24, 32)
C_MENU_PANEL = (32, 36, 48)
C_GOLD = (255, 200, 50)
C_RED = (220, 60, 60)
C_SELECTION = (0, 180, 255)

# Physics
GRAVITY = 0.35
GRAVITY_HOLD = 0.2
FRICTION = 0.89
ACCEL = 0.14
ACCEL_RUN = 0.21
MAX_WALK = 3.5
MAX_RUN = 6.5
JUMP_FORCE = -9.8
JUMP_FORCE_RUN = -10.8
P_METER_MAX = 112

screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
pygame.display.set_caption(f"{BRAND_NAME} {VERSION}")
clock = pygame.time.Clock()

# Fonts
try:
    FONT_SM = pygame.font.SysFont("Segoe UI", 11)
    FONT = pygame.font.SysFont("Segoe UI", 12)
    FONT_MD = pygame.font.SysFont("Segoe UI", 13, bold=True)
    FONT_LG = pygame.font.SysFont("Segoe UI", 14, bold=True)
    FONT_TITLE = pygame.font.SysFont("Segoe UI", 16, bold=True)
    FONT_SPLASH = pygame.font.SysFont("Segoe UI", 48, bold=True)
    FONT_SPLASH_SM = pygame.font.SysFont("Segoe UI", 18)
    FONT_SPLASH_VER = pygame.font.SysFont("Segoe UI", 24, bold=True)
    FONT_MENU = pygame.font.SysFont("Segoe UI", 28, bold=True)
    FONT_MENU_SM = pygame.font.SysFont("Segoe UI", 16)
    FONT_MENU_LG = pygame.font.SysFont("Segoe UI", 36, bold=True)
except:
    FONT_SM = pygame.font.SysFont("Arial", 11)
    FONT = pygame.font.SysFont("Arial", 12)
    FONT_MD = pygame.font.SysFont("Arial", 13, bold=True)
    FONT_LG = pygame.font.SysFont("Arial", 14, bold=True)
    FONT_TITLE = pygame.font.SysFont("Arial", 16, bold=True)
    FONT_SPLASH = pygame.font.SysFont("Arial", 48, bold=True)
    FONT_SPLASH_SM = pygame.font.SysFont("Arial", 18)
    FONT_SPLASH_VER = pygame.font.SysFont("Arial", 24, bold=True)
    FONT_MENU = pygame.font.SysFont("Arial", 28, bold=True)
    FONT_MENU_SM = pygame.font.SysFont("Arial", 16)
    FONT_MENU_LG = pygame.font.SysFont("Arial", 36, bold=True)

# ---------------- MENU ASSETS ----------------
def create_menu_mario():
    """Large Mario for menu screen"""
    s = pygame.Surface((64, 64), pygame.SRCALPHA)
    skin = (255, 200, 148)
    red = (228, 52, 52)
    brown = (128, 56, 0)
    blue = (32, 64, 200)
    
    # Hat
    pygame.draw.rect(s, red, (16, 4, 32, 12))
    pygame.draw.rect(s, red, (12, 8, 8, 8))
    # Face
    pygame.draw.rect(s, skin, (16, 16, 28, 20))
    # Hair
    pygame.draw.rect(s, brown, (12, 16, 8, 12))
    pygame.draw.rect(s, brown, (40, 24, 8, 8))
    # Eyes
    pygame.draw.rect(s, (0,0,0), (20, 20, 6, 6))
    pygame.draw.rect(s, (0,0,0), (32, 20, 6, 6))
    pygame.draw.rect(s, (255,255,255), (22, 22, 2, 2))
    pygame.draw.rect(s, (255,255,255), (34, 22, 2, 2))
    # Mustache
    pygame.draw.rect(s, brown, (18, 30, 24, 4))
    # Shirt
    pygame.draw.rect(s, red, (12, 36, 40, 12))
    # Overalls
    pygame.draw.rect(s, blue, (16, 44, 32, 16))
    pygame.draw.rect(s, C_GOLD, (22, 46, 4, 4))  # Button
    pygame.draw.rect(s, C_GOLD, (36, 46, 4, 4))  # Button
    # Arms
    pygame.draw.rect(s, red, (4, 38, 12, 8))
    pygame.draw.rect(s, red, (46, 38, 12, 8))
    pygame.draw.rect(s, skin, (2, 44, 10, 8))
    pygame.draw.rect(s, skin, (50, 44, 10, 8))
    # Feet
    pygame.draw.rect(s, brown, (10, 58, 16, 6))
    pygame.draw.rect(s, brown, (36, 58, 16, 6))
    
    return s

def create_menu_goomba():
    """Goomba for menu decoration"""
    s = pygame.Surface((48, 48), pygame.SRCALPHA)
    pygame.draw.ellipse(s, (168, 80, 32), (6, 12, 36, 30))
    pygame.draw.ellipse(s, (96, 40, 0), (9, 3, 30, 21))
    pygame.draw.ellipse(s, (255,255,255), (9, 9, 12, 15))
    pygame.draw.ellipse(s, (255,255,255), (27, 9, 12, 15))
    pygame.draw.ellipse(s, (0,0,0), (15, 15, 6, 9))
    pygame.draw.ellipse(s, (0,0,0), (27, 15, 6, 9))
    pygame.draw.ellipse(s, (0,0,0), (3, 39, 18, 9))
    pygame.draw.ellipse(s, (0,0,0), (27, 39, 18, 9))
    return s

def create_menu_block():
    """Question block for menu"""
    s = pygame.Surface((48, 48))
    s.fill((248, 184, 0))
    pygame.draw.rect(s, (255, 232, 128), (0, 0, 48, 4))
    pygame.draw.rect(s, (184, 112, 0), (0, 44, 48, 4))
    # ? mark
    pygame.draw.rect(s, (255,255,255), (16, 8, 16, 5))
    pygame.draw.rect(s, (255,255,255), (27, 13, 5, 8))
    pygame.draw.rect(s, (255,255,255), (18, 21, 10, 5))
    pygame.draw.rect(s, (255,255,255), (18, 26, 5, 5))
    pygame.draw.rect(s, (255,255,255), (18, 35, 5, 6))
    return s

def create_folder_icon():
    """Folder icon for episodes"""
    s = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.rect(s, (220, 180, 80), (2, 8, 28, 22), border_radius=2)
    pygame.draw.rect(s, (255, 210, 100), (2, 4, 14, 6), border_radius=2)
    pygame.draw.rect(s, (180, 140, 40), (2, 8, 28, 4))
    return s

def create_wrench_icon():
    """Wrench icon for editor"""
    s = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.polygon(s, (180, 180, 190), [(8, 4), (14, 4), (14, 14), (24, 24), (20, 28), (10, 18), (4, 18), (4, 12), (8, 12)])
    pygame.draw.circle(s, (140, 140, 150), (20, 24), 6, 2)
    return s

def create_star():
    """Star decoration"""
    s = pygame.Surface((24, 24), pygame.SRCALPHA)
    points = []
    for i in range(5):
        angle = math.radians(i * 72 - 90)
        points.append((12 + 10 * math.cos(angle), 12 + 10 * math.sin(angle)))
        angle = math.radians(i * 72 - 90 + 36)
        points.append((12 + 4 * math.cos(angle), 12 + 4 * math.sin(angle)))
    pygame.draw.polygon(s, C_GOLD, points)
    return s

# Episode data
EPISODES = [
    {"name": "The Invasion 2", "author": "AC Studios", "levels": 24, "stars": 5, "difficulty": "Normal"},
    {"name": "Super Mario Bros. X", "author": "Redigit", "levels": 64, "stars": 0, "difficulty": "Classic"},
    {"name": "Talkhaus Episode", "author": "Community", "levels": 38, "stars": 3, "difficulty": "Hard"},
    {"name": "A2XT Episode 1", "author": "Horikawa", "levels": 52, "stars": 4, "difficulty": "Expert"},
    {"name": "The Princess Cliche", "author": "Demo", "levels": 12, "stars": 2, "difficulty": "Easy"},
]

class MenuButton:
    def __init__(self, x, y, w, h, text, icon=None, color=C_ACCENT):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.icon = icon
        self.color = color
        self.hover = False
        self.press_anim = 0
    
    def update(self, mx, my, clicked):
        self.hover = self.rect.collidepoint(mx, my)
        if self.press_anim > 0:
            self.press_anim -= 1
        if self.hover and clicked:
            self.press_anim = 8
            return True
        return False
    
    def draw(self, surf):
        # Shadow
        shadow_rect = self.rect.copy()
        shadow_rect.y += 4
        pygame.draw.rect(surf, (0, 0, 0, 80), shadow_rect, border_radius=8)
        
        # Button body
        col = self.color
        if self.hover:
            col = tuple(min(255, c + 30) for c in self.color)
        
        draw_rect = self.rect.copy()
        if self.press_anim > 0:
            draw_rect.y += 2
        
        # Gradient effect
        pygame.draw.rect(surf, col, draw_rect, border_radius=8)
        highlight = pygame.Surface((draw_rect.width, draw_rect.height // 2), pygame.SRCALPHA)
        highlight.fill((255, 255, 255, 30))
        surf.blit(highlight, draw_rect.topleft)
        
        # Border
        border_col = tuple(min(255, c + 50) for c in col)
        pygame.draw.rect(surf, border_col, draw_rect, 2, border_radius=8)
        
        # Icon
        cx = draw_rect.centerx
        cy = draw_rect.centery
        if self.icon:
            surf.blit(self.icon, (draw_rect.x + 20, cy - 16))
            cx += 20
        
        # Text
        txt = FONT_MENU.render(self.text, True, C_TEXT)
        surf.blit(txt, (cx - txt.get_width()//2, cy - txt.get_height()//2))

class EpisodeCard:
    def __init__(self, x, y, w, h, episode_data, index):
        self.rect = pygame.Rect(x, y, w, h)
        self.data = episode_data
        self.index = index
        self.hover = False
        self.selected = False
    
    def update(self, mx, my, clicked):
        self.hover = self.rect.collidepoint(mx, my)
        if self.hover and clicked:
            return True
        return False
    
    def draw(self, surf, star_img):
        # Card background
        col = C_PANEL_LIGHT if self.hover else C_MENU_PANEL
        if self.selected:
            col = C_TAB_ACTIVE
        
        pygame.draw.rect(surf, col, self.rect, border_radius=6)
        
        if self.selected:
            pygame.draw.rect(surf, C_ACCENT, self.rect, 3, border_radius=6)
        elif self.hover:
            pygame.draw.rect(surf, C_ACCENT_HOVER, self.rect, 2, border_radius=6)
        
        # Episode number
        num_surf = FONT_MENU.render(f"{self.index + 1}", True, C_ACCENT)
        pygame.draw.circle(surf, C_PANEL_DARK, (self.rect.x + 30, self.rect.centery), 20)
        surf.blit(num_surf, (self.rect.x + 30 - num_surf.get_width()//2, self.rect.centery - num_surf.get_height()//2))
        
        # Episode name
        name_surf = FONT_LG.render(self.data["name"], True, C_TEXT)
        surf.blit(name_surf, (self.rect.x + 60, self.rect.y + 12))
        
        # Author
        author_surf = FONT_SM.render(f"by {self.data['author']}", True, C_TEXT_DIM)
        surf.blit(author_surf, (self.rect.x + 60, self.rect.y + 32))
        
        # Stats
        levels_surf = FONT_SM.render(f"{self.data['levels']} Levels", True, C_TEXT_DIM)
        surf.blit(levels_surf, (self.rect.x + 60, self.rect.y + 50))
        
        # Difficulty badge
        diff = self.data["difficulty"]
        diff_colors = {"Easy": (80, 180, 80), "Normal": (80, 150, 220), "Classic": (180, 140, 80),
                      "Hard": (220, 140, 60), "Expert": (200, 60, 60)}
        diff_col = diff_colors.get(diff, C_TEXT_DIM)
        diff_surf = FONT_SM.render(diff, True, diff_col)
        pygame.draw.rect(surf, (*diff_col, 40), (self.rect.right - 80, self.rect.y + 12, 70, 20), border_radius=4)
        surf.blit(diff_surf, (self.rect.right - 80 + (70 - diff_surf.get_width())//2, self.rect.y + 14))
        
        # Stars
        for i in range(5):
            sx = self.rect.right - 85 + i * 16
            if i < self.data["stars"]:
                surf.blit(star_img, (sx, self.rect.y + 42))
            else:
                # Empty star
                pygame.draw.polygon(surf, (60, 60, 65), 
                    [(sx+8 + 6*math.cos(math.radians(j*72-90)), self.rect.y+50 + 6*math.sin(math.radians(j*72-90))) 
                     for j in range(5)], 1)

# ---------------- SPLASH SCREEN ----------------
def create_splash_mario(frame):
    s = pygame.Surface((32, 32), pygame.SRCALPHA)
    skin = (255, 200, 148)
    red = (228, 52, 52)
    brown = (128, 56, 0)
    blue = (32, 64, 200)
    leg_offset = [0, 2, 4, 2][frame % 4]
    arm_offset = [0, -2, 0, 2][frame % 4]
    
    pygame.draw.rect(s, red, (8, 2 + abs(leg_offset)//2, 16, 6))
    pygame.draw.rect(s, red, (6, 4 + abs(leg_offset)//2, 4, 4))
    pygame.draw.rect(s, skin, (8, 8 + abs(leg_offset)//2, 14, 10))
    pygame.draw.rect(s, brown, (6, 8 + abs(leg_offset)//2, 4, 6))
    pygame.draw.rect(s, (0,0,0), (10, 10 + abs(leg_offset)//2, 3, 3))
    pygame.draw.rect(s, (0,0,0), (16, 10 + abs(leg_offset)//2, 3, 3))
    pygame.draw.rect(s, red, (6, 18, 20, 6))
    pygame.draw.rect(s, red, (2 + arm_offset, 18, 6, 4))
    pygame.draw.rect(s, red, (22 - arm_offset, 18, 6, 4))
    pygame.draw.rect(s, blue, (8, 22, 16, 6))
    pygame.draw.rect(s, blue, (6 - leg_offset, 26, 6, 6))
    pygame.draw.rect(s, blue, (18 + leg_offset, 26, 6, 6))
    pygame.draw.rect(s, brown, (4 - leg_offset, 30, 8, 4))
    pygame.draw.rect(s, brown, (18 + leg_offset, 30, 8, 4))
    return s

def create_n64_logo():
    s = pygame.Surface((120, 120), pygame.SRCALPHA)
    red, green, blue, yellow = (228, 52, 52), (52, 180, 52), (52, 100, 228), (255, 220, 0)
    pts = [(20, 100), (20, 20), (40, 20), (60, 60), (60, 20), (100, 20), (100, 100), (80, 100), (80, 60), (60, 100), (40, 100), (40, 40), (40, 100)]
    shadow_pts = [(p[0] + 6, p[1] + 6) for p in pts]
    pygame.draw.polygon(s, (40, 40, 40), shadow_pts)
    pygame.draw.polygon(s, red, pts[:4] + [(40, 100), (20, 100)])
    pygame.draw.polygon(s, green, [(40, 20), (60, 60), (60, 20)])
    pygame.draw.polygon(s, blue, [(60, 20), (100, 20), (100, 100), (80, 100), (80, 60), (60, 60)])
    pygame.draw.polygon(s, yellow, [(40, 40), (40, 100), (60, 100), (60, 60)])
    pygame.draw.polygon(s, (255, 255, 255), pts, 2)
    return s

def create_star_particle():
    s = pygame.Surface((8, 8), pygame.SRCALPHA)
    pygame.draw.line(s, (255, 255, 200), (4, 0), (4, 8), 1)
    pygame.draw.line(s, (255, 255, 200), (0, 4), (8, 4), 1)
    pygame.draw.line(s, (255, 255, 150), (1, 1), (7, 7), 1)
    pygame.draw.line(s, (255, 255, 150), (7, 1), (1, 7), 1)
    return s

class SplashParticle:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-3, -1)
        self.life = random.randint(20, 40)
        self.max_life = self.life
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1
        self.life -= 1
        return self.life > 0
    
    def draw(self, surf, img):
        alpha = int(255 * (self.life / self.max_life))
        img_copy = img.copy()
        img_copy.set_alpha(alpha)
        surf.blit(img_copy, (int(self.x), int(self.y)))

def run_splash_screen():
    global W, H, screen
    
    n_logo = create_n64_logo()
    star_img = create_star_particle()
    mario_frames = [create_splash_mario(i) for i in range(4)]
    
    phase, timer = 0, 0
    logo_alpha, logo_scale, logo_rotation = 0, 0.5, 0
    text_alpha = 0
    mario_angle, mario_frame, mario_frame_timer = 0, 0, 0
    particles = []
    
    running = True
    while running:
        clock.tick(FPS)
        timer += 1
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN or e.type == pygame.MOUSEBUTTONDOWN:
                if timer > 30: running = False
            if e.type == pygame.VIDEORESIZE:
                W, H = e.w, e.h
                screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
        
        if phase == 0 and timer > 60: phase = 1
        elif phase == 1 and timer > 180: phase = 2
        elif phase == 2 and timer > 300: phase = 3
        elif phase == 3 and timer > 360: running = False
        
        if phase == 0:
            logo_alpha = min(255, logo_alpha + 8)
            logo_scale = min(1.0, logo_scale + 0.02)
            logo_rotation = (logo_rotation + 8) % 360
        elif phase == 1:
            logo_alpha = 255
            logo_scale = 1.0
            logo_rotation *= 0.9
            mario_angle += 0.05
            mario_frame_timer += 1
            if mario_frame_timer > 6:
                mario_frame_timer = 0
                mario_frame = (mario_frame + 1) % 4
            if timer % 4 == 0:
                mx = W//2 + math.cos(mario_angle) * 140
                my = H//2 + math.sin(mario_angle) * 70 + 20
                particles.append(SplashParticle(mx, my))
        elif phase == 2:
            text_alpha = min(255, text_alpha + 6)
            mario_angle += 0.03
            mario_frame_timer += 1
            if mario_frame_timer > 8:
                mario_frame_timer = 0
                mario_frame = (mario_frame + 1) % 4
        elif phase == 3:
            logo_alpha = max(0, logo_alpha - 8)
            text_alpha = max(0, text_alpha - 8)
        
        particles = [p for p in particles if p.update()]
        
        screen.fill((8, 8, 12))
        random.seed(42)
        for i in range(50):
            sx, sy = random.randint(0, W), random.randint(0, H)
            twinkle = abs(math.sin((timer + i * 10) * 0.05)) * 55 + 200
            col = (int(random.randint(100, 255) * twinkle / 255),) * 3
            pygame.draw.circle(screen, col, (sx, sy), random.randint(1, 2))
        random.seed()
        
        for p in particles:
            p.draw(screen, star_img)
        
        if logo_alpha > 0:
            scaled = pygame.transform.scale(n_logo, (int(120 * logo_scale), int(120 * logo_scale)))
            if abs(logo_rotation) > 0.5:
                scaled = pygame.transform.rotate(scaled, logo_rotation)
            scaled.set_alpha(logo_alpha)
            screen.blit(scaled, scaled.get_rect(center=(W//2, H//2 - 30)))
        
        if phase >= 1:
            mx = W//2 + math.cos(mario_angle) * 140 - 16
            my = H//2 + math.sin(mario_angle) * 70 - 16
            mario_img = mario_frames[mario_frame]
            if math.cos(mario_angle) < 0:
                mario_img = pygame.transform.flip(mario_img, True, False)
            scale = 0.8 + 0.4 * (math.sin(mario_angle) * 0.5 + 0.5)
            scaled = pygame.transform.scale(mario_img, (int(32 * scale), int(32 * scale)))
            scaled.set_alpha(logo_alpha)
            shadow = pygame.Surface((int(24 * scale), int(8 * scale)), pygame.SRCALPHA)
            pygame.draw.ellipse(shadow, (0, 0, 0, 80), shadow.get_rect())
            screen.blit(shadow, (mx + 4, H//2 + 70 + 10))
            screen.blit(scaled, (mx, my))
        
        if text_alpha > 0:
            brand = FONT_SPLASH.render(BRAND_NAME, True, (255, 255, 255))
            brand.set_alpha(text_alpha)
            screen.blit(brand, brand.get_rect(center=(W//2, H//2 + 80)))
            ver = FONT_SPLASH_VER.render(VERSION, True, C_ACCENT)
            ver.set_alpha(text_alpha)
            screen.blit(ver, ver.get_rect(center=(W//2, H//2 + 120)))
            copy = FONT_SPLASH_SM.render(COPYRIGHT, True, (150, 150, 155))
            copy.set_alpha(text_alpha)
            screen.blit(copy, copy.get_rect(center=(W//2, H//2 + 160)))
            dots = "." * ((timer // 20) % 4)
            load = FONT_SM.render(f"Loading{dots}", True, (100, 100, 105))
            load.set_alpha(text_alpha)
            screen.blit(load, (W//2 - 30, H - 40))
        
        if timer > 60:
            skip = FONT_SM.render("Press any key to skip", True, (80, 80, 85))
            skip.set_alpha(min(150, (timer - 60) * 2))
            screen.blit(skip, (W - 150, H - 25))
        
        pygame.display.flip()
    
    pygame.time.wait(200)

# ---------------- MAIN MENU ----------------
def run_main_menu():
    global W, H, screen
    
    # Create menu assets
    mario_img = create_menu_mario()
    goomba_img = create_menu_goomba()
    block_img = create_menu_block()
    folder_icon = create_folder_icon()
    wrench_icon = create_wrench_icon()
    star_img = create_star()
    
    # Animated decorations
    class FloatingBlock:
        def __init__(self, x, y):
            self.x, self.y = x, y
            self.base_y = y
            self.phase = random.uniform(0, math.pi * 2)
            self.speed = random.uniform(0.02, 0.04)
        
        def update(self, timer):
            self.y = self.base_y + math.sin(timer * self.speed + self.phase) * 8
        
        def draw(self, surf):
            surf.blit(block_img, (self.x, self.y))
    
    class WalkingGoomba:
        def __init__(self, x, y):
            self.x, self.y = x, y
            self.dir = 1
            self.frame = 0
        
        def update(self):
            self.x += self.dir * 1.5
            if self.x > W + 50:
                self.x = -50
            elif self.x < -50:
                self.x = W + 50
            self.frame = (self.frame + 1) % 20
        
        def draw(self, surf):
            img = goomba_img
            if self.frame >= 10:
                img = pygame.transform.flip(goomba_img, True, False)
            surf.blit(img, (self.x, self.y))
    
    # Create decorations
    blocks = [FloatingBlock(100, 150), FloatingBlock(W - 150, 180), FloatingBlock(200, H - 200)]
    goombas = [WalkingGoomba(-30, H - 80), WalkingGoomba(W // 2, H - 85)]
    
    # Menu state
    menu_state = "main"  # main, episodes
    selected_episode = 0
    
    # Main menu buttons
    btn_episodes = MenuButton(W//2 - 180, H//2 - 20, 360, 70, "Play Episode", folder_icon, (60, 140, 60))
    btn_editor = MenuButton(W//2 - 180, H//2 + 70, 360, 70, "Level Editor", wrench_icon, (60, 100, 180))
    btn_quit = MenuButton(W//2 - 100, H//2 + 160, 200, 50, "Quit", None, (140, 60, 60))
    
    # Episode cards
    episode_cards = []
    
    # Back button for episodes
    btn_back = MenuButton(40, H - 70, 120, 45, "← Back", None, C_PANEL_LIGHT)
    btn_play = MenuButton(W - 200, H - 70, 160, 45, "▶ Play", None, (60, 160, 60))
    
    timer = 0
    mario_bob = 0
    
    running = True
    while running:
        dt = clock.tick(FPS)
        timer += 1
        mx, my = pygame.mouse.get_pos()
        clicked = False
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.VIDEORESIZE:
                W, H = e.w, e.h
                screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
                # Recreate buttons with new positions
                btn_episodes = MenuButton(W//2 - 180, H//2 - 20, 360, 70, "Play Episode", folder_icon, (60, 140, 60))
                btn_editor = MenuButton(W//2 - 180, H//2 + 70, 360, 70, "Level Editor", wrench_icon, (60, 100, 180))
                btn_quit = MenuButton(W//2 - 100, H//2 + 160, 200, 50, "Quit", None, (140, 60, 60))
                btn_back = MenuButton(40, H - 70, 120, 45, "← Back", None, C_PANEL_LIGHT)
                btn_play = MenuButton(W - 200, H - 70, 160, 45, "▶ Play", None, (60, 160, 60))
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                clicked = True
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    if menu_state == "episodes":
                        menu_state = "main"
                    else:
                        pygame.quit()
                        sys.exit()
                if menu_state == "episodes":
                    if e.key == pygame.K_UP:
                        selected_episode = max(0, selected_episode - 1)
                    if e.key == pygame.K_DOWN:
                        selected_episode = min(len(EPISODES) - 1, selected_episode + 1)
                    if e.key == pygame.K_RETURN:
                        return ("play", EPISODES[selected_episode])
        
        # Update decorations
        for block in blocks:
            block.update(timer)
        for goomba in goombas:
            goomba.update()
        mario_bob = math.sin(timer * 0.05) * 5
        
        # ---- DRAW ----
        # Gradient background
        for y in range(H):
            ratio = y / H
            r = int(C_MENU_BG[0] + (C_MENU_PANEL[0] - C_MENU_BG[0]) * ratio)
            g = int(C_MENU_BG[1] + (C_MENU_PANEL[1] - C_MENU_BG[1]) * ratio)
            b = int(C_MENU_BG[2] + (C_MENU_PANEL[2] - C_MENU_BG[2]) * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (W, y))
        
        # Ground
        pygame.draw.rect(screen, (60, 40, 20), (0, H - 40, W, 40))
        pygame.draw.rect(screen, (80, 60, 30), (0, H - 40, W, 8))
        for x in range(0, W, 64):
            pygame.draw.rect(screen, (50, 30, 15), (x, H - 32, 32, 32))
        
        # Draw decorations
        for block in blocks:
            block.draw(screen)
        for goomba in goombas:
            goomba.draw(screen)
        
        if menu_state == "main":
            # Title
            title = FONT_SPLASH.render(BRAND_NAME, True, C_TEXT)
            title_shadow = FONT_SPLASH.render(BRAND_NAME, True, (0, 0, 0))
            screen.blit(title_shadow, (W//2 - title.get_width()//2 + 3, 63))
            screen.blit(title, (W//2 - title.get_width()//2, 60))
            
            # Version badge
            ver = FONT_MENU_SM.render(VERSION, True, C_ACCENT)
            pygame.draw.rect(screen, C_PANEL_DARK, (W//2 + title.get_width()//2 - 10, 70, ver.get_width() + 16, 24), border_radius=4)
            screen.blit(ver, (W//2 + title.get_width()//2 - 2, 73))
            
            # Mario mascot
            screen.blit(mario_img, (W//2 - 220, H//2 - 10 + mario_bob))
            
            # Buttons
            if btn_episodes.update(mx, my, clicked):
                menu_state = "episodes"
                # Create episode cards
                episode_cards = []
                for i, ep in enumerate(EPISODES):
                    card = EpisodeCard(W//2 - 280, 140 + i * 80, 560, 70, ep, i)
                    episode_cards.append(card)
                episode_cards[selected_episode].selected = True
            
            if btn_editor.update(mx, my, clicked):
                return ("editor", None)
            
            if btn_quit.update(mx, my, clicked):
                pygame.quit()
                sys.exit()
            
            btn_episodes.draw(screen)
            btn_editor.draw(screen)
            btn_quit.draw(screen)
            
        elif menu_state == "episodes":
            # Header
            header = FONT_MENU_LG.render("Select Episode", True, C_TEXT)
            screen.blit(header, (W//2 - header.get_width()//2, 60))
            
            # Episode count
            count = FONT_MENU_SM.render(f"{len(EPISODES)} episodes available", True, C_TEXT_DIM)
            screen.blit(count, (W//2 - count.get_width()//2, 100))
            
            # Episode cards
            for i, card in enumerate(episode_cards):
                card.selected = (i == selected_episode)
                if card.update(mx, my, clicked):
                    selected_episode = i
                card.draw(screen, star_img)
            
            # Selected episode info panel
            if selected_episode < len(EPISODES):
                ep = EPISODES[selected_episode]
                info_rect = pygame.Rect(W//2 - 280, H - 150, 560, 60)
                pygame.draw.rect(screen, C_PANEL_DARK, info_rect, border_radius=8)
                
                info_text = f'Ready to play "{ep["name"]}" - {ep["levels"]} levels'
                info_surf = FONT_MENU_SM.render(info_text, True, C_TEXT)
                screen.blit(info_surf, (info_rect.centerx - info_surf.get_width()//2, info_rect.y + 20))
            
            # Navigation buttons
            if btn_back.update(mx, my, clicked):
                menu_state = "main"
            btn_back.draw(screen)
            
            if btn_play.update(mx, my, clicked):
                return ("play", EPISODES[selected_episode])
            btn_play.draw(screen)
        
        # Copyright footer
        copy = FONT_SM.render(COPYRIGHT, True, C_TEXT_DIM)
        screen.blit(copy, (W//2 - copy.get_width()//2, H - 20))
        
        pygame.display.flip()
    
    return ("quit", None)

# ---------------- ICONS ----------------
def make_icon(name):
    s = pygame.Surface((16, 16), pygame.SRCALPHA)
    if name == "new":
        pygame.draw.rect(s, (255,255,255), (3, 2, 10, 12), 1)
        pygame.draw.polygon(s, (255,255,255), [(9,2), (13,6), (9,6)])
    elif name == "open":
        pygame.draw.rect(s, (220,180,80), (2, 6, 12, 8), 0)
        pygame.draw.rect(s, (255,210,100), (1, 4, 10, 3), 0)
    elif name == "save":
        pygame.draw.rect(s, (100,150,255), (2, 2, 12, 12), 0)
        pygame.draw.rect(s, (255,255,255), (4, 2, 8, 5), 0)
        pygame.draw.rect(s, (60,60,60), (6, 3, 4, 3), 0)
        pygame.draw.rect(s, (200,200,200), (4, 9, 8, 4), 0)
    elif name == "undo":
        pygame.draw.arc(s, (255,255,255), (2, 3, 10, 10), 0.5, 3.14, 2)
        pygame.draw.polygon(s, (255,255,255), [(2, 5), (6, 2), (6, 8)])
    elif name == "redo":
        pygame.draw.arc(s, (255,255,255), (4, 3, 10, 10), 0, 2.6, 2)
        pygame.draw.polygon(s, (255,255,255), [(14, 5), (10, 2), (10, 8)])
    elif name == "play":
        pygame.draw.polygon(s, (80,200,80), [(4, 2), (14, 8), (4, 14)])
    elif name == "stop":
        pygame.draw.rect(s, (200,80,80), (3, 3, 10, 10))
    elif name == "grid":
        for i in range(4):
            pygame.draw.line(s, (255,255,255), (i*5+2, 2), (i*5+2, 14), 1)
            pygame.draw.line(s, (255,255,255), (2, i*5+2), (14, i*5+2), 1)
    elif name == "layers":
        pygame.draw.rect(s, (150,150,255), (2, 8, 8, 6), 1)
        pygame.draw.rect(s, (200,200,255), (4, 5, 8, 6), 1)
        pygame.draw.rect(s, (255,255,255), (6, 2, 8, 6), 1)
    elif name == "events":
        pygame.draw.circle(s, (255,200,80), (8, 8), 6, 2)
        pygame.draw.line(s, (255,200,80), (8, 5), (8, 8), 2)
        pygame.draw.line(s, (255,200,80), (8, 8), (11, 10), 2)
    elif name == "select":
        pygame.draw.rect(s, (255,255,255), (3, 3, 10, 10), 1)
        pygame.draw.line(s, C_ACCENT, (1, 1), (6, 6), 2)
    elif name == "eraser":
        pygame.draw.polygon(s, (255,180,180), [(10, 2), (14, 6), (6, 14), (2, 10)])
        pygame.draw.line(s, (255,100,100), (6, 6), (10, 10), 2)
    elif name == "hand":
        pygame.draw.ellipse(s, (255,220,180), (5, 8, 8, 6))
        for i in range(4):
            pygame.draw.rect(s, (255,220,180), (4+i*2, 3, 2, 7))
    elif name == "zoom_in":
        pygame.draw.circle(s, (255,255,255), (7, 7), 5, 1)
        pygame.draw.line(s, (255,255,255), (11, 11), (14, 14), 2)
        pygame.draw.line(s, (255,255,255), (4, 7), (10, 7), 1)
        pygame.draw.line(s, (255,255,255), (7, 4), (7, 10), 1)
    elif name == "zoom_out":
        pygame.draw.circle(s, (255,255,255), (7, 7), 5, 1)
        pygame.draw.line(s, (255,255,255), (11, 11), (14, 14), 2)
        pygame.draw.line(s, (255,255,255), (4, 7), (10, 7), 1)
    elif name == "eyedropper":
        pygame.draw.polygon(s, (255,255,255), [(3, 13), (6, 10), (10, 14)])
        pygame.draw.line(s, (200,200,255), (6, 10), (12, 4), 2)
        pygame.draw.circle(s, (150,150,255), (13, 3), 2)
    elif name == "copy":
        pygame.draw.rect(s, (180,180,255), (1, 3, 9, 11), 1)
        pygame.draw.rect(s, (255,255,255), (5, 1, 9, 11), 1)
        pygame.draw.rect(s, C_PANEL, (5, 3, 5, 9))
    elif name == "paste":
        pygame.draw.rect(s, (200,180,140), (3, 1, 10, 14), 1)
        pygame.draw.rect(s, (150,130,100), (5, 0, 6, 3))
        pygame.draw.line(s, (255,255,255), (5, 6), (11, 6), 1)
        pygame.draw.line(s, (255,255,255), (5, 9), (11, 9), 1)
    elif name == "bounds":
        pygame.draw.rect(s, (255,180,80), (2, 2, 12, 12), 1)
        pygame.draw.line(s, (255,180,80), (2, 7), (5, 7), 1)
        pygame.draw.line(s, (255,180,80), (11, 7), (14, 7), 1)
        pygame.draw.line(s, (255,180,80), (7, 2), (7, 5), 1)
        pygame.draw.line(s, (255,180,80), (7, 11), (7, 14), 1)
    elif name == "export":
        pygame.draw.rect(s, (100,200,100), (3, 6, 10, 8), 1)
        pygame.draw.polygon(s, (100,200,100), [(8, 1), (12, 5), (4, 5)])
        pygame.draw.rect(s, (100,200,100), (6, 5, 4, 4))
    return s

icons = {n: make_icon(n) for n in ["new","open","save","undo","redo","play","stop","grid",
                                    "layers","events","select","eraser","hand","zoom_in","zoom_out",
                                    "eyedropper","copy","paste","bounds","export"]}

# ---------------- GAME ASSETS ----------------
def create_block_ground():
    s = pygame.Surface((TILE, TILE))
    s.fill((176, 96, 0))
    pygame.draw.rect(s, (248, 184, 104), (0, 0, 32, 3))
    pygame.draw.rect(s, (104, 56, 0), (0, 29, 32, 3))
    return s

def create_block_brick():
    s = pygame.Surface((TILE, TILE))
    s.fill((184, 72, 24))
    for row in range(2):
        y = row * 16
        for c in range(3):
            x = (8 if row else 0) + c * 16 - 8
            if 0 <= x < 32:
                pygame.draw.rect(s, (248,144,88), (x, y, 14, 2))
                pygame.draw.rect(s, (104,40,0), (x, y+14, 16, 2))
    return s

def create_block_question():
    s = pygame.Surface((TILE, TILE))
    s.fill((248, 184, 0))
    pygame.draw.rect(s, (255,232,128), (0, 0, 32, 3))
    pygame.draw.rect(s, (184,112,0), (0, 29, 32, 3))
    pygame.draw.rect(s, (255,255,255), (11, 5, 10, 3))
    pygame.draw.rect(s, (255,255,255), (18, 8, 3, 5))
    pygame.draw.rect(s, (255,255,255), (12, 13, 6, 3))
    pygame.draw.rect(s, (255,255,255), (12, 22, 3, 4))
    return s

def create_block_stone():
    s = pygame.Surface((TILE, TILE))
    s.fill((96, 96, 96))
    pygame.draw.rect(s, (168,168,168), (0, 0, 32, 2))
    pygame.draw.rect(s, (48,48,48), (0, 30, 32, 2))
    return s

def create_block_coin():
    s = pygame.Surface((TILE, TILE), pygame.SRCALPHA)
    pygame.draw.ellipse(s, (255, 200, 50), (8, 4, 16, 24))
    pygame.draw.ellipse(s, (255, 230, 100), (10, 6, 12, 20))
    pygame.draw.ellipse(s, (255, 200, 50), (12, 8, 8, 16))
    return s

def create_goal_pole():
    s = pygame.Surface((TILE, TILE * 8), pygame.SRCALPHA)
    # Pole
    pygame.draw.rect(s, (60, 60, 60), (14, 0, 4, TILE * 8))
    pygame.draw.rect(s, (100, 100, 100), (14, 0, 2, TILE * 8))
    # Ball on top
    pygame.draw.circle(s, (50, 200, 50), (16, 8), 8)
    pygame.draw.circle(s, (80, 230, 80), (14, 6), 3)
    # Flag
    pygame.draw.polygon(s, (50, 200, 50), [(18, 12), (18, 44), (48, 28)])
    pygame.draw.polygon(s, (80, 230, 80), [(18, 12), (18, 28), (33, 20)])
    return s

def create_goomba():
    s = pygame.Surface((TILE, TILE), pygame.SRCALPHA)
    pygame.draw.ellipse(s, (168, 80, 32), (4, 8, 24, 20))
    pygame.draw.ellipse(s, (96, 40, 0), (6, 2, 20, 14))
    pygame.draw.ellipse(s, (255,255,255), (6, 6, 8, 10))
    pygame.draw.ellipse(s, (255,255,255), (18, 6, 8, 10))
    pygame.draw.ellipse(s, (0,0,0), (10, 10, 4, 6))
    pygame.draw.ellipse(s, (0,0,0), (18, 10, 4, 6))
    pygame.draw.ellipse(s, (0,0,0), (2, 26, 12, 6))
    pygame.draw.ellipse(s, (0,0,0), (18, 26, 12, 6))
    return s

def create_koopa():
    s = pygame.Surface((TILE, TILE), pygame.SRCALPHA)
    pygame.draw.ellipse(s, (32, 168, 32), (4, 10, 24, 18))
    pygame.draw.ellipse(s, (72, 200, 72), (8, 12, 16, 12))
    pygame.draw.ellipse(s, (255, 216, 168), (8, 2, 12, 12))
    pygame.draw.ellipse(s, (0,0,0), (14, 6, 3, 3))
    pygame.draw.ellipse(s, (255, 216, 168), (4, 26, 10, 6))
    pygame.draw.ellipse(s, (255, 216, 168), (18, 26, 10, 6))
    return s

def create_mario():
    s = pygame.Surface((TILE, TILE), pygame.SRCALPHA)
    skin, red, brown = (255, 200, 148), (228, 52, 52), (128, 56, 0)
    pygame.draw.rect(s, red, (8, 4, 16, 6))
    pygame.draw.rect(s, skin, (8, 10, 14, 10))
    pygame.draw.rect(s, brown, (6, 10, 4, 6))
    pygame.draw.rect(s, (0,0,0), (10, 12, 3, 3))
    pygame.draw.rect(s, (0,0,0), (16, 12, 3, 3))
    pygame.draw.rect(s, red, (6, 20, 20, 6))
    pygame.draw.rect(s, (32, 64, 200), (8, 24, 16, 6))
    pygame.draw.rect(s, brown, (4, 28, 8, 4))
    pygame.draw.rect(s, brown, (18, 28, 8, 4))
    return s

assets = {
    "Blocks": {1: ("Ground", create_block_ground()), 2: ("Brick", create_block_brick()),
               3: ("? Block", create_block_question()), 4: ("Stone", create_block_stone()),
               5: ("Coin", create_block_coin())},
    "NPCs": {1: ("Goomba", create_goomba()), 2: ("Koopa", create_koopa())},
    "Special": {100: ("Goal Pole", create_goal_pole())},
    "BGOs": {}
}

player_img = create_mario()
player_img_flip = pygame.transform.flip(player_img, True, False)

# ---------------- UI / CLASSES ----------------
class Button:
    def __init__(self, x, y, w, h, text="", icon=None, toggle=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.text, self.icon, self.toggle = text, icon, toggle
        self.active, self.hover, self.enabled = False, False, True
    
    def update(self, mx, my, clicked):
        self.hover = self.rect.collidepoint(mx, my) and self.enabled
        if self.hover and clicked:
            if self.toggle: self.active = not self.active
            return True
        return False
    
    def draw(self, surf):
        col = C_BUTTON_HOVER if self.hover else (C_TAB_ACTIVE if self.active else C_BUTTON)
        pygame.draw.rect(surf, col, self.rect)
        if self.active: pygame.draw.rect(surf, C_ACCENT, self.rect, 1)
        cx, cy = self.rect.center
        if self.icon and self.icon in icons:
            surf.blit(icons[self.icon], (cx - 8, cy - 8))
        elif self.text:
            txt = FONT.render(self.text, True, C_TEXT)
            surf.blit(txt, (cx - txt.get_width()//2, cy - txt.get_height()//2))

class TabBar:
    def __init__(self, x, y, w, tabs):
        self.x, self.y, self.w, self.tabs = x, y, w, tabs
        self.active = 0
        self.tab_w = min(80, w // len(tabs))
    
    def update(self, mx, my, clicked):
        if self.y <= my <= self.y + 24:
            for i in range(len(self.tabs)):
                if self.x + i * self.tab_w <= mx <= self.x + (i+1) * self.tab_w and clicked:
                    self.active = i
                    return i
        return None
    
    def draw(self, surf):
        pygame.draw.rect(surf, C_PANEL_DARK, (self.x, self.y, self.w, 24))
        for i, tab in enumerate(self.tabs):
            tx = self.x + i * self.tab_w
            col = C_TAB_ACTIVE if i == self.active else C_TAB_INACTIVE
            pygame.draw.rect(surf, col, (tx, self.y, self.tab_w - 1, 24))
            if i == self.active:
                pygame.draw.rect(surf, C_ACCENT, (tx, self.y + 21, self.tab_w - 1, 3))
            txt = FONT_SM.render(tab, True, C_TEXT if i == self.active else C_TEXT_DIM)
            surf.blit(txt, (tx + (self.tab_w - txt.get_width())//2, self.y + 5))

class UndoManager:
    def __init__(self, max_history=20):
        self.history = []
        self.redo_stack = []
        self.max_history = max_history
    
    def save_state(self, level):
        state = {
            'blocks': copy.deepcopy(level.blocks),
            'npcs': copy.deepcopy(level.npcs),
            'specials': copy.deepcopy(level.specials),
            'coins': copy.deepcopy(level.coins)
        }
        self.history.append(state)
        if len(self.history) > self.max_history:
            self.history.pop(0)
        self.redo_stack.clear()
    
    def undo(self, level):
        if len(self.history) > 1:
            self.redo_stack.append(self.history.pop())
            state = self.history[-1]
            level.blocks = copy.deepcopy(state['blocks'])
            level.npcs = copy.deepcopy(state['npcs'])
            level.specials = copy.deepcopy(state['specials'])
            level.coins = copy.deepcopy(state['coins'])
            return True
        return False
    
    def redo(self, level):
        if self.redo_stack:
            state = self.redo_stack.pop()
            self.history.append(state)
            level.blocks = copy.deepcopy(state['blocks'])
            level.npcs = copy.deepcopy(state['npcs'])
            level.specials = copy.deepcopy(state['specials'])
            level.coins = copy.deepcopy(state['coins'])
            return True
        return False

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 24, 30)
        self.spawn_x, self.spawn_y = x, y
        self.vx, self.vy = 0, 0
        self.on_ground, self.facing = False, 1
        self.jump_held, self.jump_released = False, True
        self.coyote, self.jump_buffer, self.p_meter = 0, 0, 0
        self.running = False
        self.coins = 0
        self.lives = 3
        self.dead = False
        self.death_timer = 0
        self.won = False
        self.win_timer = 0

    def respawn(self):
        self.rect.x, self.rect.y = self.spawn_x, self.spawn_y
        self.vx, self.vy = 0, 0
        self.dead = False
        self.death_timer = 0
        self.on_ground = False

    def die(self):
        if not self.dead and not self.won:
            self.dead = True
            self.death_timer = 90
            self.lives -= 1
            self.vy = -10

    def update(self, blocks, coins_dict, specials):
        if self.won:
            self.win_timer -= 1
            return "win" if self.win_timer <= 0 else None
        
        if self.dead:
            self.vy += GRAVITY
            self.rect.y += int(self.vy)
            self.death_timer -= 1
            if self.death_timer <= 0:
                if self.lives > 0:
                    self.respawn()
                else:
                    return "gameover"
            return None
        
        keys = pygame.key.get_pressed()
        self.running = keys[pygame.K_x] or keys[pygame.K_LSHIFT]
        max_spd = MAX_RUN if self.running else MAX_WALK
        accel = ACCEL_RUN if self.running else ACCEL
        
        if keys[pygame.K_LEFT]: self.vx -= accel; self.facing = -1
        elif keys[pygame.K_RIGHT]: self.vx += accel; self.facing = 1
        
        if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]): self.vx *= FRICTION
        if abs(self.vx) < 0.05: self.vx = 0
        if abs(self.vx) > max_spd: self.vx = max_spd * (1 if self.vx > 0 else -1)
        
        if abs(self.vx) >= MAX_RUN - 0.5 and self.on_ground and self.running:
            self.p_meter = min(P_METER_MAX, self.p_meter + 1)
        else:
            self.p_meter = max(0, self.p_meter - 2)
        
        self.coyote = 6 if self.on_ground else max(0, self.coyote - 1)
        
        if keys[pygame.K_z] and self.jump_released:
            self.jump_buffer = 6
            self.jump_released = False
        elif not keys[pygame.K_z]:
            self.jump_released = True
        self.jump_buffer = max(0, self.jump_buffer - 1)
        
        if self.coyote > 0 and self.jump_buffer > 0 and not self.jump_held:
            self.vy = JUMP_FORCE_RUN if abs(self.vx) > MAX_WALK else JUMP_FORCE
            self.jump_held = True
            self.coyote = self.jump_buffer = 0
        
        if self.jump_held and not keys[pygame.K_z]: self.jump_held = False
        self.vy += GRAVITY_HOLD if (self.vy < 0 and self.jump_held and keys[pygame.K_z]) else GRAVITY
        if self.vy > 10: self.vy = 10
        
        self.rect.x += int(self.vx)
        self.collide(blocks, True)
        self.rect.y += int(self.vy)
        self.on_ground = False
        self.collide(blocks, False)
        
        # Collect coins
        player_tile = (self.rect.centerx // TILE, self.rect.centery // TILE)
        if player_tile in coins_dict:
            self.coins += 1
            del coins_dict[player_tile]
        
        # Check goal pole
        for pos, sid in list(specials.items()):
            if sid == 100:  # Goal pole
                goal_rect = pygame.Rect(pos[0]*TILE, pos[1]*TILE - TILE*7, TILE, TILE*8)
                if self.rect.colliderect(goal_rect):
                    self.won = True
                    self.win_timer = 120
        
        # Death by falling
        if self.rect.y > 2000:
            self.die()
        
        return None

    def collide(self, blocks, horizontal):
        for pos, bid in blocks.items():
            br = pygame.Rect(pos[0]*TILE, pos[1]*TILE, TILE, TILE)
            if self.rect.colliderect(br):
                if horizontal:
                    if self.vx > 0: self.rect.right = br.left
                    elif self.vx < 0: self.rect.left = br.right
                    self.vx = 0
                else:
                    if self.vy > 0: self.rect.bottom = br.top; self.vy = 0; self.on_ground = True
                    elif self.vy < 0: self.rect.top = br.bottom; self.vy = 0

    def stomp(self, hold): self.vy = -9.0 if hold else -5.0
    
    def draw(self, surf, cx, cy):
        if self.dead:
            # Spinning death animation
            angle = self.death_timer * 10
            img = pygame.transform.rotate(player_img if self.facing > 0 else player_img_flip, angle)
            surf.blit(img, (self.rect.x - cx - img.get_width()//2 + 12, self.rect.y - cy - img.get_height()//2 + 15))
        else:
            surf.blit(player_img if self.facing > 0 else player_img_flip, (self.rect.x - cx - 4, self.rect.y - cy - 2))

class Enemy:
    def __init__(self, x, y, eid):
        self.rect = pygame.Rect(x, y, 28, 30)
        self.id, self.vx, self.vy = eid, -1.5, 0
        self.alive, self.squish = True, 0

    def update(self, blocks):
        if self.squish > 0:
            self.squish -= 1
            if self.squish <= 0: self.alive = False
            return
        self.vy += GRAVITY
        self.rect.x += int(self.vx)
        for pos, _ in blocks.items():
            br = pygame.Rect(pos[0]*TILE, pos[1]*TILE, TILE, TILE)
            if self.rect.colliderect(br):
                if self.vx > 0: self.rect.right = br.left
                elif self.vx < 0: self.rect.left = br.right
                self.vx *= -1
        self.rect.y += int(self.vy)
        for pos, _ in blocks.items():
            br = pygame.Rect(pos[0]*TILE, pos[1]*TILE, TILE, TILE)
            if self.rect.colliderect(br) and self.vy > 0:
                self.rect.bottom = br.top; self.vy = 0

    def stomp(self): self.squish = 15; self.vx = 0
    def draw(self, surf, cx, cy):
        if self.id in assets["NPCs"]:
            img = assets["NPCs"][self.id][1]
            if self.squish > 0:
                img = pygame.transform.scale(img, (TILE, 8))
                surf.blit(img, (self.rect.x - cx, self.rect.y - cy + 24))
            else:
                surf.blit(img, (self.rect.x - cx - 2, self.rect.y - cy - 2))

class Level:
    def __init__(self):
        self.blocks, self.npcs, self.bgos = {}, {}, {}
        self.specials = {}  # Goal poles etc
        self.coins = {}  # Separate coin layer for gameplay
        self.cx, self.cy = 0, 0
        self.layers = ["Default", "Foreground", "Background"]
        self.current_layer = 0
        self.filename = "Untitled"
        # Level bounds (in tiles)
        self.bounds_x, self.bounds_y = 0, 0
        self.bounds_w, self.bounds_h = 80, 25  # Default: 80x25 tiles

    def save(self, fn):
        data = {"format": "ACSMBX2", "version": VERSION,
                "bounds": {"x": self.bounds_x, "y": self.bounds_y, "w": self.bounds_w, "h": self.bounds_h},
                "blocks": [{"x": x*32, "y": y*32, "id": i} for (x,y), i in self.blocks.items()],
                "npcs": [{"x": x*32, "y": y*32, "id": i} for (x,y), i in self.npcs.items()],
                "specials": [{"x": x*32, "y": y*32, "id": i} for (x,y), i in self.specials.items()],
                "coins": [{"x": x*32, "y": y*32} for (x,y) in self.coins.keys()]}
        with open(fn, "w") as f: json.dump(data, f, indent=2)
        self.filename = os.path.basename(fn)

    def load(self, fn):
        if not os.path.exists(fn): return False
        with open(fn, "r") as f: data = json.load(f)
        self.blocks = {(b["x"]//32, b["y"]//32): b["id"] for b in data.get("blocks", [])}
        self.npcs = {(n["x"]//32, n["y"]//32): n["id"] for n in data.get("npcs", [])}
        self.specials = {(s["x"]//32, s["y"]//32): s["id"] for s in data.get("specials", [])}
        self.coins = {(c["x"]//32, c["y"]//32): 5 for c in data.get("coins", [])}
        if "bounds" in data:
            b = data["bounds"]
            self.bounds_x, self.bounds_y = b.get("x", 0), b.get("y", 0)
            self.bounds_w, self.bounds_h = b.get("w", 80), b.get("h", 25)
        self.filename = os.path.basename(fn)
        return True

    def export_smbx(self, fn):
        """Export to SMBX .lvl format (simplified)"""
        lines = []
        lines.append("SMBXFile64")
        lines.append("Version=64")
        lines.append("")
        
        # Section header (simplified)
        lines.append("[Level]")
        lines.append(f"Title={self.filename}")
        lines.append(f"StartX={self.bounds_x * 32 + 100}")
        lines.append(f"StartY={self.bounds_y * 32 + 100}")
        lines.append("")
        
        # Blocks
        lines.append("[Blocks]")
        block_map = {1: 1, 2: 6, 3: 4, 4: 2}  # Map to SMBX block IDs
        for (x, y), bid in self.blocks.items():
            smbx_id = block_map.get(bid, 1)
            lines.append(f"{x*32},{y*32},{smbx_id},0,0,0")
        lines.append("")
        
        # NPCs
        lines.append("[NPCs]")
        npc_map = {1: 1, 2: 2}  # Goomba=1, Koopa=2 in SMBX
        for (x, y), nid in self.npcs.items():
            smbx_id = npc_map.get(nid, 1)
            lines.append(f"{x*32},{y*32},{smbx_id},-1,0,0,0,0,0,0")
        lines.append("")
        
        with open(fn, "w") as f:
            f.write("\n".join(lines))

# ---------------- EDITOR ----------------
def run_editor():
    global W, H, screen
    
    level = Level()
    player = Player(100, 300)
    enemies = []
    undo_mgr = UndoManager(20)
    
    mode, tool = "Editor", "place"
    edit_category, edit_id = "Blocks", 1
    show_grid, show_layer_panel, show_bounds = True, True, True
    zoom = 1.0
    
    # Selection system
    selection_start = None
    selection_rect = None
    clipboard = {"blocks": {}, "npcs": {}, "specials": {}, "coins": {}}
    
    TOOLBAR_H, MENUBAR_H, STATUSBAR_H = 28, 24, 22
    LEFT_PANEL_W, RIGHT_PANEL_W = 200, 180
    
    # Save initial state
    undo_mgr.save_state(level)
    
    toolbar_buttons = [
        Button(4, MENUBAR_H + 4, 24, 20, icon="new"),
        Button(30, MENUBAR_H + 4, 24, 20, icon="open"),
        Button(56, MENUBAR_H + 4, 24, 20, icon="save"),
        None,
        Button(90, MENUBAR_H + 4, 24, 20, icon="undo"),
        Button(116, MENUBAR_H + 4, 24, 20, icon="redo"),
        None,
        Button(150, MENUBAR_H + 4, 24, 20, icon="select", toggle=True),
        Button(176, MENUBAR_H + 4, 24, 20, icon="eraser", toggle=True),
        Button(202, MENUBAR_H + 4, 24, 20, icon="hand", toggle=True),
        Button(228, MENUBAR_H + 4, 24, 20, icon="eyedropper", toggle=True),
        None,
        Button(262, MENUBAR_H + 4, 24, 20, icon="copy"),
        Button(288, MENUBAR_H + 4, 24, 20, icon="paste"),
        None,
        Button(322, MENUBAR_H + 4, 24, 20, icon="grid", toggle=True),
        Button(348, MENUBAR_H + 4, 24, 20, icon="bounds", toggle=True),
        Button(374, MENUBAR_H + 4, 24, 20, icon="layers", toggle=True),
        None,
        Button(408, MENUBAR_H + 4, 24, 20, icon="zoom_in"),
        Button(434, MENUBAR_H + 4, 24, 20, icon="zoom_out"),
        None,
        Button(468, MENUBAR_H + 4, 50, 20, icon="play"),
        None,
        Button(530, MENUBAR_H + 4, 24, 20, icon="export"),
    ]
    toolbar_buttons[15].active = True  # grid
    toolbar_buttons[16].active = True  # bounds
    toolbar_buttons[17].active = True  # layers
    
    palette_tabs = TabBar(0, MENUBAR_H + TOOLBAR_H, LEFT_PANEL_W, ["Blocks", "NPCs", "Special"])
    menus = ["File", "Edit", "View", "Level", "Test", "Help"]
    
    # Default level content
    for x in range(5, 30): level.blocks[(x, 14)] = 1
    for x in range(12, 18): level.blocks[(x, 10)] = 2
    level.blocks[(15, 10)] = 3
    level.npcs[(20, 13)] = 1
    level.coins[(10, 13)] = 5
    level.coins[(11, 13)] = 5
    level.coins[(12, 13)] = 5
    level.specials[(28, 6)] = 100  # Goal pole
    
    undo_mgr.save_state(level)
    
    pygame.display.set_caption(f"{BRAND_NAME} {VERSION} - Editor")
    
    # Mouse-centered zoom tracking
    last_zoom_mx, last_zoom_my = W//2, H//2
    
    running = True
    while running:
        clock.tick(FPS)
        mx, my = pygame.mouse.get_pos()
        clicked, right_clicked, scroll_delta = False, False, 0
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return "quit"
            if e.type == pygame.VIDEORESIZE:
                W, H = e.w, e.h
                screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1: clicked = True
                if e.button == 3: right_clicked = True
                if e.button == 4: scroll_delta = 1  # Zoom in
                if e.button == 5: scroll_delta = -1  # Zoom out
            if e.type == pygame.MOUSEBUTTONUP:
                if e.button == 1 and selection_start and tool == "select":
                    selection_start = None
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    if mode == "Play": mode = "Editor"
                    elif selection_rect:
                        selection_rect = None
                    else: return "menu"
                if e.key == pygame.K_F5 or (e.key == pygame.K_RETURN and mode == "Editor"):
                    if mode == "Editor":
                        mode = "Play"
                        # Copy coins for gameplay
                        play_coins = copy.deepcopy(level.coins)
                        # Add coins from block layer
                        for pos, bid in level.blocks.items():
                            if bid == 5:  # Coin block
                                play_coins[pos] = 5
                        player = Player(level.bounds_x * TILE + 100, level.bounds_y * TILE + 200)
                        enemies = [Enemy(nx*TILE, ny*TILE, nid) for (nx,ny), nid in level.npcs.items()]
                    else:
                        mode = "Editor"
                if mode == "Editor":
                    mod = e.mod & (pygame.KMOD_CTRL | pygame.KMOD_META)
                    if e.key == pygame.K_s and mod: level.save("level.lvlx")
                    if e.key == pygame.K_o and mod: level.load("level.lvlx")
                    if e.key == pygame.K_z and mod:
                        if e.mod & pygame.KMOD_SHIFT:
                            undo_mgr.redo(level)
                        else:
                            undo_mgr.undo(level)
                    if e.key == pygame.K_y and mod:
                        undo_mgr.redo(level)
                    if e.key == pygame.K_c and mod and selection_rect:
                        # Copy selection
                        clipboard = {"blocks": {}, "npcs": {}, "specials": {}, "coins": {}}
                        sx1, sy1 = selection_rect[0]
                        sx2, sy2 = selection_rect[1]
                        for (x, y), bid in level.blocks.items():
                            if sx1 <= x <= sx2 and sy1 <= y <= sy2:
                                clipboard["blocks"][(x - sx1, y - sy1)] = bid
                        for (x, y), nid in level.npcs.items():
                            if sx1 <= x <= sx2 and sy1 <= y <= sy2:
                                clipboard["npcs"][(x - sx1, y - sy1)] = nid
                        for (x, y), sid in level.specials.items():
                            if sx1 <= x <= sx2 and sy1 <= y <= sy2:
                                clipboard["specials"][(x - sx1, y - sy1)] = sid
                        for (x, y), cid in level.coins.items():
                            if sx1 <= x <= sx2 and sy1 <= y <= sy2:
                                clipboard["coins"][(x - sx1, y - sy1)] = cid
                    if e.key == pygame.K_v and mod and clipboard["blocks"]:
                        # Paste at mouse position
                        vp_x = LEFT_PANEL_W
                        vp_y = MENUBAR_H + TOOLBAR_H
                        gx = int((mx - vp_x + level.cx) / TILE / zoom)
                        gy = int((my - vp_y + level.cy) / TILE / zoom)
                        undo_mgr.save_state(level)
                        for (dx, dy), bid in clipboard["blocks"].items():
                            level.blocks[(gx + dx, gy + dy)] = bid
                        for (dx, dy), nid in clipboard["npcs"].items():
                            level.npcs[(gx + dx, gy + dy)] = nid
                        for (dx, dy), sid in clipboard["specials"].items():
                            level.specials[(gx + dx, gy + dy)] = sid
                        for (dx, dy), cid in clipboard["coins"].items():
                            level.coins[(gx + dx, gy + dy)] = cid
                    if e.key == pygame.K_DELETE and selection_rect:
                        # Delete selection
                        undo_mgr.save_state(level)
                        sx1, sy1 = selection_rect[0]
                        sx2, sy2 = selection_rect[1]
                        for x in range(sx1, sx2 + 1):
                            for y in range(sy1, sy2 + 1):
                                level.blocks.pop((x, y), None)
                                level.npcs.pop((x, y), None)
                                level.specials.pop((x, y), None)
                                level.coins.pop((x, y), None)
                        selection_rect = None
                    if e.key == pygame.K_g: show_grid = not show_grid; toolbar_buttons[15].active = show_grid
                    if e.key == pygame.K_b: show_bounds = not show_bounds; toolbar_buttons[16].active = show_bounds

        vp_x, vp_y = LEFT_PANEL_W, MENUBAR_H + TOOLBAR_H
        vp_w = W - LEFT_PANEL_W - (RIGHT_PANEL_W if show_layer_panel else 0)
        vp_h = H - MENUBAR_H - TOOLBAR_H - STATUSBAR_H
        viewport = pygame.Rect(vp_x, vp_y, vp_w, vp_h)
        
        # Mouse-centered zoom
        if scroll_delta != 0 and viewport.collidepoint(mx, my) and mode == "Editor":
            # Get world position under mouse before zoom
            world_x = (mx - vp_x + level.cx) / zoom
            world_y = (my - vp_y + level.cy) / zoom
            
            # Apply zoom
            old_zoom = zoom
            if scroll_delta > 0:
                zoom = min(4.0, zoom * 1.25)
            else:
                zoom = max(0.25, zoom / 1.25)
            
            # Adjust camera so mouse stays over same world position
            level.cx = world_x * zoom - (mx - vp_x)
            level.cy = world_y * zoom - (my - vp_y)
        
        if mode == "Editor":
            keys = pygame.key.get_pressed()
            spd = 12 if keys[pygame.K_LSHIFT] else 6
            if tool == "hand" and pygame.mouse.get_pressed()[0] and viewport.collidepoint(mx, my):
                rel = pygame.mouse.get_rel()
                level.cx -= rel[0]; level.cy -= rel[1]
            else:
                pygame.mouse.get_rel()
                if keys[pygame.K_a] or keys[pygame.K_LEFT]: level.cx -= spd
                if keys[pygame.K_d] or keys[pygame.K_RIGHT]: level.cx += spd
                if keys[pygame.K_w] or keys[pygame.K_UP]: level.cy -= spd
                if keys[pygame.K_s] and not (pygame.key.get_mods() & (pygame.KMOD_CTRL|pygame.KMOD_META)): level.cy += spd
            
            if viewport.collidepoint(mx, my):
                gx = int((mx - vp_x + level.cx) / TILE / zoom)
                gy = int((my - vp_y + level.cy) / TILE / zoom)
                
                # Eyedropper (right-click or tool)
                if right_clicked or (tool == "eyedropper" and clicked):
                    # Pick tile under cursor
                    if (gx, gy) in level.blocks:
                        edit_category = "Blocks"
                        edit_id = level.blocks[(gx, gy)]
                        palette_tabs.active = 0
                        tool = "place"
                        for btn in toolbar_buttons[7:11]:
                            if btn: btn.active = False
                    elif (gx, gy) in level.npcs:
                        edit_category = "NPCs"
                        edit_id = level.npcs[(gx, gy)]
                        palette_tabs.active = 1
                        tool = "place"
                        for btn in toolbar_buttons[7:11]:
                            if btn: btn.active = False
                    elif (gx, gy) in level.specials:
                        edit_category = "Special"
                        edit_id = level.specials[(gx, gy)]
                        palette_tabs.active = 2
                        tool = "place"
                        for btn in toolbar_buttons[7:11]:
                            if btn: btn.active = False
                
                # Selection tool
                elif tool == "select":
                    if clicked:
                        selection_start = (gx, gy)
                    if pygame.mouse.get_pressed()[0] and selection_start:
                        sx1 = min(selection_start[0], gx)
                        sy1 = min(selection_start[1], gy)
                        sx2 = max(selection_start[0], gx)
                        sy2 = max(selection_start[1], gy)
                        selection_rect = ((sx1, sy1), (sx2, sy2))
                
                # Place tool
                elif pygame.mouse.get_pressed()[0] and tool == "place":
                    old_state = (copy.deepcopy(level.blocks), copy.deepcopy(level.npcs), 
                                copy.deepcopy(level.specials), copy.deepcopy(level.coins))
                    if edit_category == "Blocks":
                        if edit_id == 5:  # Coin
                            level.coins[(gx, gy)] = edit_id
                        else:
                            level.blocks[(gx, gy)] = edit_id
                    elif edit_category == "NPCs":
                        level.npcs[(gx, gy)] = edit_id
                    elif edit_category == "Special":
                        level.specials[(gx, gy)] = edit_id
                    # Only save undo if something changed
                    new_state = (level.blocks, level.npcs, level.specials, level.coins)
                    if old_state != new_state and clicked:
                        undo_mgr.save_state(level)
                
                # Erase
                if pygame.mouse.get_pressed()[2] or (pygame.mouse.get_pressed()[0] and tool == "erase"):
                    changed = False
                    if (gx, gy) in level.blocks: 
                        del level.blocks[(gx, gy)]
                        changed = True
                    if (gx, gy) in level.npcs:
                        del level.npcs[(gx, gy)]
                        changed = True
                    if (gx, gy) in level.specials:
                        del level.specials[(gx, gy)]
                        changed = True
                    if (gx, gy) in level.coins:
                        del level.coins[(gx, gy)]
                        changed = True
                    if changed and clicked:
                        undo_mgr.save_state(level)
            
            # Toolbar buttons
            for i, btn in enumerate(toolbar_buttons):
                if btn and btn.update(mx, my, clicked):
                    if i == 0:  # New
                        level = Level()
                        undo_mgr = UndoManager(20)
                        undo_mgr.save_state(level)
                    elif i == 1:  # Open
                        level.load("level.lvlx")
                        undo_mgr = UndoManager(20)
                        undo_mgr.save_state(level)
                    elif i == 2:  # Save
                        level.save("level.lvlx")
                    elif i == 4:  # Undo
                        undo_mgr.undo(level)
                    elif i == 5:  # Redo
                        undo_mgr.redo(level)
                    elif i == 7:  # Select
                        tool = "select"
                        for j in [8, 9, 10]:
                            if toolbar_buttons[j]: toolbar_buttons[j].active = False
                    elif i == 8:  # Eraser
                        tool = "erase"
                        for j in [7, 9, 10]:
                            if toolbar_buttons[j]: toolbar_buttons[j].active = False
                    elif i == 9:  # Hand
                        tool = "hand"
                        for j in [7, 8, 10]:
                            if toolbar_buttons[j]: toolbar_buttons[j].active = False
                    elif i == 10:  # Eyedropper
                        tool = "eyedropper"
                        for j in [7, 8, 9]:
                            if toolbar_buttons[j]: toolbar_buttons[j].active = False
                    elif i == 12:  # Copy
                        if selection_rect:
                            clipboard = {"blocks": {}, "npcs": {}, "specials": {}, "coins": {}}
                            sx1, sy1 = selection_rect[0]
                            sx2, sy2 = selection_rect[1]
                            for (x, y), bid in level.blocks.items():
                                if sx1 <= x <= sx2 and sy1 <= y <= sy2:
                                    clipboard["blocks"][(x - sx1, y - sy1)] = bid
                            for (x, y), nid in level.npcs.items():
                                if sx1 <= x <= sx2 and sy1 <= y <= sy2:
                                    clipboard["npcs"][(x - sx1, y - sy1)] = nid
                            for (x, y), sid in level.specials.items():
                                if sx1 <= x <= sx2 and sy1 <= y <= sy2:
                                    clipboard["specials"][(x - sx1, y - sy1)] = sid
                            for (x, y), cid in level.coins.items():
                                if sx1 <= x <= sx2 and sy1 <= y <= sy2:
                                    clipboard["coins"][(x - sx1, y - sy1)] = cid
                    elif i == 13:  # Paste
                        if clipboard["blocks"] or clipboard["npcs"] or clipboard["specials"] or clipboard["coins"]:
                            undo_mgr.save_state(level)
                            gx = int((mx - vp_x + level.cx) / TILE / zoom)
                            gy = int((my - vp_y + level.cy) / TILE / zoom)
                            for (dx, dy), bid in clipboard["blocks"].items():
                                level.blocks[(gx + dx, gy + dy)] = bid
                            for (dx, dy), nid in clipboard["npcs"].items():
                                level.npcs[(gx + dx, gy + dy)] = nid
                            for (dx, dy), sid in clipboard["specials"].items():
                                level.specials[(gx + dx, gy + dy)] = sid
                            for (dx, dy), cid in clipboard["coins"].items():
                                level.coins[(gx + dx, gy + dy)] = cid
                    elif i == 15:  # Grid
                        show_grid = btn.active
                    elif i == 16:  # Bounds
                        show_bounds = btn.active
                    elif i == 17:  # Layers
                        show_layer_panel = btn.active
                    elif i == 19:  # Zoom in
                        # Zoom centered on viewport center
                        cx_world = (vp_w/2 + level.cx) / zoom
                        cy_world = (vp_h/2 + level.cy) / zoom
                        zoom = min(4.0, zoom * 1.5)
                        level.cx = cx_world * zoom - vp_w/2
                        level.cy = cy_world * zoom - vp_h/2
                    elif i == 20:  # Zoom out
                        cx_world = (vp_w/2 + level.cx) / zoom
                        cy_world = (vp_h/2 + level.cy) / zoom
                        zoom = max(0.25, zoom / 1.5)
                        level.cx = cx_world * zoom - vp_w/2
                        level.cy = cy_world * zoom - vp_h/2
                    elif i == 22:  # Play
                        mode = "Play"
                        play_coins = copy.deepcopy(level.coins)
                        for pos, bid in level.blocks.items():
                            if bid == 5:
                                play_coins[pos] = 5
                        player = Player(level.bounds_x * TILE + 100, level.bounds_y * TILE + 200)
                        enemies = [Enemy(nx*TILE, ny*TILE, nid) for (nx,ny), nid in level.npcs.items()]
                    elif i == 24:  # Export
                        level.export_smbx("level.lvl")
            
            tab_result = palette_tabs.update(mx, my, clicked)
            if tab_result is not None:
                edit_category = ["Blocks", "NPCs", "Special"][tab_result]
                edit_id = list(assets.get(edit_category, {1: None}).keys())[0] if assets.get(edit_category) else 1
        
        elif mode == "Play":
            result = player.update(level.blocks, play_coins, level.specials)
            if result == "gameover":
                mode = "Editor"
            elif result == "win":
                mode = "Editor"
            
            for enemy in enemies[:]:
                if not enemy.alive: enemies.remove(enemy); continue
                enemy.update(level.blocks)
                if enemy.squish <= 0 and player.rect.colliderect(enemy.rect) and not player.dead:
                    if player.vy > 0 and player.rect.bottom - 8 < enemy.rect.centery:
                        enemy.stomp(); player.stomp(pygame.key.get_pressed()[pygame.K_z])
                    else:
                        player.die()
            
            if not player.dead and not player.won:
                level.cx += (player.rect.centerx - vp_w//2 - level.cx) * 0.08
                level.cy += (player.rect.centery - vp_h//2 - level.cy) * 0.06

        # Draw
        screen.fill(C_BG_DARK)
        game_surf = pygame.Surface((vp_w, vp_h))
        for y in range(vp_h):
            r = y / vp_h
            c = tuple(int(C_SKY[i] + (C_SKY_GRAD[i] - C_SKY[i]) * r) for i in range(3))
            pygame.draw.line(game_surf, c, (0, y), (vp_w, y))
        
        ox, oy = -int(level.cx), -int(level.cy)
        
        # Draw level bounds
        if show_bounds and mode == "Editor":
            bx = int(level.bounds_x * TILE * zoom + ox)
            by = int(level.bounds_y * TILE * zoom + oy)
            bw = int(level.bounds_w * TILE * zoom)
            bh = int(level.bounds_h * TILE * zoom)
            # Dim area outside bounds
            if by > 0:
                pygame.draw.rect(game_surf, (0, 0, 0, 100), (0, 0, vp_w, by))
            if by + bh < vp_h:
                pygame.draw.rect(game_surf, (0, 0, 0, 100), (0, by + bh, vp_w, vp_h - by - bh))
            if bx > 0:
                pygame.draw.rect(game_surf, (0, 0, 0, 100), (0, max(0, by), bx, bh))
            if bx + bw < vp_w:
                pygame.draw.rect(game_surf, (0, 0, 0, 100), (bx + bw, max(0, by), vp_w - bx - bw, bh))
            # Bounds border
            pygame.draw.rect(game_surf, (255, 180, 80), (bx, by, bw, bh), 2)
            # Corner handles for resize
            for cx, cy in [(bx, by), (bx + bw, by), (bx, by + bh), (bx + bw, by + bh)]:
                pygame.draw.rect(game_surf, (255, 200, 100), (cx - 4, cy - 4, 8, 8))
        
        # Draw blocks
        for (x, y), bid in level.blocks.items():
            if bid in assets["Blocks"]:
                img = assets["Blocks"][bid][1]
                if zoom != 1.0: img = pygame.transform.scale(img, (int(TILE*zoom), int(TILE*zoom)))
                game_surf.blit(img, (int(x*TILE*zoom + ox), int(y*TILE*zoom + oy)))
        
        # Draw coins
        for (x, y), cid in (play_coins if mode == "Play" else level.coins).items():
            if 5 in assets["Blocks"]:
                img = assets["Blocks"][5][1]
                if zoom != 1.0: img = pygame.transform.scale(img, (int(TILE*zoom), int(TILE*zoom)))
                game_surf.blit(img, (int(x*TILE*zoom + ox), int(y*TILE*zoom + oy)))
        
        # Draw specials (goal pole)
        for (x, y), sid in level.specials.items():
            if sid == 100:
                pole_img = create_goal_pole()
                if zoom != 1.0:
                    pole_img = pygame.transform.scale(pole_img, (int(TILE*zoom), int(TILE*8*zoom)))
                game_surf.blit(pole_img, (int(x*TILE*zoom + ox), int((y - 7)*TILE*zoom + oy)))
        
        # Draw NPCs (editor mode)
        if mode == "Editor":
            for (x, y), nid in level.npcs.items():
                if nid in assets["NPCs"]:
                    img = assets["NPCs"][nid][1]
                    if zoom != 1.0: img = pygame.transform.scale(img, (int(TILE*zoom), int(TILE*zoom)))
                    game_surf.blit(img, (int(x*TILE*zoom + ox), int(y*TILE*zoom + oy)))
        
        # Draw grid
        if show_grid and mode == "Editor":
            g_size = int(TILE * zoom)
            if g_size >= 4:
                for x in range(int(ox % g_size), vp_w, g_size):
                    pygame.draw.line(game_surf, C_GRID_MINOR, (x, 0), (x, vp_h))
                for y in range(int(oy % g_size), vp_h, g_size):
                    pygame.draw.line(game_surf, C_GRID_MINOR, (0, y), (vp_w, y))
        
        # Draw selection rectangle
        if selection_rect and mode == "Editor":
            sx1, sy1 = selection_rect[0]
            sx2, sy2 = selection_rect[1]
            rx = int(sx1 * TILE * zoom + ox)
            ry = int(sy1 * TILE * zoom + oy)
            rw = int((sx2 - sx1 + 1) * TILE * zoom)
            rh = int((sy2 - sy1 + 1) * TILE * zoom)
            sel_surf = pygame.Surface((rw, rh), pygame.SRCALPHA)
            sel_surf.fill((0, 180, 255, 50))
            game_surf.blit(sel_surf, (rx, ry))
            pygame.draw.rect(game_surf, C_SELECTION, (rx, ry, rw, rh), 2)
        
        # Draw enemies and player (play mode)
        if mode == "Play":
            for enemy in enemies: enemy.draw(game_surf, level.cx, level.cy)
            player.draw(game_surf, level.cx, level.cy)
        
        screen.blit(game_surf, (vp_x, vp_y))
        
        # UI
        pygame.draw.rect(screen, C_PANEL_DARK, (0, 0, W, MENUBAR_H))
        screen.blit(FONT_MD.render(BRAND_NAME, True, C_ACCENT), (8, 4))
        menu_x = 120
        for menu in menus:
            txt = FONT.render(menu, True, C_TEXT)
            screen.blit(txt, (menu_x, 5))
            menu_x += txt.get_width() + 16
        
        pygame.draw.rect(screen, C_PANEL, (0, MENUBAR_H, W, TOOLBAR_H))
        for btn in toolbar_buttons:
            if btn: btn.draw(screen)
        
        pygame.draw.rect(screen, C_PANEL, (0, MENUBAR_H + TOOLBAR_H, LEFT_PANEL_W, H - MENUBAR_H - TOOLBAR_H - STATUSBAR_H))
        palette_tabs.draw(screen)
        
        pal_y = MENUBAR_H + TOOLBAR_H + 28
        current_assets = assets.get(edit_category, {})
        for item_id, (name, img) in current_assets.items():
            if pal_y < H - STATUSBAR_H - 10:
                is_sel = (edit_id == item_id)
                item_rect = pygame.Rect(8, pal_y, LEFT_PANEL_W - 16, 40)
                if is_sel: pygame.draw.rect(screen, C_TAB_ACTIVE, item_rect); pygame.draw.rect(screen, C_ACCENT, item_rect, 1)
                elif item_rect.collidepoint(mx, my): pygame.draw.rect(screen, C_PANEL_LIGHT, item_rect)
                if item_rect.collidepoint(mx, my) and clicked:
                    edit_id = item_id
                    tool = "place"
                    for j in [7, 8, 9, 10]:
                        if toolbar_buttons[j]: toolbar_buttons[j].active = False
                if img:
                    display_img = img
                    if img.get_height() > 36:
                        scale = 36 / img.get_height()
                        display_img = pygame.transform.scale(img, (int(img.get_width() * scale), 36))
                    screen.blit(display_img, (16, pal_y + 2))
                screen.blit(FONT.render(name, True, C_TEXT), (54, pal_y + 12))
            pal_y += 44
        
        if show_layer_panel:
            rp_x = W - RIGHT_PANEL_W
            pygame.draw.rect(screen, C_PANEL, (rp_x, MENUBAR_H + TOOLBAR_H, RIGHT_PANEL_W, H - MENUBAR_H - TOOLBAR_H - STATUSBAR_H))
            screen.blit(FONT_MD.render("LAYERS", True, C_TEXT), (rp_x + 10, MENUBAR_H + TOOLBAR_H + 10))
            for i, layer in enumerate(level.layers):
                ly = MENUBAR_H + TOOLBAR_H + 35 + i * 24
                col = C_TAB_ACTIVE if i == level.current_layer else C_PANEL
                pygame.draw.rect(screen, col, (rp_x + 8, ly, RIGHT_PANEL_W - 16, 22))
                screen.blit(FONT.render(layer, True, C_TEXT), (rp_x + 32, ly + 4))
            
            # Level bounds controls
            bounds_y = MENUBAR_H + TOOLBAR_H + 120
            screen.blit(FONT_MD.render("LEVEL SIZE", True, C_TEXT), (rp_x + 10, bounds_y))
            screen.blit(FONT_SM.render(f"Width: {level.bounds_w} tiles", True, C_TEXT_DIM), (rp_x + 10, bounds_y + 20))
            screen.blit(FONT_SM.render(f"Height: {level.bounds_h} tiles", True, C_TEXT_DIM), (rp_x + 10, bounds_y + 36))
            
            # + / - buttons for width
            btn_w_minus = pygame.Rect(rp_x + 120, bounds_y + 18, 20, 16)
            btn_w_plus = pygame.Rect(rp_x + 145, bounds_y + 18, 20, 16)
            pygame.draw.rect(screen, C_BUTTON_HOVER if btn_w_minus.collidepoint(mx, my) else C_BUTTON, btn_w_minus)
            pygame.draw.rect(screen, C_BUTTON_HOVER if btn_w_plus.collidepoint(mx, my) else C_BUTTON, btn_w_plus)
            screen.blit(FONT_SM.render("-", True, C_TEXT), (btn_w_minus.x + 6, btn_w_minus.y + 1))
            screen.blit(FONT_SM.render("+", True, C_TEXT), (btn_w_plus.x + 5, btn_w_plus.y + 1))
            if clicked:
                if btn_w_minus.collidepoint(mx, my): level.bounds_w = max(20, level.bounds_w - 5)
                if btn_w_plus.collidepoint(mx, my): level.bounds_w = min(500, level.bounds_w + 5)
            
            # + / - buttons for height
            btn_h_minus = pygame.Rect(rp_x + 120, bounds_y + 34, 20, 16)
            btn_h_plus = pygame.Rect(rp_x + 145, bounds_y + 34, 20, 16)
            pygame.draw.rect(screen, C_BUTTON_HOVER if btn_h_minus.collidepoint(mx, my) else C_BUTTON, btn_h_minus)
            pygame.draw.rect(screen, C_BUTTON_HOVER if btn_h_plus.collidepoint(mx, my) else C_BUTTON, btn_h_plus)
            screen.blit(FONT_SM.render("-", True, C_TEXT), (btn_h_minus.x + 6, btn_h_minus.y + 1))
            screen.blit(FONT_SM.render("+", True, C_TEXT), (btn_h_plus.x + 5, btn_h_plus.y + 1))
            if clicked:
                if btn_h_minus.collidepoint(mx, my): level.bounds_h = max(15, level.bounds_h - 5)
                if btn_h_plus.collidepoint(mx, my): level.bounds_h = min(200, level.bounds_h + 5)
        
        pygame.draw.rect(screen, C_PANEL_DARK, (0, H - STATUSBAR_H, W, STATUSBAR_H))
        status_text = f"Zoom: {int(zoom*100)}%  |  Tool: {tool}  |  Undo: {len(undo_mgr.history)-1}  |  {COPYRIGHT}"
        screen.blit(FONT_SM.render(status_text, True, C_TEXT_DIM), (8, H - STATUSBAR_H + 4))
        
        if mode == "Play":
            hud = pygame.Surface((vp_w, 50), pygame.SRCALPHA)
            hud.fill((0, 0, 0, 150))
            screen.blit(hud, (vp_x, vp_y))
            
            # Lives
            screen.blit(FONT_LG.render(f"♥ × {player.lives}", True, (255, 100, 100)), (vp_x + 20, vp_y + 8))
            
            # Coins
            screen.blit(FONT_LG.render(f"🪙 × {player.coins}", True, C_GOLD), (vp_x + 100, vp_y + 8))
            
            # P-meter
            pm_x = vp_x + 200
            pygame.draw.rect(screen, (40, 40, 40), (pm_x, vp_y + 10, 100, 16))
            pygame.draw.rect(screen, (100, 180, 255), (pm_x, vp_y + 10, int(player.p_meter / P_METER_MAX * 100), 16))
            pygame.draw.rect(screen, C_TEXT_DIM, (pm_x, vp_y + 10, 100, 16), 1)
            
            # Time
            screen.blit(FONT_LG.render("TIME: 300", True, C_TEXT), (vp_x + vp_w - 120, vp_y + 8))
            
            # Win message
            if player.won:
                win_surf = FONT_SPLASH.render("LEVEL CLEAR!", True, C_GOLD)
                screen.blit(win_surf, (vp_x + vp_w//2 - win_surf.get_width()//2, vp_y + vp_h//2 - 30))
            
            # Game over
            if player.lives <= 0 and player.dead:
                go_surf = FONT_SPLASH.render("GAME OVER", True, C_RED)
                screen.blit(go_surf, (vp_x + vp_w//2 - go_surf.get_width()//2, vp_y + vp_h//2 - 30))
            
            # Controls hint
            hint = FONT_SM.render("ESC = Exit  |  Z = Jump  |  X = Run  |  Arrows = Move", True, C_TEXT_DIM)
            screen.blit(hint, (vp_x + vp_w//2 - hint.get_width()//2, vp_y + 32))
        
        pygame.display.flip()
    
    return "quit"

# ---------------- MAIN ----------------
def main():
    run_splash_screen()
    
    while True:
        result, data = run_main_menu()
        
        if result == "quit":
            break
        elif result == "editor":
            editor_result = run_editor()
            if editor_result == "quit":
                break
        elif result == "play":
            # For now, just go to editor - could add episode player later
            print(f"Would play episode: {data['name']}")
            editor_result = run_editor()
            if editor_result == "quit":
                break
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
