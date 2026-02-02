import pygame
import sys
import json
import os
import math
import time

pygame.init()

# ---------------- CONFIGURATION (PGE STYLE) ----------------
SCREEN_W, SCREEN_H = 600, 400
FPS = 60
GRID_SIZE = 32
SCROLL_SPEED = 16

# PGE Dark Theme
C_BG_DARK = (30, 30, 30)
C_BG_MID = (45, 45, 48)
C_BG_LIGHT = (60, 60, 65)
C_PANEL = (38, 38, 42)
C_BORDER = (20, 20, 22)
C_ACCENT = (0, 122, 204)  # PGE Blue
C_ACCENT_LIGHT = (40, 160, 230)
C_TEXT = (210, 210, 210)
C_TEXT_DIM = (140, 140, 145)
C_TEXT_BRIGHT = (255, 255, 255)
C_SELECTION = (0, 122, 204)
C_HOVER = (70, 70, 75)
C_ACTIVE = (0, 100, 180)
C_SKY = (92, 148, 252)
C_GRID = (80, 80, 85)

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("AC'S Engine 0.1 - Samsoft")
clock = pygame.time.Clock()

try:
    FONT_UI = pygame.font.SysFont("Segoe UI", 11)
    FONT_BOLD = pygame.font.SysFont("Segoe UI", 11, bold=True)
    FONT_TITLE = pygame.font.SysFont("Segoe UI", 24, bold=True)
    FONT_SMALL = pygame.font.SysFont("Segoe UI", 9)
    FONT_SPLASH = pygame.font.SysFont("Segoe UI", 32, bold=True)
    FONT_SPLASH_SUB = pygame.font.SysFont("Segoe UI", 14)
except:
    FONT_UI = pygame.font.Font(None, 16)
    FONT_BOLD = pygame.font.Font(None, 16)
    FONT_TITLE = pygame.font.Font(None, 32)
    FONT_SMALL = pygame.font.Font(None, 14)
    FONT_SPLASH = pygame.font.Font(None, 48)
    FONT_SPLASH_SUB = pygame.font.Font(None, 20)

