import pygame
import sys
import random  # for grass tufts variation

pygame.init()

# ---------------- CONFIGURATION & XP THEME ----------------
SCREEN_W, SCREEN_H = 1024, 768
VIEWPORT_X, VIEWPORT_Y = 280, 50
VIEWPORT_W = SCREEN_W - VIEWPORT_X
VIEWPORT_H = SCREEN_H - 50
FPS = 60
GRID_SIZE = 32
SCROLL_SPEED = 16

# Windows XP Legacy Colors
C_BG_MAIN     = (236, 233, 216)     # XP window beige
C_BG_PANEL    = (236, 233, 216)
C_BG_VIEWPORT = (92, 148, 252)      # SMB3 sky
C_BORDER      = (172, 168, 153)     # XP shadow gray
C_BORDER_HI   = (255, 255, 255)     # XP highlight white
C_BUTTON      = (225, 225, 225)
C_BUTTON_HOVER= (240, 240, 230)
C_BUTTON_ACT  = (49, 106, 197)      # XP blue active
C_TEXT_MAIN   = (0, 0, 0)
C_TEXT_DIM    = (100, 100, 100)
C_GRID        = (200, 200, 255, 80)

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.RESIZABLE)
pygame.display.set_caption("Ultra Mario Bros. X - Windows XP Edition")
clock = pygame.time.Clock()

# Fonts (XP classic)
FONT_UI   = pygame.font.SysFont("Tahoma", 11) or pygame.font.Font(None, 20)
FONT_BOLD = pygame.font.SysFont("Tahoma", 11, bold=True) or pygame.font.Font(None, 20)
FONT_TITLE= pygame.font.SysFont("Trebuchet MS", 14, bold=True) or pygame.font.Font(None, 24)

# ---------------- CLAMP HELPERS ----------------
def clamp(v, lo=0, hi=255):
    return max(lo, min(hi, int(v)))

def clamp_color(c):
    return (clamp(c[0]), clamp(c[1]), clamp(c[2]))

# ---------------- XP 3D BORDER ----------------
def draw_xp_border(surf, rect, depressed=False):
    l, t, r, b = rect.left, rect.top, rect.right, rect.bottom
    light = C_BORDER_HI
    shadow = C_BORDER
    dark = (128, 128, 128)

    if depressed:
        pygame.draw.line(surf, shadow, (l, b-1), (l, t), 1)
        pygame.draw.line(surf, shadow, (l, t), (r-1, t), 1)
        pygame.draw.line(surf, light, (r-1, t), (r-1, b-1), 1)
        pygame.draw.line(surf, light, (r-1, b-1), (l, b-1), 1)
    else:
        pygame.draw.line(surf, light, (l, b-2), (l, t), 1)
        pygame.draw.line(surf, light, (l, t), (r-2, t), 1)
        pygame.draw.line(surf, shadow, (r-1, t), (r-1, b-1), 1)
        pygame.draw.line(surf, shadow, (r-1, b-1), (l, b-1), 1)
        pygame.draw.line(surf, dark, (r-2, t+1), (r-2, b-2), 1)
        pygame.draw.line(surf, dark, (r-2, b-2), (l+1, b-2), 1)

# ---------------- ASSET GENERATION (ALL PRIMITIVES, NO CRASH) ----------------
assets = {"Blocks": {}, "BGOs": {}, "NPCs": {}}

