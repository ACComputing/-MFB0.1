import pygame, sys, json, os, math, random

pygame.init()

# ---------------- CONFIG ----------------
W, H = 1280, 720
FPS = 60
TILE = 32

# Brand Info
BRAND_NAME = "AC'S SMBX2"
VERSION = "V0.1.1[A]"
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
except:
    FONT_SM = pygame.font.SysFont("Arial", 11)
    FONT = pygame.font.SysFont("Arial", 12)
    FONT_MD = pygame.font.SysFont("Arial", 13, bold=True)
    FONT_LG = pygame.font.SysFont("Arial", 14, bold=True)
    FONT_TITLE = pygame.font.SysFont("Arial", 16, bold=True)
    FONT_SPLASH = pygame.font.SysFont("Arial", 48, bold=True)
    FONT_SPLASH_SM = pygame.font.SysFont("Arial", 18)
    FONT_SPLASH_VER = pygame.font.SysFont("Arial", 24, bold=True)

# ---------------- SPLASH SCREEN ASSETS ----------------
def create_splash_mario(frame):
    """Create running Mario sprite for splash (N64DD style)"""
    s = pygame.Surface((32, 32), pygame.SRCALPHA)
    skin = (255, 200, 148)
    red = (228, 52, 52)
    brown = (128, 56, 0)
    blue = (32, 64, 200)
    
    # Animation frames (running cycle)
    leg_offset = [0, 2, 4, 2][frame % 4]
    arm_offset = [0, -2, 0, 2][frame % 4]
    
    # Hat
    pygame.draw.rect(s, red, (8, 2 + abs(leg_offset)//2, 16, 6))
    pygame.draw.rect(s, red, (6, 4 + abs(leg_offset)//2, 4, 4))
    # Face
    pygame.draw.rect(s, skin, (8, 8 + abs(leg_offset)//2, 14, 10))
    # Hair
    pygame.draw.rect(s, brown, (6, 8 + abs(leg_offset)//2, 4, 6))
    # Eyes
    pygame.draw.rect(s, (0,0,0), (10, 10 + abs(leg_offset)//2, 3, 3))
    pygame.draw.rect(s, (0,0,0), (16, 10 + abs(leg_offset)//2, 3, 3))
    # Shirt
    pygame.draw.rect(s, red, (6, 18, 20, 6))
    # Arms
    pygame.draw.rect(s, red, (2 + arm_offset, 18, 6, 4))
    pygame.draw.rect(s, red, (22 - arm_offset, 18, 6, 4))
    # Overalls
    pygame.draw.rect(s, blue, (8, 22, 16, 6))
    # Legs (running animation)
    pygame.draw.rect(s, blue, (6 - leg_offset, 26, 6, 6))
    pygame.draw.rect(s, blue, (18 + leg_offset, 26, 6, 6))
    # Feet
    pygame.draw.rect(s, brown, (4 - leg_offset, 30, 8, 4))
    pygame.draw.rect(s, brown, (18 + leg_offset, 30, 8, 4))
    
    return s

def create_n64_logo():
    """Create N64DD-style 'N' logo"""
    s = pygame.Surface((120, 120), pygame.SRCALPHA)
    
    # 3D N shape (simplified N64 style)
    # Main colors
    red = (228, 52, 52)
    green = (52, 180, 52)
    blue = (52, 100, 228)
    yellow = (255, 220, 0)
    
    # Draw chunky 3D N
    pts_front = [(20, 100), (20, 20), (40, 20), (60, 60), (60, 20), (100, 20), (100, 100), (80, 100), (80, 60), (60, 100), (40, 100), (40, 40), (40, 100)]
    
    # Shadow/3D effect
    offset = 6
    shadow_pts = [(p[0] + offset, p[1] + offset) for p in pts_front]
    pygame.draw.polygon(s, (40, 40, 40), shadow_pts)
    
    # Front face with gradient colors
    pygame.draw.polygon(s, red, pts_front[:4] + [(40, 100), (20, 100)])
    pygame.draw.polygon(s, green, [(40, 20), (60, 60), (60, 20)])
    pygame.draw.polygon(s, blue, [(60, 20), (100, 20), (100, 100), (80, 100), (80, 60), (60, 60)])
    pygame.draw.polygon(s, yellow, [(40, 40), (40, 100), (60, 100), (60, 60)])
    
    # Outline
    pygame.draw.polygon(s, (255, 255, 255), pts_front, 2)
    
    return s

def create_star_particle():
    """Create sparkle/star particle"""
    s = pygame.Surface((8, 8), pygame.SRCALPHA)
    pygame.draw.line(s, (255, 255, 200), (4, 0), (4, 8), 1)
    pygame.draw.line(s, (255, 255, 200), (0, 4), (8, 4), 1)
    pygame.draw.line(s, (255, 255, 150), (1, 1), (7, 7), 1)
    pygame.draw.line(s, (255, 255, 150), (7, 1), (1, 7), 1)
    return s

class SplashParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
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
    """N64DD-style splash screen with Mario running around logo"""
    global W, H, screen
    
    # Create assets
    n_logo = create_n64_logo()
    star_img = create_star_particle()
    mario_frames = [create_splash_mario(i) for i in range(4)]
    
    # Animation state
    phase = 0  # 0=fade in, 1=mario run, 2=text appear, 3=fade out
    timer = 0
    logo_alpha = 0
    logo_scale = 0.5
    logo_rotation = 0
    text_alpha = 0
    
    # Mario orbit
    mario_angle = 0
    mario_orbit_radius = 140
    mario_frame = 0
    mario_frame_timer = 0
    
    # Particles
    particles = []
    
    # Colors
    bg_color = (8, 8, 12)
    
    running = True
    skip = False
    
    while running:
        dt = clock.tick(FPS)
        timer += 1
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN or e.type == pygame.MOUSEBUTTONDOWN:
                if timer > 30:  # Allow skip after brief moment
                    skip = True
            if e.type == pygame.VIDEORESIZE:
                W, H = e.w, e.h
                screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
        
        # Phase transitions
        if phase == 0 and timer > 60:
            phase = 1
        elif phase == 1 and timer > 180:
            phase = 2
        elif phase == 2 and timer > 300:
            phase = 3
        elif phase == 3 and timer > 360:
            running = False
        
        if skip and timer > 30:
            running = False
        
        # Update animations based on phase
        if phase == 0:
            # Logo fades in and scales up with rotation
            logo_alpha = min(255, logo_alpha + 8)
            logo_scale = min(1.0, logo_scale + 0.02)
            logo_rotation = (logo_rotation + 8) % 360
        
        elif phase == 1:
            logo_alpha = 255
            logo_scale = 1.0
            logo_rotation *= 0.9  # Slow down rotation
            
            # Mario runs around logo
            mario_angle += 0.05
            mario_frame_timer += 1
            if mario_frame_timer > 6:
                mario_frame_timer = 0
                mario_frame = (mario_frame + 1) % 4
            
            # Spawn particles from Mario's feet
            if timer % 4 == 0:
                mx = W//2 + math.cos(mario_angle) * mario_orbit_radius
                my = H//2 + math.sin(mario_angle) * mario_orbit_radius * 0.5 + 20
                particles.append(SplashParticle(mx, my))
        
        elif phase == 2:
            # Text fades in
            text_alpha = min(255, text_alpha + 6)
            mario_angle += 0.03  # Slower orbit
            mario_frame_timer += 1
            if mario_frame_timer > 8:
                mario_frame_timer = 0
                mario_frame = (mario_frame + 1) % 4
        
        elif phase == 3:
            # Everything fades out
            logo_alpha = max(0, logo_alpha - 8)
            text_alpha = max(0, text_alpha - 8)
        
        # Update particles
        particles = [p for p in particles if p.update()]
        
        # ---- DRAW ----
        screen.fill(bg_color)
        
        # Draw starfield background
        random.seed(42)  # Consistent stars
        for i in range(50):
            sx = random.randint(0, W)
            sy = random.randint(0, H)
            brightness = random.randint(100, 255)
            twinkle = abs(math.sin((timer + i * 10) * 0.05)) * 55 + 200
            col = (int(brightness * twinkle / 255),) * 3
            pygame.draw.circle(screen, col, (sx, sy), random.randint(1, 2))
        random.seed()
        
        # Draw particles (behind logo)
        for p in particles:
            p.draw(screen, star_img)
        
        # Draw N logo (centered, scaled, rotated)
        if logo_alpha > 0:
            scaled_size = int(120 * logo_scale)
            logo_scaled = pygame.transform.scale(n_logo, (scaled_size, scaled_size))
            
            if abs(logo_rotation) > 0.5:
                logo_rotated = pygame.transform.rotate(logo_scaled, logo_rotation)
            else:
                logo_rotated = logo_scaled
            
            logo_rotated.set_alpha(logo_alpha)
            logo_rect = logo_rotated.get_rect(center=(W//2, H//2 - 30))
            screen.blit(logo_rotated, logo_rect)
        
        # Draw Mario running around logo
        if phase >= 1:
            mx = W//2 + math.cos(mario_angle) * mario_orbit_radius - 16
            my = H//2 + math.sin(mario_angle) * mario_orbit_radius * 0.5 - 16
            
            # Flip Mario based on direction
            mario_img = mario_frames[mario_frame]
            if math.cos(mario_angle) < 0:
                mario_img = pygame.transform.flip(mario_img, True, False)
            
            # Scale Mario based on Y position (pseudo-3D)
            scale = 0.8 + 0.4 * (math.sin(mario_angle) * 0.5 + 0.5)
            scaled_mario = pygame.transform.scale(mario_img, (int(32 * scale), int(32 * scale)))
            scaled_mario.set_alpha(logo_alpha)
            
            # Draw shadow
            shadow_surf = pygame.Surface((int(24 * scale), int(8 * scale)), pygame.SRCALPHA)
            pygame.draw.ellipse(shadow_surf, (0, 0, 0, 80), shadow_surf.get_rect())
            screen.blit(shadow_surf, (mx + 4, H//2 + mario_orbit_radius * 0.5 + 10))
            
            screen.blit(scaled_mario, (mx, my))
        
        # Draw text
        if text_alpha > 0:
            # Brand name
            brand_surf = FONT_SPLASH.render(BRAND_NAME, True, (255, 255, 255))
            brand_surf.set_alpha(text_alpha)
            brand_rect = brand_surf.get_rect(center=(W//2, H//2 + 80))
            screen.blit(brand_surf, brand_rect)
            
            # Version
            ver_surf = FONT_SPLASH_VER.render(VERSION, True, C_ACCENT)
            ver_surf.set_alpha(text_alpha)
            ver_rect = ver_surf.get_rect(center=(W//2, H//2 + 120))
            screen.blit(ver_surf, ver_rect)
            
            # Copyright
            copy_surf = FONT_SPLASH_SM.render(COPYRIGHT, True, (150, 150, 155))
            copy_surf.set_alpha(text_alpha)
            copy_rect = copy_surf.get_rect(center=(W//2, H//2 + 160))
            screen.blit(copy_surf, copy_rect)
            
            # Loading text
            dots = "." * ((timer // 20) % 4)
            load_surf = FONT_SM.render(f"Loading{dots}", True, (100, 100, 105))
            load_surf.set_alpha(text_alpha)
            screen.blit(load_surf, (W//2 - 30, H - 40))
        
        # Skip hint
        if timer > 60:
            skip_alpha = min(150, (timer - 60) * 2)
            skip_surf = FONT_SM.render("Press any key to skip", True, (80, 80, 85))
            skip_surf.set_alpha(skip_alpha)
            screen.blit(skip_surf, (W - 150, H - 25))
        
        pygame.display.flip()
    
    # Brief pause before editor
    pygame.time.wait(200)

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
    elif name == "section":
        pygame.draw.rect(s, (255,255,255), (2, 4, 5, 8), 1)
        pygame.draw.rect(s, (255,255,255), (9, 4, 5, 8), 1)
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
    elif name == "settings":
        pygame.draw.circle(s, (180,180,180), (8, 8), 3, 1)
        for i in range(8):
            a = i * 0.785
            pygame.draw.line(s, (180,180,180), (8+int(4*math.cos(a)), 8+int(4*math.sin(a))), 
                           (8+int(6*math.cos(a)), 8+int(6*math.sin(a))), 1)
    return s

icons = {n: make_icon(n) for n in ["new","open","save","undo","redo","play","stop","grid",
                                    "layers","events","section","select","eraser","hand",
                                    "zoom_in","zoom_out","settings"]}

# ---------------- BLOCK/NPC ASSETS ----------------
def create_block_ground():
    s = pygame.Surface((TILE, TILE))
    s.fill((176, 96, 0))
    pygame.draw.rect(s, (248, 184, 104), (0, 0, 32, 3))
    pygame.draw.rect(s, (248, 184, 104), (0, 0, 3, 32))
    pygame.draw.rect(s, (104, 56, 0), (0, 29, 32, 3))
    pygame.draw.rect(s, (104, 56, 0), (29, 0, 3, 32))
    return s

def create_block_brick():
    s = pygame.Surface((TILE, TILE))
    s.fill((184, 72, 24))
    for row in range(2):
        y = row * 16
        off = 8 if row else 0
        for c in range(3):
            x = off + c * 16 - 8
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
    pygame.draw.rect(s, (255,255,255), (12, 16, 3, 3))
    pygame.draw.rect(s, (255,255,255), (12, 22, 3, 4))
    return s

def create_block_stone():
    s = pygame.Surface((TILE, TILE))
    s.fill((96, 96, 96))
    pygame.draw.rect(s, (168,168,168), (0, 0, 32, 2))
    pygame.draw.rect(s, (48,48,48), (0, 30, 32, 2))
    return s

def create_block_wood():
    s = pygame.Surface((TILE, TILE))
    s.fill((160, 100, 50))
    for i in range(4):
        pygame.draw.line(s, (120, 70, 30), (0, 8+i*8), (32, 8+i*8), 1)
    return s

def create_block_pipe():
    s = pygame.Surface((TILE, TILE))
    s.fill((0, 168, 0))
    pygame.draw.rect(s, (0, 228, 0), (0, 0, 8, 32))
    pygame.draw.rect(s, (0, 100, 0), (24, 0, 8, 32))
    pygame.draw.rect(s, (0, 200, 0), (0, 0, 32, 8))
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
    pygame.draw.ellipse(s, (255,255,255), (12, 4, 6, 6))
    pygame.draw.ellipse(s, (0,0,0), (14, 6, 3, 3))
    pygame.draw.ellipse(s, (255, 216, 168), (4, 26, 10, 6))
    pygame.draw.ellipse(s, (255, 216, 168), (18, 26, 10, 6))
    return s

def create_piranha():
    s = pygame.Surface((TILE, TILE), pygame.SRCALPHA)
    pygame.draw.ellipse(s, (0, 160, 0), (4, 16, 24, 14))
    pygame.draw.ellipse(s, (200, 50, 50), (2, 2, 28, 16))
    pygame.draw.ellipse(s, (255, 255, 255), (4, 4, 24, 8))
    for i in range(5):
        pygame.draw.polygon(s, (255,255,255), [(6+i*5, 10), (8+i*5, 2), (10+i*5, 10)])
    return s

def create_mario():
    s = pygame.Surface((TILE, TILE), pygame.SRCALPHA)
    skin = (255, 200, 148)
    red = (228, 52, 52)
    brown = (128, 56, 0)
    pygame.draw.rect(s, red, (8, 4, 16, 6))
    pygame.draw.rect(s, red, (6, 6, 4, 4))
    pygame.draw.rect(s, skin, (8, 10, 14, 10))
    pygame.draw.rect(s, brown, (6, 10, 4, 6))
    pygame.draw.rect(s, (0,0,0), (10, 12, 3, 3))
    pygame.draw.rect(s, (0,0,0), (16, 12, 3, 3))
    pygame.draw.rect(s, red, (6, 20, 20, 6))
    pygame.draw.rect(s, (32, 64, 200), (8, 24, 16, 6))
    pygame.draw.rect(s, brown, (4, 28, 8, 4))
    pygame.draw.rect(s, brown, (18, 28, 8, 4))
    return s

def create_bush():
    s = pygame.Surface((64, 32), pygame.SRCALPHA)
    pygame.draw.ellipse(s, (0, 180, 0), (0, 8, 28, 24))
    pygame.draw.ellipse(s, (0, 200, 0), (16, 4, 32, 28))
    pygame.draw.ellipse(s, (0, 180, 0), (36, 8, 28, 24))
    return s

def create_cloud():
    s = pygame.Surface((64, 32), pygame.SRCALPHA)
    pygame.draw.ellipse(s, (255, 255, 255), (0, 12, 24, 20))
    pygame.draw.ellipse(s, (255, 255, 255), (12, 4, 32, 28))
    pygame.draw.ellipse(s, (255, 255, 255), (32, 8, 28, 24))
    return s

assets = {
    "Blocks": {
        1: ("Ground", create_block_ground()),
        2: ("Brick", create_block_brick()),
        3: ("? Block", create_block_question()),
        4: ("Stone", create_block_stone()),
        5: ("Wood", create_block_wood()),
        6: ("Pipe", create_block_pipe()),
    },
    "NPCs": {
        1: ("Goomba", create_goomba()),
        2: ("Koopa", create_koopa()),
        3: ("Piranha", create_piranha()),
    },
    "BGOs": {
        1: ("Bush", create_bush()),
        2: ("Cloud", create_cloud()),
    }
}

player_img = create_mario()
player_img_flip = pygame.transform.flip(player_img, True, False)

# ---------------- UI COMPONENTS ----------------
class Button:
    def __init__(self, x, y, w, h, text="", icon=None, toggle=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.icon = icon
        self.toggle = toggle
        self.active = False
        self.hover = False
        self.enabled = True
    
    def update(self, mx, my, clicked):
        self.hover = self.rect.collidepoint(mx, my) and self.enabled
        if self.hover and clicked:
            if self.toggle:
                self.active = not self.active
            return True
        return False
    
    def draw(self, surf):
        col = C_BUTTON_HOVER if self.hover else (C_TAB_ACTIVE if self.active else C_BUTTON)
        if not self.enabled:
            col = C_PANEL_DARK
        pygame.draw.rect(surf, col, self.rect)
        if self.active:
            pygame.draw.rect(surf, C_ACCENT, self.rect, 1)
        
        cx, cy = self.rect.center
        if self.icon and self.icon in icons:
            icon_surf = icons[self.icon]
            if not self.enabled:
                icon_surf = icon_surf.copy()
                icon_surf.set_alpha(80)
            surf.blit(icon_surf, (cx - 8, cy - 8))
        elif self.text:
            txt = FONT.render(self.text, True, C_TEXT if self.enabled else C_TEXT_DIM)
            surf.blit(txt, (cx - txt.get_width()//2, cy - txt.get_height()//2))

class TabBar:
    def __init__(self, x, y, w, tabs):
        self.x, self.y, self.w = x, y, w
        self.tabs = tabs
        self.active = 0
        self.tab_w = min(80, w // len(tabs))
    
    def update(self, mx, my, clicked):
        if self.y <= my <= self.y + 24:
            for i, tab in enumerate(self.tabs):
                tx = self.x + i * self.tab_w
                if tx <= mx <= tx + self.tab_w and clicked:
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

# ---------------- PLAYER ----------------
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 24, 30)
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.facing = 1
        self.jump_held = False
        self.jump_released = True
        self.coyote = 0
        self.jump_buffer = 0
        self.p_meter = 0
        self.running = False

    def update(self, blocks):
        keys = pygame.key.get_pressed()
        self.running = keys[pygame.K_x] or keys[pygame.K_LSHIFT]
        
        max_spd = MAX_RUN if self.running else MAX_WALK
        accel = ACCEL_RUN if self.running else ACCEL
        
        if keys[pygame.K_LEFT]:
            self.vx -= accel
            self.facing = -1
        elif keys[pygame.K_RIGHT]:
            self.vx += accel
            self.facing = 1
        
        if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
            self.vx *= FRICTION
        if abs(self.vx) < 0.05:
            self.vx = 0
        if abs(self.vx) > max_spd:
            self.vx = max_spd * (1 if self.vx > 0 else -1)
        
        if abs(self.vx) >= MAX_RUN - 0.5 and self.on_ground and self.running:
            self.p_meter = min(P_METER_MAX, self.p_meter + 1)
        else:
            self.p_meter = max(0, self.p_meter - 2)
        
        if self.on_ground:
            self.coyote = 6
        else:
            self.coyote = max(0, self.coyote - 1)
        
        if keys[pygame.K_z] and self.jump_released:
            self.jump_buffer = 6
            self.jump_released = False
        elif not keys[pygame.K_z]:
            self.jump_released = True
        self.jump_buffer = max(0, self.jump_buffer - 1)
        
        if self.coyote > 0 and self.jump_buffer > 0 and not self.jump_held:
            jf = JUMP_FORCE_RUN if abs(self.vx) > MAX_WALK else JUMP_FORCE
            self.vy = jf
            self.jump_held = True
            self.coyote = 0
            self.jump_buffer = 0
        
        if self.jump_held and not keys[pygame.K_z]:
            self.jump_held = False
        
        if self.vy < 0 and self.jump_held and keys[pygame.K_z]:
            self.vy += GRAVITY_HOLD
        else:
            self.vy += GRAVITY
        
        if self.vy > 10:
            self.vy = 10
        
        self.rect.x += int(self.vx)
        self.collide(blocks, True)
        self.rect.y += int(self.vy)
        self.on_ground = False
        self.collide(blocks, False)
        
        if self.rect.y > 2000:
            self.rect.x, self.rect.y = 100, 300
            self.vy = 0

    def collide(self, blocks, horizontal):
        for pos, bid in blocks.items():
            br = pygame.Rect(pos[0]*TILE, pos[1]*TILE, TILE, TILE)
            if self.rect.colliderect(br):
                if horizontal:
                    if self.vx > 0: self.rect.right = br.left
                    elif self.vx < 0: self.rect.left = br.right
                    self.vx = 0
                else:
                    if self.vy > 0:
                        self.rect.bottom = br.top
                        self.vy = 0
                        self.on_ground = True
                    elif self.vy < 0:
                        self.rect.top = br.bottom
                        self.vy = 0

    def stomp(self, hold):
        self.vy = -9.0 if hold else -5.0

    def draw(self, surf, cx, cy):
        img = player_img if self.facing > 0 else player_img_flip
        surf.blit(img, (self.rect.x - cx - 4, self.rect.y - cy - 2))

class Enemy:
    def __init__(self, x, y, eid):
        self.rect = pygame.Rect(x, y, 28, 30)
        self.id = eid
        self.vx = -1.5
        self.vy = 0
        self.alive = True
        self.squish = 0

    def update(self, blocks):
        if self.squish > 0:
            self.squish -= 1
            if self.squish <= 0:
                self.alive = False
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
                self.rect.bottom = br.top
                self.vy = 0

    def stomp(self):
        self.squish = 15
        self.vx = 0

    def draw(self, surf, cx, cy):
        if self.id in assets["NPCs"]:
            img = assets["NPCs"][self.id][1]
            if self.squish > 0:
                img = pygame.transform.scale(img, (TILE, 8))
                surf.blit(img, (self.rect.x - cx, self.rect.y - cy + 24))
            else:
                surf.blit(img, (self.rect.x - cx - 2, self.rect.y - cy - 2))

# ---------------- LEVEL ----------------
class Level:
    def __init__(self):
        self.blocks = {}
        self.npcs = {}
        self.bgos = {}
        self.cx = 0
        self.cy = 0
        self.sections = [(0, 0, 8000, 600)]
        self.current_section = 0
        self.layers = ["Default", "Foreground", "Background", "Water"]
        self.current_layer = 0
        self.events = ["Level Start", "P-Switch", "Boss Defeat"]
        self.filename = "Untitled"

    def save(self, fn):
        data = {
            "format": "ACSMBX2", "version": "0.1.1A",
            "blocks": [{"x": x*32, "y": y*32, "id": i} for (x,y), i in self.blocks.items()],
            "npcs": [{"x": x*32, "y": y*32, "id": i} for (x,y), i in self.npcs.items()],
            "bgos": [{"x": x*32, "y": y*32, "id": i} for (x,y), i in self.bgos.items()],
        }
        with open(fn, "w") as f:
            json.dump(data, f, indent=2)
        self.filename = os.path.basename(fn)

    def load(self, fn):
        if not os.path.exists(fn): return False
        with open(fn, "r") as f:
            data = json.load(f)
        self.blocks = {(b["x"]//32, b["y"]//32): b["id"] for b in data.get("blocks", [])}
        self.npcs = {(n["x"]//32, n["y"]//32): n["id"] for n in data.get("npcs", [])}
        self.bgos = {(b["x"]//32, b["y"]//32): b["id"] for b in data.get("bgos", [])}
        self.filename = os.path.basename(fn)
        return True

# ---------------- MAIN ----------------
def main():
    global W, H, screen
    
    # Run splash screen first
    run_splash_screen()
    
    level = Level()
    player = Player(100, 300)
    enemies = []
    
    mode = "Editor"
    tool = "place"
    edit_category = "Blocks"
    edit_id = 1
    show_grid = True
    show_layer_panel = True
    show_events_panel = False
    zoom = 1.0
    selection = []
    
    TOOLBAR_H = 28
    MENUBAR_H = 24
    STATUSBAR_H = 22
    LEFT_PANEL_W = 200
    RIGHT_PANEL_W = 180
    
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
        None,
        Button(236, MENUBAR_H + 4, 24, 20, icon="grid", toggle=True),
        Button(262, MENUBAR_H + 4, 24, 20, icon="layers", toggle=True),
        Button(288, MENUBAR_H + 4, 24, 20, icon="events", toggle=True),
        None,
        Button(322, MENUBAR_H + 4, 24, 20, icon="zoom_in"),
        Button(348, MENUBAR_H + 4, 24, 20, icon="zoom_out"),
        None,
        Button(382, MENUBAR_H + 4, 50, 20, icon="play"),
    ]
    toolbar_buttons[11].active = True
    toolbar_buttons[12].active = True
    
    palette_tabs = TabBar(0, MENUBAR_H + TOOLBAR_H, LEFT_PANEL_W, ["Blocks", "NPCs", "BGOs", "Warps"])
    menus = ["File", "Edit", "View", "Level", "Test", "Tools", "Help"]
    
    # Starter level
    for x in range(5, 30):
        level.blocks[(x, 14)] = 1
    for x in range(12, 18):
        level.blocks[(x, 10)] = 2
    level.blocks[(15, 10)] = 3
    level.npcs[(20, 13)] = 1
    
    running = True
    clicked = False
    scroll_y = 0
    
    pygame.display.set_caption(f"{BRAND_NAME} {VERSION} - {level.filename}")
    
    while running:
        dt = clock.tick(FPS)
        mx, my = pygame.mouse.get_pos()
        clicked = False
        scroll_delta = 0
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.VIDEORESIZE:
                W, H = e.w, e.h
                screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1: clicked = True
                if e.button == 4: scroll_delta = -30
                if e.button == 5: scroll_delta = 30
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_F5 or (e.key == pygame.K_RETURN and mode == "Editor"):
                    if mode == "Editor":
                        mode = "Play"
                        player = Player(level.cx + 200, level.cy + 200)
                        enemies = [Enemy(nx*TILE, ny*TILE, nid) for (nx,ny), nid in level.npcs.items()]
                        pygame.display.set_caption(f"{BRAND_NAME} - Testing: {level.filename}")
                    else:
                        mode = "Editor"
                        pygame.display.set_caption(f"{BRAND_NAME} {VERSION} - {level.filename}")
                
                if e.key == pygame.K_ESCAPE and mode == "Play":
                    mode = "Editor"
                    pygame.display.set_caption(f"{BRAND_NAME} {VERSION} - {level.filename}")
                
                if mode == "Editor":
                    mod = e.mod & (pygame.KMOD_CTRL | pygame.KMOD_META)
                    if e.key == pygame.K_s and mod:
                        level.save("level.lvlx")
                        pygame.display.set_caption(f"{BRAND_NAME} {VERSION} - {level.filename}")
                    if e.key == pygame.K_o and mod:
                        if level.load("level.lvlx"):
                            pygame.display.set_caption(f"{BRAND_NAME} {VERSION} - {level.filename}")
                    if e.key == pygame.K_g:
                        show_grid = not show_grid
                        toolbar_buttons[11].active = show_grid
                    if e.key == pygame.K_DELETE and selection:
                        for pos in selection:
                            level.blocks.pop(pos, None)
                            level.npcs.pop(pos, None)
                        selection = []
                    if e.key == pygame.K_v: tool = "select"
                    if e.key == pygame.K_b: tool = "place"
                    if e.key == pygame.K_e: tool = "erase"
                    if e.key == pygame.K_h: tool = "hand"
                    for i, k in enumerate([pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]):
                        if e.key == k and i < len(assets[edit_category]):
                            edit_id = i + 1

        vp_x = LEFT_PANEL_W
        vp_y = MENUBAR_H + TOOLBAR_H
        vp_w = W - LEFT_PANEL_W - (RIGHT_PANEL_W if show_layer_panel else 0)
        vp_h = H - MENUBAR_H - TOOLBAR_H - STATUSBAR_H
        viewport = pygame.Rect(vp_x, vp_y, vp_w, vp_h)
        
        if mode == "Editor":
            keys = pygame.key.get_pressed()
            spd = 12 if keys[pygame.K_LSHIFT] else 6
            
            if tool == "hand" and pygame.mouse.get_pressed()[0] and viewport.collidepoint(mx, my):
                rel = pygame.mouse.get_rel()
                level.cx -= rel[0]
                level.cy -= rel[1]
            else:
                pygame.mouse.get_rel()
                if keys[pygame.K_a] or keys[pygame.K_LEFT]: level.cx -= spd
                if keys[pygame.K_d] or keys[pygame.K_RIGHT]: level.cx += spd
                if keys[pygame.K_w] or keys[pygame.K_UP]: level.cy -= spd
                if keys[pygame.K_s] and not (pygame.key.get_mods() & (pygame.KMOD_CTRL|pygame.KMOD_META)):
                    level.cy += spd
            
            if viewport.collidepoint(mx, my):
                gx = int((mx - vp_x + level.cx) / TILE / zoom)
                gy = int((my - vp_y + level.cy) / TILE / zoom)
                
                if pygame.mouse.get_pressed()[0] and tool == "place":
                    if edit_category == "Blocks":
                        level.blocks[(gx, gy)] = edit_id
                    elif edit_category == "NPCs":
                        level.npcs[(gx, gy)] = edit_id
                    elif edit_category == "BGOs":
                        level.bgos[(gx, gy)] = edit_id
                
                if pygame.mouse.get_pressed()[2] or (pygame.mouse.get_pressed()[0] and tool == "erase"):
                    level.blocks.pop((gx, gy), None)
                    level.npcs.pop((gx, gy), None)
                    level.bgos.pop((gx, gy), None)
                
                if tool == "select" and clicked:
                    if (gx, gy) in level.blocks or (gx, gy) in level.npcs:
                        if (gx, gy) in selection:
                            selection.remove((gx, gy))
                        else:
                            selection.append((gx, gy))
            
            for i, btn in enumerate(toolbar_buttons):
                if btn and btn.update(mx, my, clicked):
                    if i == 0: level = Level(); pygame.display.set_caption(f"{BRAND_NAME} {VERSION} - Untitled")
                    elif i == 1 and level.load("level.lvlx"): pygame.display.set_caption(f"{BRAND_NAME} {VERSION} - {level.filename}")
                    elif i == 2: level.save("level.lvlx")
                    elif i == 7: tool = "select"; toolbar_buttons[8].active = False; toolbar_buttons[9].active = False
                    elif i == 8: tool = "erase"; toolbar_buttons[7].active = False; toolbar_buttons[9].active = False
                    elif i == 9: tool = "hand"; toolbar_buttons[7].active = False; toolbar_buttons[8].active = False
                    elif i == 11: show_grid = btn.active
                    elif i == 12: show_layer_panel = btn.active
                    elif i == 13: show_events_panel = btn.active
                    elif i == 15: zoom = min(4.0, zoom * 1.5)
                    elif i == 16: zoom = max(0.25, zoom / 1.5)
                    elif i == 18:
                        mode = "Play"
                        player = Player(level.cx + 200, level.cy + 200)
                        enemies = [Enemy(nx*TILE, ny*TILE, nid) for (nx,ny), nid in level.npcs.items()]
            
            tab_result = palette_tabs.update(mx, my, clicked)
            if tab_result is not None:
                edit_category = ["Blocks", "NPCs", "BGOs", "Warps"][tab_result]
                edit_id = 1
            
            if mx < LEFT_PANEL_W:
                scroll_y = max(0, scroll_y + scroll_delta)
        
        elif mode == "Play":
            player.update(level.blocks)
            for enemy in enemies[:]:
                if not enemy.alive:
                    enemies.remove(enemy)
                    continue
                enemy.update(level.blocks)
                if enemy.squish <= 0 and player.rect.colliderect(enemy.rect):
                    if player.vy > 0 and player.rect.bottom - 8 < enemy.rect.centery:
                        enemy.stomp()
                        player.stomp(pygame.key.get_pressed()[pygame.K_z])
                    else:
                        mode = "Editor"
                        pygame.display.set_caption(f"{BRAND_NAME} {VERSION} - {level.filename}")
            
            tx = player.rect.centerx - vp_w//2
            ty = player.rect.centery - vp_h//2
            level.cx += (tx - level.cx) * 0.08
            level.cy += (ty - level.cy) * 0.06

        # ---- DRAW ----
        screen.fill(C_BG_DARK)
        
        game_surf = pygame.Surface((vp_w, vp_h))
        for y in range(vp_h):
            r = y / vp_h
            c = (int(C_SKY[0]+(C_SKY_GRAD[0]-C_SKY[0])*r),
                 int(C_SKY[1]+(C_SKY_GRAD[1]-C_SKY[1])*r),
                 int(C_SKY[2]+(C_SKY_GRAD[2]-C_SKY[2])*r))
            pygame.draw.line(game_surf, c, (0, y), (vp_w, y))
        
        ox, oy = -int(level.cx * zoom), -int(level.cy * zoom)
        
        for (x, y), bid in level.bgos.items():
            if bid in assets["BGOs"] and assets["BGOs"][bid][1]:
                img = assets["BGOs"][bid][1]
                if zoom != 1.0:
                    img = pygame.transform.scale(img, (int(img.get_width()*zoom), int(img.get_height()*zoom)))
                game_surf.blit(img, (int(x*TILE*zoom + ox), int(y*TILE*zoom + oy)))
        
        for (x, y), bid in level.blocks.items():
            if bid in assets["Blocks"]:
                img = assets["Blocks"][bid][1]
                if zoom != 1.0:
                    img = pygame.transform.scale(img, (int(TILE*zoom), int(TILE*zoom)))
                game_surf.blit(img, (int(x*TILE*zoom + ox), int(y*TILE*zoom + oy)))
        
        if mode == "Editor":
            for (x, y), nid in level.npcs.items():
                if nid in assets["NPCs"]:
                    img = assets["NPCs"][nid][1]
                    if zoom != 1.0:
                        img = pygame.transform.scale(img, (int(TILE*zoom), int(TILE*zoom)))
                    game_surf.blit(img, (int(x*TILE*zoom + ox), int(y*TILE*zoom + oy)))
        
        for pos in selection:
            sx = int(pos[0]*TILE*zoom + ox)
            sy = int(pos[1]*TILE*zoom + oy)
            sel_surf = pygame.Surface((int(TILE*zoom), int(TILE*zoom)), pygame.SRCALPHA)
            sel_surf.fill((0, 122, 204, 80))
            game_surf.blit(sel_surf, (sx, sy))
            pygame.draw.rect(game_surf, C_ACCENT, (sx, sy, int(TILE*zoom), int(TILE*zoom)), 2)
        
        if show_grid and mode == "Editor":
            grid_surf = pygame.Surface((vp_w, vp_h), pygame.SRCALPHA)
            g_size = int(TILE * zoom)
            gx_off = ox % g_size
            gy_off = oy % g_size
            for x in range(gx_off, vp_w, g_size):
                col = C_GRID_MAJOR if ((x - gx_off) // g_size) % 4 == 0 else C_GRID_MINOR
                pygame.draw.line(grid_surf, (*col, 60), (x, 0), (x, vp_h))
            for y in range(gy_off, vp_h, g_size):
                col = C_GRID_MAJOR if ((y - gy_off) // g_size) % 4 == 0 else C_GRID_MINOR
                pygame.draw.line(grid_surf, (*col, 60), (0, y), (vp_w, y))
            game_surf.blit(grid_surf, (0, 0))
        
        if mode == "Play":
            for enemy in enemies:
                enemy.draw(game_surf, level.cx, level.cy)
            player.draw(game_surf, level.cx, level.cy)
        
        if mode == "Editor" and viewport.collidepoint(mx, my) and tool == "place":
            gx = int((mx - vp_x + level.cx) / TILE / zoom)
            gy = int((my - vp_y + level.cy) / TILE / zoom)
            px = int(gx*TILE*zoom + ox)
            py = int(gy*TILE*zoom + oy)
            preview = None
            if edit_category == "Blocks" and edit_id in assets["Blocks"]:
                preview = assets["Blocks"][edit_id][1]
            elif edit_category == "NPCs" and edit_id in assets["NPCs"]:
                preview = assets["NPCs"][edit_id][1]
            if preview:
                preview = preview.copy()
                preview.set_alpha(150)
                if zoom != 1.0:
                    preview = pygame.transform.scale(preview, (int(TILE*zoom), int(TILE*zoom)))
                game_surf.blit(preview, (px, py))
        
        screen.blit(game_surf, (vp_x, vp_y))
        
        # Menu bar with brand
        pygame.draw.rect(screen, C_PANEL_DARK, (0, 0, W, MENUBAR_H))
        brand_txt = FONT_MD.render(f"{BRAND_NAME}", True, C_ACCENT)
        screen.blit(brand_txt, (8, 4))
        menu_x = 120
        for menu in menus:
            txt = FONT.render(menu, True, C_TEXT)
            tw = txt.get_width() + 16
            if menu_x <= mx <= menu_x + tw and my < MENUBAR_H:
                pygame.draw.rect(screen, C_PANEL_LIGHT, (menu_x - 4, 0, tw, MENUBAR_H))
            screen.blit(txt, (menu_x, 5))
            menu_x += tw
        
        # Toolbar
        pygame.draw.rect(screen, C_PANEL, (0, MENUBAR_H, W, TOOLBAR_H))
        pygame.draw.line(screen, C_BORDER, (0, MENUBAR_H + TOOLBAR_H - 1), (W, MENUBAR_H + TOOLBAR_H - 1))
        for sx in [82, 142, 228, 314, 374]:
            pygame.draw.line(screen, C_BORDER, (sx, MENUBAR_H + 6), (sx, MENUBAR_H + TOOLBAR_H - 6))
        for btn in toolbar_buttons:
            if btn: btn.draw(screen)
        
        # Left panel
        pygame.draw.rect(screen, C_PANEL, (0, MENUBAR_H + TOOLBAR_H, LEFT_PANEL_W, H - MENUBAR_H - TOOLBAR_H - STATUSBAR_H))
        pygame.draw.line(screen, C_BORDER, (LEFT_PANEL_W - 1, MENUBAR_H + TOOLBAR_H), (LEFT_PANEL_W - 1, H - STATUSBAR_H))
        palette_tabs.draw(screen)
        
        pal_y = MENUBAR_H + TOOLBAR_H + 28 - scroll_y
        pal_items = assets.get(edit_category, {})
        for item_id, (name, img) in pal_items.items():
            if pal_y + 44 > MENUBAR_H + TOOLBAR_H + 28 and pal_y < H - STATUSBAR_H - 10:
                item_rect = pygame.Rect(8, pal_y, LEFT_PANEL_W - 16, 40)
                is_sel = (edit_id == item_id)
                is_hover = item_rect.collidepoint(mx, my)
                if is_sel:
                    pygame.draw.rect(screen, C_TAB_ACTIVE, item_rect)
                    pygame.draw.rect(screen, C_ACCENT, item_rect, 1)
                elif is_hover:
                    pygame.draw.rect(screen, C_PANEL_LIGHT, item_rect)
                if is_hover and clicked:
                    edit_id = item_id
                    tool = "place"
                    toolbar_buttons[7].active = False
                    toolbar_buttons[8].active = False
                    toolbar_buttons[9].active = False
                if img:
                    screen.blit(img, (16, pal_y + 4))
                screen.blit(FONT_SM.render(f"#{item_id}", True, C_TEXT_DIM), (54, pal_y + 4))
                screen.blit(FONT.render(name, True, C_TEXT if is_sel else C_TEXT_DIM), (54, pal_y + 18))
            pal_y += 44
        
        # Right panel
        if show_layer_panel:
            rp_x = W - RIGHT_PANEL_W
            pygame.draw.rect(screen, C_PANEL, (rp_x, MENUBAR_H + TOOLBAR_H, RIGHT_PANEL_W, H - MENUBAR_H - TOOLBAR_H - STATUSBAR_H))
            pygame.draw.line(screen, C_BORDER, (rp_x, MENUBAR_H + TOOLBAR_H), (rp_x, H - STATUSBAR_H))
            
            py = MENUBAR_H + TOOLBAR_H + 8
            pygame.draw.rect(screen, C_PANEL_DARK, (rp_x + 4, py, RIGHT_PANEL_W - 8, 20))
            screen.blit(FONT_MD.render("LAYERS", True, C_TEXT), (rp_x + 10, py + 3))
            py += 26
            
            for i, layer in enumerate(level.layers):
                lr = pygame.Rect(rp_x + 8, py, RIGHT_PANEL_W - 16, 22)
                is_active = (i == level.current_layer)
                if is_active:
                    pygame.draw.rect(screen, C_TAB_ACTIVE, lr)
                elif lr.collidepoint(mx, my):
                    pygame.draw.rect(screen, C_PANEL_LIGHT, lr)
                if lr.collidepoint(mx, my) and clicked:
                    level.current_layer = i
                pygame.draw.circle(screen, C_ACCENT, (rp_x + 20, py + 11), 4, 1)
                pygame.draw.circle(screen, C_ACCENT, (rp_x + 20, py + 11), 2)
                screen.blit(FONT.render(layer, True, C_TEXT if is_active else C_TEXT_DIM), (rp_x + 32, py + 4))
                py += 24
            
            py += 15
            pygame.draw.rect(screen, C_PANEL_DARK, (rp_x + 4, py, RIGHT_PANEL_W - 8, 20))
            screen.blit(FONT_MD.render("SECTIONS", True, C_TEXT), (rp_x + 10, py + 3))
            py += 26
            
            for i in range(len(level.sections)):
                sr = pygame.Rect(rp_x + 8, py, RIGHT_PANEL_W - 16, 20)
                is_active = (i == level.current_section)
                if is_active:
                    pygame.draw.rect(screen, C_TAB_ACTIVE, sr)
                elif sr.collidepoint(mx, my):
                    pygame.draw.rect(screen, C_PANEL_LIGHT, sr)
                if sr.collidepoint(mx, my) and clicked:
                    level.current_section = i
                    level.cx, level.cy = level.sections[i][0], level.sections[i][1]
                screen.blit(FONT.render(f"Section {i + 1}", True, C_TEXT if is_active else C_TEXT_DIM), (rp_x + 14, py + 3))
                py += 22
        
        # Status bar
        pygame.draw.rect(screen, C_PANEL_DARK, (0, H - STATUSBAR_H, W, STATUSBAR_H))
        pygame.draw.line(screen, C_BORDER, (0, H - STATUSBAR_H), (W, H - STATUSBAR_H))
        
        if viewport.collidepoint(mx, my):
            gx = int((mx - vp_x + level.cx) / TILE / zoom)
            gy = int((my - vp_y + level.cy) / TILE / zoom)
            screen.blit(FONT_SM.render(f"X: {gx*32}  Y: {gy*32}  |  Grid: ({gx}, {gy})", True, C_TEXT), (8, H - STATUSBAR_H + 4))
        else:
            screen.blit(FONT_SM.render("Ready", True, C_TEXT_DIM), (8, H - STATUSBAR_H + 4))
        
        screen.blit(FONT_SM.render(f"Zoom: {int(zoom*100)}%", True, C_TEXT_DIM), (220, H - STATUSBAR_H + 4))
        screen.blit(FONT_SM.render(f"Layer: {level.layers[level.current_layer]}", True, C_TEXT), (340, H - STATUSBAR_H + 4))
        screen.blit(FONT_SM.render(f"Tool: {tool.capitalize()}", True, C_ACCENT), (480, H - STATUSBAR_H + 4))
        
        # Copyright in status bar
        copy_txt = FONT_SM.render(COPYRIGHT, True, C_TEXT_DIM)
        screen.blit(copy_txt, (W - copy_txt.get_width() - 10, H - STATUSBAR_H + 4))
        
        if mode == "Play":
            screen.blit(FONT_MD.render("▶ TESTING - Press ESC to stop", True, C_SUCCESS), (W - 280, H - STATUSBAR_H + 3))
            
            # Play HUD
            hud = pygame.Surface((vp_w, 40), pygame.SRCALPHA)
            hud.fill((0, 0, 0, 120))
            screen.blit(hud, (vp_x, vp_y))
            screen.blit(FONT_LG.render("♥ × 3", True, (255, 100, 100)), (vp_x + 20, vp_y + 10))
            screen.blit(FONT_LG.render("🪙 × 0", True, (255, 220, 0)), (vp_x + 100, vp_y + 10))
            
            pm_x = vp_x + 200
            pygame.draw.rect(screen, (40, 40, 40), (pm_x, vp_y + 12, 140, 16))
            fill = int((player.p_meter / P_METER_MAX) * 140)
            col = (255, 200, 0) if player.p_meter >= P_METER_MAX else (100, 180, 255)
            pygame.draw.rect(screen, col, (pm_x, vp_y + 12, fill, 16))
            pygame.draw.rect(screen, (80, 80, 80), (pm_x, vp_y + 12, 140, 16), 1)
            
            for i in range(7):
                px = pm_x + 4 + i * 19
                filled = player.p_meter >= (i+1) * (P_METER_MAX // 7)
                c = C_ACCENT if filled else (60, 60, 60)
                screen.blit(FONT_SM.render("P" if i == 6 else "▸", True, c), (px, vp_y + 14))
            
            screen.blit(FONT_LG.render("TIME: 300", True, C_TEXT), (vp_x + vp_w - 120, vp_y + 10))
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