# ---------------- SPLASH SCREEN ----------------
def show_splash():
    start_time = time.time()
    duration = 2.5
    
    # Logo animation
    while time.time() - start_time < duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # Skip splash
        
        progress = (time.time() - start_time) / duration
        
        # Background gradient
        screen.fill(C_BG_DARK)
        
        # Animated glow effect
        glow_alpha = int(128 + 64 * math.sin(progress * math.pi * 4))
        glow_surf = pygame.Surface((300, 100), pygame.SRCALPHA)
        pygame.draw.ellipse(glow_surf, (*C_ACCENT, glow_alpha // 2), (0, 20, 300, 60))
        screen.blit(glow_surf, (SCREEN_W//2 - 150, SCREEN_H//2 - 60))
        
        # Main title with fade-in
        alpha = min(255, int(progress * 400))
        
        # Engine name
        title1 = FONT_SPLASH.render("AC'S Engine", True, C_TEXT_BRIGHT)
        title1.set_alpha(alpha)
        screen.blit(title1, (SCREEN_W//2 - title1.get_width()//2, SCREEN_H//2 - 50))
        
        # Version
        ver = FONT_TITLE.render("0.1", True, C_ACCENT_LIGHT)
        ver.set_alpha(alpha)
        screen.blit(ver, (SCREEN_W//2 - ver.get_width()//2, SCREEN_H//2))
        
        # Samsoft branding
        sub_alpha = min(255, max(0, int((progress - 0.3) * 500)))
        samsoft = FONT_SPLASH_SUB.render("Samsoft 1.x", True, C_TEXT)
        samsoft.set_alpha(sub_alpha)
        screen.blit(samsoft, (SCREEN_W//2 - samsoft.get_width()//2, SCREEN_H//2 + 40))
        
        # Copyright
        copy_alpha = min(255, max(0, int((progress - 0.5) * 400)))
        copy_text = FONT_SMALL.render("[C] 1999-2026 Team Flames / Flames Co.", True, C_TEXT_DIM)
        copy_text.set_alpha(copy_alpha)
        screen.blit(copy_text, (SCREEN_W//2 - copy_text.get_width()//2, SCREEN_H//2 + 70))
        
        # Loading bar
        bar_w = 200
        bar_h = 4
        bar_x = SCREEN_W//2 - bar_w//2
        bar_y = SCREEN_H - 60
        pygame.draw.rect(screen, C_BG_LIGHT, (bar_x, bar_y, bar_w, bar_h))
        pygame.draw.rect(screen, C_ACCENT, (bar_x, bar_y, int(bar_w * progress), bar_h))
        
        # Loading text
        load_txt = FONT_SMALL.render("Loading editor...", True, C_TEXT_DIM)
        screen.blit(load_txt, (SCREEN_W//2 - load_txt.get_width()//2, bar_y + 10))
        
        pygame.display.flip()
        clock.tick(60)

# ---------------- SMBX FILE FORMAT HANDLERS ----------------
class SMBXFormats:
    @staticmethod
    def save_lvl(filename, level_data):
        with open(filename, 'w') as f:
            f.write("SMBXFile64\n65\n")
            f.write(f"{level_data.get('stars', 0)}\n{level_data.get('name', 'Untitled')}\n")
            for i in range(21):
                f.write("-200000|-200000|200000|200000|0|0|0|0|0|0\n")
            for pos, blk in level_data.get('blocks', {}).items():
                f.write(f"B|{pos[0]*32}|{pos[1]*32}|{blk}|0|0|0|0|0|0\n")
            for pos, bgo in level_data.get('bgos', {}).items():
                f.write(f"T|{pos[0]*32}|{pos[1]*32}|{bgo}\n")
            for pos, npc in level_data.get('npcs', {}).items():
                f.write(f"N|{pos[0]*32}|{pos[1]*32}|1|{npc}|0|0|0|0|0|0|0||0\n")
            f.write('"next"\n')
    
    @staticmethod
    def load_lvl(filename):
        data = {'blocks': {}, 'bgos': {}, 'npcs': {}}
        try:
            with open(filename, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('B|'):
                        p = line.split('|')
                        data['blocks'][(int(p[1])//32, int(p[2])//32)] = int(p[3])
                    elif line.startswith('T|'):
                        p = line.split('|')
                        data['bgos'][(int(p[1])//32, int(p[2])//32)] = int(p[3])
                    elif line.startswith('N|'):
                        p = line.split('|')
                        data['npcs'][(int(p[1])//32, int(p[2])//32)] = int(p[4])
        except: pass
        return data
    
    @staticmethod
    def save_lvlx(filename, level_data):
        data = {'format': 'LVLX', 'version': 38, 'name': level_data.get('name', 'Untitled'),
                'stars': level_data.get('stars', 0), 'blocks': [], 'bgos': [], 'npcs': [],
                'layers': [{'name': 'Default', 'hidden': False}], 'events': [], 'warps': []}
        for pos, blk in level_data.get('blocks', {}).items():
            data['blocks'].append({'x': pos[0]*32, 'y': pos[1]*32, 'id': blk, 'layer': 'Default'})
        for pos, bgo in level_data.get('bgos', {}).items():
            data['bgos'].append({'x': pos[0]*32, 'y': pos[1]*32, 'id': bgo, 'layer': 'Default'})
        for pos, npc in level_data.get('npcs', {}).items():
            data['npcs'].append({'x': pos[0]*32, 'y': pos[1]*32, 'id': npc, 'layer': 'Default'})
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    @staticmethod
    def load_lvlx(filename):
        data = {'blocks': {}, 'bgos': {}, 'npcs': {}}
        try:
            with open(filename, 'r') as f:
                j = json.load(f)
                for b in j.get('blocks', []): data['blocks'][(b['x']//32, b['y']//32)] = b['id']
                for b in j.get('bgos', []): data['bgos'][(b['x']//32, b['y']//32)] = b['id']
                for n in j.get('npcs', []): data['npcs'][(n['x']//32, n['y']//32)] = n['id']
        except: pass
        return data
    
    @staticmethod
    def save_wld(filename, world_data):
        with open(filename, 'w') as f:
            f.write(f"SMBXFile65\n{world_data.get('name', 'World')}\n0\n\n")
            for pos, t in world_data.get('tiles', {}).items():
                f.write(f"T|{pos[0]*32}|{pos[1]*32}|{t}\n")
    
    @staticmethod
    def save_wldx(filename, world_data):
        data = {'format': 'WLDX', 'version': 38, 'name': world_data.get('name', 'World'),
                'tiles': [], 'scenery': [], 'paths': [], 'levels': []}
        for pos, t in world_data.get('tiles', {}).items():
            data['tiles'].append({'x': pos[0]*32, 'y': pos[1]*32, 'id': t})
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

# ---------------- PGE-STYLE GRAPHICS ----------------
def draw_pge_button(surf, rect, state="normal", text="", icon=None):
    x, y, w, h = rect
    if state == "active":
        bg, border, txt_c = C_ACTIVE, C_ACCENT, C_TEXT_BRIGHT
    elif state == "hover":
        bg, border, txt_c = C_HOVER, C_BG_LIGHT, C_TEXT_BRIGHT
    else:
        bg, border, txt_c = C_BG_MID, C_BORDER, C_TEXT
    
    pygame.draw.rect(surf, bg, rect)
    pygame.draw.rect(surf, border, rect, 1)
    
    txt = FONT_UI.render(text, True, txt_c)
    surf.blit(txt, (x + (w - txt.get_width())//2, y + (h - txt.get_height())//2))

def draw_pge_panel(surf, rect, title=None):
    pygame.draw.rect(surf, C_PANEL, rect)
    pygame.draw.rect(surf, C_BORDER, rect, 1)
    if title:
        pygame.draw.rect(surf, C_BG_LIGHT, (rect[0], rect[1], rect[2], 20))
        pygame.draw.line(surf, C_BORDER, (rect[0], rect[1]+20), (rect[0]+rect[2], rect[1]+20))
        t = FONT_BOLD.render(title, True, C_TEXT)
        surf.blit(t, (rect[0] + 6, rect[1] + 3))

def draw_pge_toolbar(surf, rect):
    pygame.draw.rect(surf, C_BG_MID, rect)
    pygame.draw.line(surf, C_BORDER, (rect[0], rect[1]+rect[3]-1), (rect[0]+rect[2], rect[1]+rect[3]-1))

# ---------------- ASSET GENERATION ----------------
assets = {"Blocks": {}, "BGOs": {}, "NPCs": {}}

def generate_assets():
    # Blocks
    for i, (fill, top, name) in enumerate([
        ((176, 128, 56), (224, 176, 104), "Ground"),
        ((184, 80, 24), None, "Brick"),
        ((248, 184, 0), None, "Question"),
        ((128, 80, 32), None, "Used"),
        ((0, 168, 0), (96, 248, 96), "Pipe"),
        ((248, 248, 248), None, "Cloud"),
    ], 1):
        s = pygame.Surface((32, 32), pygame.SRCALPHA)
        if i == 6:  # Cloud
            pygame.draw.ellipse(s, fill, (0, 8, 32, 20))
            pygame.draw.ellipse(s, (0, 0, 0), (0, 8, 32, 20), 1)
        else:
            s.fill(fill)
            if top: pygame.draw.rect(s, top, (2, 2, 28, 14))
            if i == 2:  # Brick lines
                for lx in [0, 16]: pygame.draw.line(s, (0,0,0), (lx, 0), (lx, 15), 2)
                for lx in [8, 24]: pygame.draw.line(s, (0,0,0), (lx, 15), (lx, 32), 2)
                pygame.draw.line(s, (0,0,0), (0, 15), (32, 15), 2)
            if i == 3:  # Question mark
                q = FONT_BOLD.render("?", True, (0, 0, 0))
                s.blit(q, (12, 8))
            pygame.draw.rect(s, (0, 0, 0), (0, 0, 32, 32), 1)
        assets["Blocks"][i] = s
    
    # BGOs
    s = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.ellipse(s, (0, 168, 0), (0, 8, 32, 24))
    assets["BGOs"][1] = s
    
    s = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.polygon(s, (0, 168, 0), [(16, 0), (0, 32), (32, 32)])
    assets["BGOs"][2] = s
    
    s = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.ellipse(s, (248, 248, 248, 180), (0, 8, 32, 20))
    assets["BGOs"][3] = s
    
    # NPCs
    # Goomba
    s = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.ellipse(s, (168, 80, 32), (4, 4, 24, 20))
    pygame.draw.ellipse(s, (248, 208, 160), (8, 20, 16, 12))
    pygame.draw.circle(s, (255, 255, 255), (10, 12), 4)
    pygame.draw.circle(s, (255, 255, 255), (22, 12), 4)
    pygame.draw.circle(s, (0, 0, 0), (11, 13), 2)
    pygame.draw.circle(s, (0, 0, 0), (21, 13), 2)
    assets["NPCs"][1] = s
    
    # Koopa
    s = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.ellipse(s, (0, 168, 0), (6, 8, 20, 24))
    pygame.draw.ellipse(s, (248, 208, 160), (10, 0, 12, 14))
    pygame.draw.circle(s, (255, 255, 255), (14, 6), 3)
    pygame.draw.circle(s, (0, 0, 0), (15, 6), 1)
    assets["NPCs"][2] = s
    
    # Mushroom
    s = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.ellipse(s, (248, 56, 0), (2, 2, 28, 18))
    pygame.draw.circle(s, (248, 248, 248), (10, 10), 5)
    pygame.draw.circle(s, (248, 248, 248), (22, 10), 5)
    pygame.draw.rect(s, (248, 208, 160), (10, 16, 12, 14))
    assets["NPCs"][3] = s
    
    # Fire Flower
    s = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.circle(s, (248, 128, 0), (16, 10), 8)
    pygame.draw.circle(s, (248, 248, 0), (16, 10), 5)
    pygame.draw.rect(s, (0, 168, 0), (14, 16, 4, 14))
    pygame.draw.ellipse(s, (0, 168, 0), (6, 22, 10, 8))
    pygame.draw.ellipse(s, (0, 168, 0), (16, 22, 10, 8))
    assets["NPCs"][4] = s
    
    # Star
    s = pygame.Surface((32, 32), pygame.SRCALPHA)
    pts = []
    for i in range(5):
        a = math.radians(i * 72 - 90)
        pts.append((16 + 12 * math.cos(a), 16 + 12 * math.sin(a)))
        a2 = math.radians(i * 72 - 90 + 36)
        pts.append((16 + 5 * math.cos(a2), 16 + 5 * math.sin(a2)))
    pygame.draw.polygon(s, (248, 248, 0), pts)
    pygame.draw.polygon(s, (0, 0, 0), pts, 1)
    assets["NPCs"][5] = s

generate_assets()

# ---------------- STATE ----------------
class LevelData:
    def __init__(self):
        self.blocks, self.bgos, self.npcs = {}, {}, {}
        self.camera_x, self.camera_y = 0, 0
        self.name, self.stars = "Untitled", 0
    
    def to_dict(self):
        return {'blocks': self.blocks, 'bgos': self.bgos, 'npcs': self.npcs,
                'name': self.name, 'stars': self.stars}
    
    def from_dict(self, data):
        self.blocks = {(k if isinstance(k, tuple) else tuple(k)): v for k, v in data.get('blocks', {}).items()}
        self.bgos = {(k if isinstance(k, tuple) else tuple(k)): v for k, v in data.get('bgos', {}).items()}
        self.npcs = {(k if isinstance(k, tuple) else tuple(k)): v for k, v in data.get('npcs', {}).items()}
    
    def save(self, fn, fmt='lvlx'):
        if fmt == 'lvl': SMBXFormats.save_lvl(fn, self.to_dict())
        else: SMBXFormats.save_lvlx(fn, self.to_dict())
    
    def load(self, fn):
        data = SMBXFormats.load_lvlx(fn) if fn.endswith('.lvlx') else SMBXFormats.load_lvl(fn)
        self.from_dict(data)

level = LevelData()

class EditorState:
    def __init__(self):
        self.mode, self.selected_id = "Blocks", 1
        self.show_grid, self.status = True, "Ready"
        self.tool = "pencil"  # pencil, eraser, select
    
    def set_mode(self, mode):
        if mode in assets and assets[mode]:
            self.mode = mode
            keys = list(assets[mode].keys())
            self.selected_id = keys[0] if keys else 1

state = EditorState()

# ---------------- UI ----------------
class Button:
    def __init__(self, x, y, w, h, text, func=None, group=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text, self.func, self.group = text, func, group
        self.state = "normal"
    
    def update(self, mx, my, click, active=False):
        self.state = "active" if active else "normal"
        if self.rect.collidepoint(mx, my):
            if click:
                if self.func: self.func()
                return True
            elif not active:
                self.state = "hover"
        return False
    
    def draw(self, surf):
        draw_pge_button(surf, self.rect, self.state, self.text)

buttons = []

def do_new():
    level.blocks, level.bgos, level.npcs = {}, {}, {}
    level.camera_x, level.camera_y = 0, 0
    state.status = "New level"

def do_save():
    level.save("level.lvlx", "lvlx")
    state.status = "Saved: level.lvlx"

def do_save_lvl():
    level.save("level.lvl", "lvl")
    state.status = "Saved: level.lvl"

def do_load():
    for fn in ["level.lvlx", "level.lvl"]:
        if os.path.exists(fn):
            level.load(fn)
            state.status = f"Loaded: {fn}"
            return
    state.status = "No level found"

def init_ui():
    buttons.clear()
    # File toolbar
    x = 5
    for txt, fn in [("New", do_new), ("Open", do_load), ("Save", do_save), (".LVL", do_save_lvl)]:
        buttons.append(Button(x, 5, 45, 22, txt, fn))
        x += 48
    
    # Mode tabs
    y = 32
    buttons.append(Button(5, y, 55, 20, "Blocks", lambda: state.set_mode("Blocks"), "TAB"))
    buttons.append(Button(62, y, 45, 20, "BGOs", lambda: state.set_mode("BGOs"), "TAB"))
    buttons.append(Button(109, y, 45, 20, "NPCs", lambda: state.set_mode("NPCs"), "TAB"))

init_ui()

# ---------------- VIEWPORT LAYOUT ----------------
PANEL_W = 160
TOOLBAR_H = 55
VP_X, VP_Y = PANEL_W + 5, TOOLBAR_H + 5
VP_W, VP_H = SCREEN_W - VP_X - 5, SCREEN_H - VP_Y - 20

# ---------------- MAIN LOOP ----------------
def main():
    show_splash()
    
    running = True
    while running:
        click = False
        mx, my = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g: state.show_grid = not state.show_grid
                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL: do_save()
                if event.key == pygame.K_n and pygame.key.get_mods() & pygame.KMOD_CTRL: do_new()
        
        # Camera
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: level.camera_x -= SCROLL_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: level.camera_x += SCROLL_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]: level.camera_y -= SCROLL_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: level.camera_y += SCROLL_SPEED
        
        # Update UI
        ui_hit = False
        for btn in buttons:
            active = btn.group == "TAB" and btn.text == state.mode
            if btn.rect.collidepoint(mx, my): ui_hit = True
            btn.update(mx, my, click, active)
        
        # Asset palette clicks
        palette_rect = pygame.Rect(5, 75, PANEL_W - 10, SCREEN_H - 95)
        if palette_rect.collidepoint(mx, my):
            ui_hit = True
            if click:
                rx, ry = mx - 10, my - 80
                if rx > 0 and ry > 0:
                    col, row = rx // 38, ry // 38
                    idx = row * 4 + col
                    keys = list(assets[state.mode].keys())
                    if 0 <= idx < len(keys):
                        state.selected_id = keys[idx]
        
        # Viewport editing
        vp_rect = pygame.Rect(VP_X, VP_Y, VP_W, VP_H)
        if not ui_hit and vp_rect.collidepoint(mx, my):
            wx = mx + level.camera_x - VP_X
            wy = my + level.camera_y - VP_Y
            gx, gy = wx // GRID_SIZE, wy // GRID_SIZE
            target = {"Blocks": level.blocks, "BGOs": level.bgos, "NPCs": level.npcs}[state.mode]
            m = pygame.mouse.get_pressed()
            if m[0]: target[(gx, gy)] = state.selected_id
            if m[2]: target.pop((gx, gy), None)
        
        # ============ DRAWING ============
        screen.fill(C_BG_DARK)
        
        # Top toolbar
        draw_pge_toolbar(screen, (0, 0, SCREEN_W, 30))
        
        # Left panel
        draw_pge_panel(screen, (0, 30, PANEL_W, SCREEN_H - 30), f"Items - {state.mode}")
        
        # Viewport
        pygame.draw.rect(screen, C_SKY, vp_rect)
        vp_surf = screen.subsurface(vp_rect)
        
        # Grid
        if state.show_grid:
            sx, sy = -(level.camera_x % GRID_SIZE), -(level.camera_y % GRID_SIZE)
            for x in range(int(sx), VP_W, GRID_SIZE):
                pygame.draw.line(vp_surf, C_GRID, (x, 0), (x, VP_H))
            for y in range(int(sy), VP_H, GRID_SIZE):
                pygame.draw.line(vp_surf, C_GRID, (0, y), (VP_W, y))
        
        # Render objects
        for layer, lib in [(level.bgos, assets["BGOs"]), (level.blocks, assets["Blocks"]), (level.npcs, assets["NPCs"])]:
            for (gx, gy), aid in layer.items():
                sx, sy = gx * GRID_SIZE - level.camera_x, gy * GRID_SIZE - level.camera_y
                if -32 < sx < VP_W and -32 < sy < VP_H and aid in lib:
                    vp_surf.blit(lib[aid], (sx, sy))
        
        pygame.draw.rect(screen, C_BORDER, vp_rect, 1)
        
        # Buttons
        for btn in buttons:
            btn.draw(screen)
        
        # Asset palette
        cur = assets[state.mode]
        for i, k in enumerate(cur.keys()):
            ax, ay = 10 + (i % 4) * 38, 80 + (i // 4) * 38
            if state.selected_id == k:
                pygame.draw.rect(screen, C_ACCENT, (ax-3, ay-3, 38, 38), 2)
            screen.blit(cur[k], (ax, ay))
        
        # Status bar
        pygame.draw.rect(screen, C_BG_MID, (0, SCREEN_H - 18, SCREEN_W, 18))
        pygame.draw.line(screen, C_BORDER, (0, SCREEN_H - 18), (SCREEN_W, SCREEN_H - 18))
        stat = FONT_SMALL.render(f"{state.status} | AC'S Engine 0.1 | [C] 1999-2026 Samsoft/Flames Co.", True, C_TEXT_DIM)
        screen.blit(stat, (5, SCREEN_H - 14))
        
        # Coords
        coords = FONT_SMALL.render(f"Pos: {mx}, {my} | Grid: G | Scroll: WASD", True, C_TEXT_DIM)
        screen.blit(coords, (SCREEN_W - coords.get_width() - 5, SCREEN_H - 14))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