def generate_assets():
    # BLOCK 1: Grass Ground
    s = pygame.Surface((32, 32))
    s.fill((139, 69, 19))  # dirt
    pygame.draw.rect(s, (34, 139, 34), (0, 0, 32, 12))  # grass
    for x in range(4, 32, 8):
        h = random.randint(6, 10)
        pygame.draw.line(s, (0, 100, 0), (x, 12), (x-2, 12-h), 1)
        pygame.draw.line(s, (0, 100, 0), (x, 12), (x+2, 12-h), 1)
    assets["Blocks"][1] = s

    # BLOCK 2: Brick
    s = pygame.Surface((32, 32))
    s.fill((181, 101, 29))
    pygame.draw.rect(s, (0,0,0), (0,0,32,32), 1)
    pygame.draw.line(s, (0,0,0), (0,16), (32,16), 1)
    pygame.draw.line(s, (0,0,0), (16,0), (16,16), 1)
    pygame.draw.line(s, (0,0,0), (8,16), (8,32), 1)
    pygame.draw.line(s, (0,0,0), (24,16), (24,32), 1)
    assets["Blocks"][2] = s

    # BLOCK 3: Question Block
    s = pygame.Surface((32, 32))
    s.fill((255, 204, 0))
    pygame.draw.rect(s, (180, 120, 0), (0,0,32,32), 2)
    for x,y in [(2,2),(30,2),(2,30),(30,30)]:
        pygame.draw.circle(s, (180, 100, 0), (x,y), 2)
    # ?
    pygame.draw.lines(s, (139, 69, 19), False, [(12,10),(20,10),(20,16),(16,20),(16,24)], 3)
    pygame.draw.circle(s, (139, 69, 19), (16, 28), 2)
    assets["Blocks"][3] = s

    # BLOCK 4: Pipe
    s = pygame.Surface((32, 32))
    s.fill((0, 168, 0))
    pygame.draw.rect(s, (0,0,0), (0,0,32,32), 1)
    pygame.draw.line(s, (0, 220, 0), (6,0), (6,32), 4)   # highlight
    pygame.draw.line(s, (0, 100, 0), (26,0), (26,32), 4) # shadow
    assets["Blocks"][4] = s

    # BGO 1: Hill Top
    s = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.circle(s, (0, 140, 0), (16, 32), 16)
    pygame.draw.circle(s, (0, 0, 0), (16, 32), 16, 1)
    assets["BGOs"][1] = s

    # BGO 2: Cloud
    s = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.circle(s, (255, 255, 255), (16, 16), 12)
    pygame.draw.circle(s, (240, 240, 240), (16, 16), 12, 2)
    assets["BGOs"][2] = s

    # BGO 3: Desert Hill (FIXED - clamped colors)
    s = pygame.Surface((64, 64), pygame.SRCALPHA)
    base = (252, 216, 168)
    light = clamp_color((base[0]+30, base[1]+30, base[2]+20))
    dark  = clamp_color((base[0]-40, base[1]-40, base[2]-30))
    pygame.draw.circle(s, base, (32, 64), 30)
    pygame.draw.circle(s, light, (32, 64), 25)
    pygame.draw.circle(s, dark, (40, 72), 18)
    assets["BGOs"][3] = s

    # NPC 1: Goomba
    s = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.polygon(s, (140, 60, 20), [(8,28),(16,8),(24,28)])
    pygame.draw.circle(s, (255,255,255), (13,16), 4)
    pygame.draw.circle(s, (255,255,255), (19,16), 4)
    pygame.draw.circle(s, (0,0,0), (14,16), 1)
    pygame.draw.circle(s, (0,0,0), (20,16), 1)
    assets["NPCs"][1] = s

    print("Assets generated - all primitives, no crashes")

generate_assets()

# ---------------- DATA & STATE ----------------
class LevelData:
    def __init__(self):
        self.blocks = {}
        self.bgos = {}
        self.npcs = {}
        self.camera_x = 0
        self.camera_y = 0

    def save(self):
        print("Level Saved (stub)")

    def load(self):
        print("Level Loaded (stub)")
        self.camera_x = 0
        self.camera_y = 0

level = LevelData()

class EditorState:
    def __init__(self):
        self.mode = "Blocks"
        self.selected_id = 1
        self.show_grid = True
        self.message = "XP Edition Ready"
        self.msg_timer = 180

    def set_mode(self, mode):
        self.mode = mode
        keys = list(assets[mode].keys())
        self.selected_id = keys[0] if keys else 1
        self.message = f"Mode switched to {mode}"
        self.msg_timer = 120

state = EditorState()

