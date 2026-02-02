import pygame, sys, json, os

# Initialize Pygame
pygame.init()

# ---------------- CONFIG ----------------
W, H = 800, 600
FPS = 60
TILE = 32

# Colors (SMBX Palette)
C_BG = (92, 148, 252)      # SMBX Sky Blue
C_PANEL = (38, 38, 42)
C_BORDER = (20, 20, 22)
C_TEXT = (255, 255, 255)
C_GRID = (255, 255, 255, 80)
C_ACCENT = (0, 122, 204)

# Physics Constants (SMBX 1.3 Feel)
GRAVITY = 0.4
FRICTION = 0.85
ACCEL = 0.5
MAX_SPEED = 6.0
JUMP_FORCE = -11.0

# Setup Display
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("SMBX 1.3 Python Clone")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("Arial", 14, bold=True)

# ---------------- ASSETS ----------------
# Procedurally generated assets to simulate SMBX graphics
def create_block(color, border_color=(0,0,0)):
    s = pygame.Surface((TILE, TILE))
    s.fill(color)
    pygame.draw.rect(s, border_color, (0,0,TILE,TILE), 2)
    # Inner bevel
    pygame.draw.line(s, (255,255,255), (2,2), (28,2))
    pygame.draw.line(s, (255,255,255), (2,2), (2,28))
    return s

def create_mario():
    s = pygame.Surface((TILE, TILE), pygame.SRCALPHA)
    # Red shirt
    pygame.draw.rect(s, (200, 0, 0), (4, 4, 24, 28))
    # Hat
    pygame.draw.rect(s, (200, 0, 0), (2, 4, 28, 8))
    # Face
    pygame.draw.rect(s, (255, 200, 150), (6, 12, 20, 10))
    return s

def create_goomba():
    s = pygame.Surface((TILE, TILE), pygame.SRCALPHA)
    # Brown body
    pygame.draw.circle(s, (139, 69, 19), (16, 22), 10)
    # Head
    pygame.draw.circle(s, (160, 82, 45), (16, 12), 8)
    # Feet
    pygame.draw.ellipse(s, (0, 0, 0), (4, 26, 10, 6))
    pygame.draw.ellipse(s, (18, 26, 10, 6), (18, 26, 10, 6))
    return s

assets = {
    "Blocks": {
        1: create_block((176, 128, 56)),  # Ground
        2: create_block((184, 80, 24)),   # Brick
        3: create_block((248, 184, 0)),   # Question Block
        4: create_block((100, 100, 100)), # Stone
    },
    "NPCs": {
        1: create_goomba(),
    }
}
player_img = create_mario()

# ---------------- CLASSES ----------------

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 28, 30) # Hitbox slightly smaller than tile
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.facing_right = True

    def update(self, blocks):
        # Input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.vel_x -= ACCEL
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.vel_x += ACCEL
            self.facing_right = True
        
        # Friction & Limits
        self.vel_x *= FRICTION
        if abs(self.vel_x) < 0.1: self.vel_x = 0
        self.vel_x = max(-MAX_SPEED, min(self.vel_x, MAX_SPEED))

        # Gravity
        self.vel_y += GRAVITY
        
        # Move X
        self.rect.x += int(self.vel_x)
        self.collision(blocks, True)

        # Move Y
        self.rect.y += int(self.vel_y)
        self.on_ground = False
        self.collision(blocks, False)

        # Jump
        if keys[pygame.K_z] and self.on_ground:
            self.vel_y = JUMP_FORCE

        # Reset if fall
        if self.rect.y > 2000:
            self.rect.x, self.rect.y = 100, 300
            self.vel_y = 0

    def collision(self, blocks, horizontal):
        # Simple AABB collision
        for pos, id in blocks.items():
            bx, by = pos[0]*TILE, pos[1]*TILE
            block_rect = pygame.Rect(bx, by, TILE, TILE)
            
            if self.rect.colliderect(block_rect):
                if horizontal:
                    if self.vel_x > 0: self.rect.right = block_rect.left
                    if self.vel_x < 0: self.rect.left = block_rect.right
                    self.vel_x = 0
                else:
                    if self.vel_y > 0: 
                        self.rect.bottom = block_rect.top
                        self.vel_y = 0
                        self.on_ground = True
                    if self.vel_y < 0: 
                        self.rect.top = block_rect.bottom
                        self.vel_y = 0

    def draw(self, surface, camx, camy):
        # Draw Mario with simple flip logic
        img = player_img if self.facing_right else pygame.transform.flip(player_img, True, False)
        surface.blit(img, (self.rect.x - camx - 2, self.rect.y - camy - 2))