# ---------------- BUTTON CLASS ----------------
class Button:
    def __init__(self, x, y, w, h, text, func=None, group_id=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.func = func
        self.group_id = group_id
        self.active = False
        self.hover = False

    def draw(self, surf):
        if self.active:
            pygame.draw.rect(surf, C_BUTTON_ACT, self.rect)
            draw_xp_border(surf, self.rect, depressed=True)
            col = (255,255,255)
        elif self.hover:
            pygame.draw.rect(surf, C_BUTTON_HOVER, self.rect)
            draw_xp_border(surf, self.rect, depressed=False)
            col = C_TEXT_MAIN
        else:
            pygame.draw.rect(surf, C_BUTTON, self.rect)
            draw_xp_border(surf, self.rect, depressed=False)
            col = C_TEXT_MAIN

        txt = FONT_UI.render(self.text, True, col)
        tx = self.rect.centerx - txt.get_width() // 2
        ty = self.rect.centery - txt.get_height() // 2
        surf.blit(txt, (tx, ty))

    def update(self, mx, my, click):
        self.hover = self.rect.collidepoint(mx, my)
        if self.hover and click:
            if self.func: self.func()
            return True
        return False

# ---------------- UI SETUP ----------------
buttons = []
def init_ui():
    buttons.clear()
    # Top bar
    buttons.append(Button(5, 5, 60, 22, "File"))
    buttons.append(Button(70, 5, 60, 22, "View"))
    buttons.append(Button(135, 5, 60, 22, "Help"))
    buttons.append(Button(SCREEN_W - 140, 5, 60, 22, "Save", level.save))
    buttons.append(Button(SCREEN_W - 75, 5, 60, 22, "Load", level.load))

    # Mode tabs
    y = 60
    buttons.append(Button(10, y, 80, 24, "Blocks", lambda: state.set_mode("Blocks"), "TAB"))
    buttons.append(Button(95, y, 80, 24, "BGOs", lambda: state.set_mode("BGOs"), "TAB"))
    buttons.append(Button(180, y, 80, 24, "NPCs", lambda: state.set_mode("NPCs"), "TAB"))

init_ui()

# ---------------- MAIN LOOP ----------------
def main():
    running = True
    while running:
        mx, my = pygame.mouse.get_pos()
        m_pressed = pygame.mouse.get_pressed()
        click = m_pressed[0]  # simple for now

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    state.show_grid = not state.show_grid

        # Camera
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: level.camera_x -= SCROLL_SPEED
        if keys[pygame.K_RIGHT]: level.camera_x += SCROLL_SPEED
        if keys[pygame.K_UP]: level.camera_y -= SCROLL_SPEED
        if keys[pygame.K_DOWN]: level.camera_y += SCROLL_SPEED

        # UI hit test
        ui_hit = my < 50 or mx < 280
        if ui_hit:
            for btn in buttons:
                if btn.group_id == "TAB":
                    btn.active = (btn.text == state.mode)
                btn.update(mx, my, click)

        # Editing
        if not ui_hit:
            wx = mx + level.camera_x - VIEWPORT_X
            wy = my + level.camera_y - VIEWPORT_Y
            gx = wx // GRID_SIZE
            gy = wy // GRID_SIZE

            target = level.blocks if state.mode == "Blocks" else \
                     level.bgos   if state.mode == "BGOs"   else level.npcs

            if m_pressed[0]:
                target[(gx, gy)] = state.selected_id
            if m_pressed[2]:
                target.pop((gx, gy), None)

        # DRAW
        screen.fill(C_BG_MAIN)

        # Viewport
        vp_rect = pygame.Rect(VIEWPORT_X, VIEWPORT_Y, VIEWPORT_W, VIEWPORT_H)
        pygame.draw.rect(screen, C_BG_VIEWPORT, vp_rect)
        vp_surf = screen.subsurface(vp_rect)

        # Grid
        if state.show_grid:
            sx = -(level.camera_x % GRID_SIZE)
            sy = -(level.camera_y % GRID_SIZE)
            for x in range(sx, VIEWPORT_W, GRID_SIZE):
                pygame.draw.line(vp_surf, C_GRID, (x, 0), (x, VIEWPORT_H))
            for y in range(sy, VIEWPORT_H, GRID_SIZE):
                pygame.draw.line(vp_surf, C_GRID, (0, y), (VIEWPORT_W, y))

        # Draw layers
        for layer, lib in [(level.bgos, assets["BGOs"]),
                           (level.blocks, assets["Blocks"]),
                           (level.npcs, assets["NPCs"])]:
            for (gx, gy), aid in layer.items():
                sx = gx * GRID_SIZE - level.camera_x
                sy = gy * GRID_SIZE - level.camera_y
                if -64 < sx < VIEWPORT_W and -64 < sy < VIEWPORT_H:
                    if aid in lib:
                        vp_surf.blit(lib[aid], (sx, sy))

        # UI
        draw_xp_border(screen, pygame.Rect(0, 0, SCREEN_W, 50), False)  # top bar
        draw_xp_border(screen, pygame.Rect(0, 50, 280, SCREEN_H-50), False)  # left panel

        for btn in buttons:
            btn.draw(screen)

        # Asset selector label
        lbl = FONT_BOLD.render(f"Select {state.mode}:", True, C_TEXT_MAIN)
        screen.blit(lbl, (20, 95))

        # Asset grid
        asset_dict = assets[state.mode]
        idx = 0
        cols = 4
        for k, surf in asset_dict.items():
            bx = 20 + (idx % cols) * 60
            by = 120 + (idx // cols) * 60
            r = pygame.Rect(bx, by, 50, 50)

            if state.selected_id == k:
                pygame.draw.rect(screen, C_BUTTON_ACT, r)
                draw_xp_border(screen, r, depressed=True)
            else:
                draw_xp_border(screen, r, depressed=False)

            # Scale preview if too big
            ps = surf
            if surf.get_width() > 40 or surf.get_height() > 40:
                scale = 40 / max(surf.get_width(), surf.get_height())
                ps = pygame.transform.smoothscale(surf, (int(surf.get_width()*scale), int(surf.get_height()*scale)))

            sx = bx + (50 - ps.get_width()) // 2
            sy = by + (50 - ps.get_height()) // 2
            screen.blit(ps, (sx, sy))
            idx += 1

        # Status
        if state.msg_timer > 0:
            state.msg_timer -= 1
            msg = FONT_UI.render(state.message, True, (0, 128, 0))
            screen.blit(msg, (VIEWPORT_X + 10, SCREEN_H - 20))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