class Enemy:
    def __init__(self, x, y, id):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.id = id
        self.vel_x = -2
        self.vel_y = 0
    
    def update(self, blocks):
        self.vel_y += GRAVITY
        self.rect.x += self.vel_x
        
        # Wall Collision / Turn around
        for pos, _ in blocks.items():
            brect = pygame.Rect(pos[0]*TILE, pos[1]*TILE, TILE, TILE)
            if self.rect.colliderect(brect):
                if self.vel_x > 0: self.rect.right = brect.left
                if self.vel_x < 0: self.rect.left = brect.right
                self.vel_x *= -1
        
        self.rect.y += self.vel_y
        # Floor Collision
        for pos, _ in blocks.items():
            brect = pygame.Rect(pos[0]*TILE, pos[1]*TILE, TILE, TILE)
            if self.rect.colliderect(brect):
                if self.vel_y > 0: 
                    self.rect.bottom = brect.top
                    self.vel_y = 0

class Level:
    def __init__(self):
        self.blocks = {}
        self.npcs = {}
        self.camx = 0
        self.camy = 0

    def save_lvlx(self, fn):
        data = {
            "format":"SMBX_PYTHON",
            "version":1,
            "blocks":[{"x":x*32,"y":y*32,"id":i} for (x,y),i in self.blocks.items()],
            "npcs":[{"x":x*32,"y":y*32,"id":i} for (x,y),i in self.npcs.items()]
        }
        try:
            with open(fn, "w") as f:
                json.dump(data, f, indent=2)
            print("Level Saved!")
        except Exception as e:
            print(f"Error saving: {e}")

    def load_lvlx(self, fn):
        try:
            if not os.path.exists(fn):
                print("File not found.")
                return
            with open(fn, "r") as f:
                j = json.load(f)
            self.blocks = {(b["x"]//32,b["y"]//32):b["id"] for b in j.get("blocks",[])}
            self.npcs = {(n["x"]//32,n["y"]//32):n["id"] for n in j.get("npcs",[])}
            print("Level Loaded!")
        except Exception as e:
            print(f"Failed to load: {e}")

# ---------------- MAIN ----------------
def main():
    # Variables that were global are now local to main
    # This allows 'nonlocal' to work inside nested functions like draw_text
    level = Level()
    player = Player(100, 300)
    active_enemies = []

    mode = "Editor" # Editor or Play
    edit_mode = "Blocks"
    selected = 1
    show_grid = True
    
    # UI helper variable
    y_ui = 20

    def draw_text(t, col=C_TEXT):
        nonlocal y_ui
        surf = FONT.render(t, True, col)
        screen.blit(surf, (15, y_ui))
        y_ui += 25

    while True:
        clock.tick(FPS)
        mx, my = pygame.mouse.get_pos()
        
        # Event Handling
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
                
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    # Toggle Mode
                    if mode == "Editor":
                        mode = "Play"
                        # Initialize Play State
                        player = Player(level.camx + 300, level.camy + 200) # Spawn near cam
                        active_enemies = []
                        for (nx, ny), nid in level.npcs.items():
                            active_enemies.append(Enemy(nx*TILE, ny*TILE, nid))
                    else:
                        mode = "Editor"

                if mode == "Editor":
                    if e.key == pygame.K_1: edit_mode="Blocks"; selected=1
                    if e.key == pygame.K_2: edit_mode="Blocks"; selected=2
                    if e.key == pygame.K_3: edit_mode="Blocks"; selected=3
                    if e.key == pygame.K_4: edit_mode="Blocks"; selected=4
                    if e.key == pygame.K_5: edit_mode="NPCs"; selected=1
                    if e.key == pygame.K_g: show_grid = not show_grid
                    # Use cmd+s/o on mac, ctrl+s/o on windows
                    is_cmd = (e.mod & pygame.KMOD_CTRL) or (e.mod & pygame.KMOD_META)
                    if e.key == pygame.K_s and is_cmd:
                        level.save_lvlx("level.lvlx")
                    if e.key == pygame.K_o and is_cmd:
                        level.load_lvlx("level.lvlx")

        # UPDATE LOGIC
        if mode == "Editor":
            # Editor Camera
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]: level.camx -= 8
            if keys[pygame.K_d]: level.camx += 8
            if keys[pygame.K_w]: level.camy -= 8
            if keys[pygame.K_s]: level.camy += 8
            
            # Mouse Interaction
            vp = pygame.Rect(200, 0, W-200, H)
            if vp.collidepoint(mx, my):
                gx = (mx - vp.x + level.camx) // TILE
                gy = (my - vp.y + level.camy) // TILE
                
                if pygame.mouse.get_pressed()[0]:
                    target = level.blocks if edit_mode == "Blocks" else level.npcs
                    target[(gx, gy)] = selected
                if pygame.mouse.get_pressed()[2]:
                    level.blocks.pop((gx, gy), None)
                    level.npcs.pop((gx, gy), None)
                    
        elif mode == "Play":
            # Game Physics
            player.update(level.blocks)
            
            for enemy in active_enemies:
                enemy.update(level.blocks)
                # Kill player logic (simple)
                if player.rect.colliderect(enemy.rect):
                    # Stomp check
                    if player.vel_y > 0 and player.rect.bottom < enemy.rect.centery:
                        active_enemies.remove(enemy)
                        player.vel_y = -6 # Bounce
                    else:
                        # Reset level (Death)
                        mode = "Editor" 
            
            # Camera Follow Player
            target_camx = player.rect.centerx - (W-200)//2
            target_camy = player.rect.centery - H//2
            level.camx += (target_camx - level.camx) * 0.1
            level.camy += (target_camy - level.camy) * 0.1

        # ---------------- DRAW ----------------
        screen.fill(C_BG)

        # Viewport Offset
        cam_ox = -int(level.camx)
        cam_oy = -int(level.camy)

        # Draw World (Clipped to Viewport area)
        game_surface = pygame.Surface((W-200, H))
        game_surface.fill(C_BG)
        
        # 1. Blocks
        for (x,y), i in level.blocks.items():
            if i in assets["Blocks"]:
                game_surface.blit(assets["Blocks"][i], (x*TILE + cam_ox, y*TILE + cam_oy))
                
        # 2. NPCs (Editor Mode)
        if mode == "Editor":
            for (x,y), i in level.npcs.items():
                if i in assets["NPCs"]:
                    game_surface.blit(assets["NPCs"][i], (x*TILE + cam_ox, y*TILE + cam_oy))
        
        # 3. Entities (Play Mode)
        if mode == "Play":
            player.draw(game_surface, level.camx, level.camy)
            for enemy in active_enemies:
                game_surface.blit(assets["NPCs"][enemy.id], (enemy.rect.x + cam_ox, enemy.rect.y + cam_oy))

        # 4. Grid
        if show_grid and mode == "Editor":
            off_x = cam_ox % TILE
            off_y = cam_oy % TILE
            for x in range(off_x, W-200, TILE):
                pygame.draw.line(game_surface, C_GRID, (x, 0), (x, H))
            for y in range(off_y, H, TILE):
                pygame.draw.line(game_surface, C_GRID, (0, y), (W-200, y))

        screen.blit(game_surface, (200, 0))

        # Sidebar UI
        pygame.draw.rect(screen, C_PANEL, (0, 0, 200, H))
        pygame.draw.rect(screen, C_BORDER, (0, 0, 200, H), 2)
        
        # Reset text Y position for this frame
        y_ui = 20
        
        draw_text(f"MODE: {mode.upper()}", C_ACCENT)
        y_ui += 10
        
        if mode == "Editor":
            draw_text("Controls:")
            draw_text("WASD: Move Camera")
            draw_text("L-Click: Place")
            draw_text("R-Click: Delete")
            draw_text("ENTER: Test Level")
            draw_text("Cmd/Ctrl+S: Save")
            draw_text("Cmd/Ctrl+O: Load")
            y_ui += 20
            draw_text("Items (Keys 1-5):")
            
            # Draw Palette
            pal_y = y_ui
            items = [
                (1, "Blocks", "Ground"),
                (2, "Blocks", "Brick"),
                (3, "Blocks", "? Block"),
                (4, "Blocks", "Stone"),
                (1, "NPCs", "Goomba"),
            ]
            
            for idx, (id, cat, name) in enumerate(items):
                # Selection Box
                is_sel = (edit_mode == cat and selected == id)
                if idx == 4: # Separator for NPCs
                     if edit_mode == "NPCs" and selected == 1: is_sel = True
                     else: is_sel = False

                if is_sel:
                    pygame.draw.rect(screen, C_ACCENT, (15, pal_y-5, 170, 42), 2)
                
                screen.blit(assets[cat][id], (20, pal_y))
                txt = FONT.render(f"{idx+1}: {name}", True, C_TEXT)
                screen.blit(txt, (60, pal_y+8))
                pal_y += 45

        else:
            draw_text("Playing...")
            draw_text("Arrows: Move")
            draw_text("Z: Jump")
            draw_text("ENTER: Stop")

        pygame.display.flip()

if __name__ == "__main__":
    main()
