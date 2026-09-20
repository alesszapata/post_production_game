import sys
import math
import random
import pygame

pygame.init()
pygame.font.init()

# --- Initialize Pygame Audio Mixer ---
try:
    pygame.mixer.init(frequency=22100, size=-16, channels=2)
    AUDIO_ENABLED = True
except Exception:
    AUDIO_ENABLED = False

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Post-Production Rush: Behind the Screen")
clock = pygame.time.Clock()

font_header = pygame.font.SysFont("Arial", 16, bold=True)
font_title = pygame.font.SysFont("Arial", 13, bold=True)
font_body = pygame.font.SysFont("Arial", 13)
font_small = pygame.font.SysFont("Arial", 11, bold=True)

# --- Sound Synthesis Helpers ---
def play_sound(sound_type):
    if not AUDIO_ENABLED:
        return
    try:
        sample_rate = 22100
        if sound_type == "spray":
            duration = 0.04
            freq = 450
        elif sound_type == "success":
            duration = 0.2
            freq = 880
        elif sound_type == "penalty":
            duration = 0.25
            freq = 110
        elif sound_type == "collect":
            duration = 0.08
            freq = 1200
        else:
            return

        num_samples = int(sample_rate * duration)
        buffer = bytearray()
        for i in range(num_samples):
            val = int(32767 * math.sin(2 * math.pi * freq * i / sample_rate))
            buffer += val.to_bytes(2, byteorder='little', signed=True)
            buffer += val.to_bytes(2, byteorder='little', signed=True)
        
        sound = pygame.mixer.Sound(buffer=bytes(buffer))
        sound.set_volume(0.12)
        sound.play()
    except Exception:
        pass

# --- Pixel-Art Asset Generators ---
def create_pixel_player():
    surf = pygame.Surface((36, 36), pygame.SRCALPHA)
    pygame.draw.rect(surf, (0, 200, 255), (9, 12, 18, 18), border_radius=2)
    pygame.draw.rect(surf, (255, 220, 177), (12, 4, 12, 9))
    pygame.draw.rect(surf, (60, 40, 30), (12, 2, 12, 4))
    surf.set_at((15, 7), (0, 0, 0))
    surf.set_at((20, 7), (0, 0, 0))
    return surf

def create_pixel_client():
    surf = pygame.Surface((36, 36), pygame.SRCALPHA)
    pygame.draw.rect(surf, (230, 50, 50), (9, 12, 18, 18), border_radius=2)
    pygame.draw.rect(surf, (255, 220, 177), (12, 4, 12, 9))
    surf.set_at((17, 15), (255, 255, 255))
    surf.set_at((17, 16), (255, 255, 255))
    surf.set_at((17, 17), (255, 255, 255))
    return surf

def create_coffee_mug_surface():
    surf = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.rect(surf, (245, 245, 250), (6, 10, 16, 16), border_radius=3)
    pygame.draw.rect(surf, (120, 70, 40), (9, 13, 10, 4))
    pygame.draw.line(surf, (150, 210, 255, 200), (12, 6), (12, 2), 2)
    pygame.draw.line(surf, (150, 210, 255, 200), (18, 7), (18, 3), 2)
    return surf

def create_fire_frames():
    frames = []
    for i in range(4):
        surf = pygame.Surface((44, 44), pygame.SRCALPHA)
        pts = [(22, 4 + (i % 2)), (38, 34), (6, 34)]
        pygame.draw.polygon(surf, (255, 80, 20, 220), pts)
        pts_inner = [(22, 14 + (i % 2)), (30, 34), (14, 34)]
        pygame.draw.polygon(surf, (255, 220, 50), pts_inner)
        pygame.draw.circle(surf, (255, 255, 220), (22, 28), 4)
        frames.append(surf)
    return frames

def create_station_icons():
    icons = {}
    s1 = pygame.Surface((36, 36), pygame.SRCALPHA)
    pygame.draw.rect(s1, (170, 180, 200), (6, 2, 24, 32), border_radius=4)
    pygame.draw.rect(s1, (0, 255, 180), (10, 7, 16, 4), border_radius=1)
    pygame.draw.rect(s1, (0, 255, 180), (10, 15, 16, 4), border_radius=1)
    icons[0] = s1

    s2 = pygame.Surface((36, 36), pygame.SRCALPHA)
    pygame.draw.rect(s2, (60, 60, 75), (2, 6, 32, 22), border_radius=4)
    pygame.draw.rect(s2, (255, 255, 255), (5, 10, 6, 6))
    pygame.draw.rect(s2, (255, 255, 255), (15, 10, 6, 6))
    pygame.draw.rect(s2, (255, 255, 255), (25, 10, 6, 6))
    icons[1] = s2

    s3 = pygame.Surface((36, 36), pygame.SRCALPHA)
    pygame.draw.rect(s3, (50, 50, 65), (2, 2, 32, 32), border_radius=4)
    pygame.draw.rect(s3, (0, 255, 140), (7, 18, 4, 11), border_radius=1)
    pygame.draw.rect(s3, (0, 255, 220), (13, 11, 4, 18), border_radius=1)
    pygame.draw.rect(s3, (255, 220, 0), (19, 14, 4, 15), border_radius=1)
    icons[2] = s3

    s4 = pygame.Surface((36, 36), pygame.SRCALPHA)
    pygame.draw.circle(s4, (50, 50, 65), (18, 18), 16)
    pygame.draw.arc(s4, (255, 70, 70), (4, 4, 28, 28), 0, 2.09, 3)
    pygame.draw.arc(s4, (70, 255, 70), (4, 4, 28, 28), 2.09, 4.18, 3)
    icons[3] = s4

    s5 = pygame.Surface((36, 36), pygame.SRCALPHA)
    pygame.draw.line(s5, (200, 150, 100), (4, 32), (25, 11), 3)
    pygame.draw.circle(s5, (255, 255, 120), (28, 8), 6)
    icons[4] = s5

    s6 = pygame.Surface((36, 36), pygame.SRCALPHA)
    pygame.draw.rect(s6, (150, 150, 165), (2, 5, 32, 20), border_radius=3)
    pygame.draw.rect(s6, (0, 230, 255), (4, 7, 28, 16))
    icons[5] = s6

    return icons

player_img = create_pixel_player()
client_img = create_pixel_client()
coffee_mug_img = create_coffee_mug_surface()
fire_frames = create_fire_frames()
station_icons = create_station_icons()

COLOR_BG = (10, 14, 24)
COLOR_GRID = (18, 25, 42)
COLOR_WALL_CYAN = (0, 200, 245)
COLOR_WALL_PURPLE = (170, 60, 245)
COLOR_TEXT = (240, 244, 255)
COLOR_TEXT_MUTED = (130, 145, 175)

PIPELINE_STEPS = [
    {
        "name": "1. INGESTION", 
        "summary": "Transferring raw media files onto secure backup servers and verifying digital checksums so data is 100% safe."
    },
    {
        "name": "2. EDITING", 
        "summary": "Assembling clips into a compelling story timeline. Once approved ('Picture Lock'), the structural cut is frozen."
    },
    {
        "name": "3. SOUND MIX", 
        "summary": "Cleaning dialogue, balancing background music, and adding custom sound effects (Foley) for crisp audio clarity."
    },
    {
        "name": "4. COLOR GRADE", 
        "summary": "Balancing tones, contrast, and color palettes across all shots to establish the right visual mood and style."
    },
    {
        "name": "5. VFX & GRAPHICS", 
        "summary": "Adding digital effects, cleaning up unwanted objects, and incorporating on-screen titles or animations."
    },
    {
        "name": "6. MASTER", 
        "summary": "Performing quality control (QC) checks, formatting codecs, and outputting the final deliverable for platforms."
    }
]

wall_lines = [
    ((30, 20), (930, 20), COLOR_WALL_CYAN),
    ((930, 20), (930, 350), COLOR_WALL_PURPLE),
    ((930, 350), (30, 350), COLOR_WALL_PURPLE),
    ((30, 350), (30, 20), COLOR_WALL_CYAN),
    ((280, 20), (280, 140), COLOR_WALL_CYAN),
    ((280, 210), (280, 350), COLOR_WALL_CYAN),
    ((680, 20), (680, 140), COLOR_WALL_PURPLE),
    ((680, 210), (680, 350), COLOR_WALL_PURPLE),
    ((480, 120), (480, 240), COLOR_WALL_CYAN),
]

collision_walls = []
for line in wall_lines:
    p1, p2, _ = line
    x = min(p1[0], p2[0]) - 3
    y = min(p1[1], p2[1]) - 3
    w = max(abs(p1[0] - p2[0]), 6)
    h = max(abs(p1[1] - p2[1]), 6)
    collision_walls.append(pygame.Rect(x, y, w, h))

STAGE_POSITIONS = [
    (150, 95),
    (830, 95),
    (645, 95),
    (165, 275),
    (625, 285),
    (835, 285),
]

initial_data_drops = [
    {"pos": [380, 100], "active": True},
    {"pos": [380, 260], "active": True},
    {"pos": [580, 100], "active": True},
    {"pos": [580, 260], "active": True},
    {"pos": [320, 185], "active": True},
    {"pos": [720, 185], "active": True},
    {"pos": [480, 55], "active": True},
    {"pos": [480, 300], "active": True},
    {"pos": [880, 185], "active": True},
]

class WaterParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(1.0, 3.5)
        self.vy = random.uniform(-1.0, 1.0)
        self.life = random.randint(12, 20)
        self.color = (0, 200, 255)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 3)

class FloatingText:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.life = 45

    def update(self):
        self.y -= 0.8
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            surf = font_title.render(self.text, True, self.color)
            padding_x = 8
            padding_y = 5
            bg_rect = pygame.Rect(
                int(self.x) - padding_x, 
                int(self.y) - padding_y, 
                surf.get_width() + (padding_x * 2), 
                surf.get_height() + (padding_y * 2)
            )
            pygame.draw.rect(surface, (14, 18, 32), bg_rect, border_radius=6)
            pygame.draw.rect(surface, (45, 60, 95), bg_rect, width=1, border_radius=6)
            surface.blit(surf, (int(self.x), int(self.y)))

def draw_wrapped_text(surface, text, font, color, rect, line_spacing=4):
    words = text.split(' ')
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        if font.size(test_line)[0] <= rect.width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
        
    y = rect.top
    for line in lines:
        line_surf = font.render(line, True, color)
        surface.blit(line_surf, (rect.left, y))
        y += font.get_height() + line_spacing

game_state = "INTRO"

player_rect = pygame.Rect(440, 175, 36, 36)
player_speed = 3
data_collected = 0

client_rect = pygame.Rect(750, 240, 36, 36)
client_speed = 1.3
client_touch_cooldown = 0

elapsed_time = 0.0
time_penalties_added = 0
current_step = 0

particles = []
floating_texts = []
anim_frame = 0
anim_timer = 0
sound_cooldown = 0
data_drops = []

client_quotes = [
    "CAN WE MAKE THE LOGO BIGGER?",
    "I HAVE A FEW QUICK NOTES...",
    "CAN WE CHANGE THE ENTIRE ENDING?",
    "MAKE IT POP MORE!",
    "MY NEPHEW SAYS WE SHOULD CUT IT!",
    "CAN WE DO ONE MORE TAKE?",
    "DO WE HAVE A FUNNIER FONT?"
]

def reset_game():
    global player_rect, client_rect, data_collected, elapsed_time, time_penalties_added, current_step, data_drops, client_touch_cooldown
    player_rect.topleft = (440, 175)
    client_rect.topleft = (750, 240)
    data_collected = 0
    elapsed_time = 0.0
    time_penalties_added = 0
    current_step = 0
    client_touch_cooldown = 0
    data_drops = [{"pos": list(d["pos"]), "active": True} for d in initial_data_drops]

reset_game()

running = True
while running:
    dt = clock.tick(FPS) / 1000.0
    anim_timer += 1
    if anim_timer % 10 == 0:
        anim_frame = (anim_frame + 1) % len(fire_frames)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif game_state == "INTRO":
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    reset_game()
                    game_state = "PLAYING"
            elif game_state == "MILESTONE_PAUSE":
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    if current_step >= len(PIPELINE_STEPS):
                        game_state = "VICTORY"
                    else:
                        game_state = "PLAYING"
            elif game_state == "VICTORY":
                if event.key == pygame.K_r:
                    reset_game()
                    game_state = "PLAYING"

    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx = -1
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = 1
    if keys[pygame.K_UP] or keys[pygame.K_w]: dy = -1
    if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy = 1

    if game_state == "PLAYING":
        elapsed_time += dt

        player_rect.x += dx * player_speed
        for wall in collision_walls:
            if player_rect.colliderect(wall):
                if dx > 0: player_rect.right = wall.left
                if dx < 0: player_rect.left = wall.right

        player_rect.y += dy * player_speed
        for wall in collision_walls:
            if player_rect.colliderect(wall):
                if dy > 0: player_rect.bottom = wall.top
                if dy < 0: player_rect.top = wall.bottom

        for drop in data_drops:
            if drop["active"]:
                drop_rect = pygame.Rect(drop["pos"][0] - 12, drop["pos"][1] - 12, 24, 24)
                if player_rect.colliderect(drop_rect):
                    drop["active"] = False
                    data_collected += 1
                    elapsed_time = max(0.0, elapsed_time - 3.0)
                    floating_texts.append(FloatingText("-3s CAFFEINE BOOST", player_rect.centerx, player_rect.centery - 15, (0, 255, 180)))
                    play_sound("collect")

        if client_rect.centerx < player_rect.centerx: c_dx = 1
        elif client_rect.centerx > player_rect.centerx: c_dx = -1
        else: c_dx = 0

        if client_rect.centery < player_rect.centery: c_dy = 1
        elif client_rect.centery > player_rect.centery: c_dy = -1
        else: c_dy = 0

        client_rect.x += c_dx * client_speed
        for wall in collision_walls:
            if client_rect.colliderect(wall):
                if c_dx > 0: client_rect.right = wall.left
                if c_dx < 0: client_rect.left = wall.right

        client_rect.y += c_dy * client_speed
        for wall in collision_walls:
            if client_rect.colliderect(wall):
                if c_dy > 0: client_rect.bottom = wall.top
                if c_dy < 0: client_rect.top = wall.bottom

        if client_touch_cooldown > 0:
            client_touch_cooldown -= 1

        if player_rect.colliderect(client_rect):
            if client_touch_cooldown == 0:
                elapsed_time += 10.0
                time_penalties_added += 1
                client_touch_cooldown = 90
                funny_quote = random.choice(client_quotes)
                floating_texts.append(FloatingText(f'"{funny_quote}" (+10s)', player_rect.centerx, player_rect.centery - 20, (255, 80, 80)))
                play_sound("penalty")

        tx, ty = STAGE_POSITIONS[current_step]
        target_rect = pygame.Rect(tx - 18, ty - 18, 36, 36)

        extinguish_range = 110 + (data_collected * 3)
        dist = math.hypot(player_rect.centerx - tx, player_rect.centery - ty)
        if dist < extinguish_range:
            for _ in range(2):
                particles.append(WaterParticle(player_rect.centerx, player_rect.centery))
            if sound_cooldown % 15 == 0:
                play_sound("spray")

        if player_rect.colliderect(target_rect):
            play_sound("success")
            current_step += 1
            game_state = "MILESTONE_PAUSE"

    # --- Render ---
    screen.fill(COLOR_BG)

    if game_state == "INTRO":
        title_surf = font_header.render("THE POST-PRODUCTION RUSH: BEHIND THE SCREEN", True, COLOR_WALL_CYAN)
        screen.blit(title_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 60))
        
        credit_surf = font_title.render("Developed by Alessandra Zapata", True, (255, 220, 50))
        screen.blit(credit_surf, (SCREEN_WIDTH // 2 - credit_surf.get_width() // 2, 88))

        intro_desc_1 = font_body.render("An interactive educational game exploring how modern media projects move from raw files to final release.", True, COLOR_TEXT)
        intro_desc_2 = font_body.render("Navigate the studio, grab coffee mugs for time boosts, complete milestones, and dodge last-minute client revisions!", True, COLOR_TEXT_MUTED)
        screen.blit(intro_desc_1, (SCREEN_WIDTH // 2 - intro_desc_1.get_width() // 2, 125))
        screen.blit(intro_desc_2, (SCREEN_WIDTH // 2 - intro_desc_2.get_width() // 2, 150))

        intro_box = pygame.Rect(100, 195, 760, 275)
        pygame.draw.rect(screen, (14, 18, 32), intro_box, border_radius=8)
        pygame.draw.rect(screen, COLOR_WALL_CYAN, intro_box, width=1, border_radius=8)
        
        rules_title = font_header.render("HOW TO PLAY:", True, (255, 220, 50))
        rule_1 = font_body.render("• Move using Arrow Keys or W-A-S-D.", True, COLOR_TEXT)
        rule_2 = font_body.render("• Travel through active stations to complete production steps in order.", True, COLOR_TEXT)
        rule_3 = font_body.render("• Collect coffee mugs ☕ to gain energy and save 3 seconds (-3s).", True, COLOR_TEXT)
        rule_4 = font_body.render("• Avoid the chasing Client! Getting caught adds +10s in revision delays.", True, COLOR_TEXT)
        
        screen.blit(rules_title, (130, 215))
        screen.blit(rule_1, (130, 255))
        screen.blit(rule_2, (130, 290))
        screen.blit(rule_3, (130, 325))
        screen.blit(rule_4, (130, 360))

        prompt_surf = font_title.render("PRESS [SPACE] OR [ENTER] TO BEGIN", True, (0, 255, 180))
        screen.blit(prompt_surf, (SCREEN_WIDTH // 2 - prompt_surf.get_width() // 2, 510))
        
    else:
        for x in range(0, SCREEN_WIDTH, 32):
            pygame.draw.line(screen, COLOR_GRID, (x, 0), (x, 350))
        for y in range(0, 350, 32):
            pygame.draw.line(screen, COLOR_GRID, (0, y), (SCREEN_WIDTH, y))

        for p1, p2, color in wall_lines:
            pygame.draw.line(screen, color, p1, p2, width=3)

        for drop in data_drops:
            if drop["active"]:
                screen.blit(coffee_mug_img, (drop["pos"][0] - 16, drop["pos"][1] - 16))

        for idx, (sx, sy) in enumerate(STAGE_POSITIONS):
            screen.blit(station_icons[idx], (sx - 18, sy - 34))
            label_text = PIPELINE_STEPS[idx]["name"]
            lbl = font_title.render(label_text, True, COLOR_TEXT)
            screen.blit(lbl, (sx - lbl.get_width() // 2, sy + 6))

        if game_state in ("PLAYING", "MILESTONE_PAUSE") and current_step < len(PIPELINE_STEPS):
            fx, fy = STAGE_POSITIONS[current_step]
            screen.blit(fire_frames[anim_frame], (fx - 22, fy - 22))

        for p in particles[:]:
            p.update()
            p.draw(screen)
            if p.life <= 0:
                particles.remove(p)

        for ft in floating_texts[:]:
            ft.update()
            ft.draw(screen)
            if ft.life <= 0:
                floating_texts.remove(ft)

        screen.blit(player_img, (player_rect.x, player_rect.y))
        screen.blit(client_img, (client_rect.x, client_rect.y))
        
        client_lbl = font_small.render("CLIENT", True, (255, 100, 100))
        screen.blit(client_lbl, (client_rect.centerx - client_lbl.get_width() // 2, client_rect.y - 16))

        # --- Minimalist Dashboard Container ---
        ui_panel = pygame.Rect(0, 350, SCREEN_WIDTH, 290)
        pygame.draw.rect(screen, (12, 16, 28), ui_panel)
        pygame.draw.line(screen, (28, 38, 65), (0, 350), (SCREEN_WIDTH, 350), width=2)

        line_start_x = 40
        line_end_x = SCREEN_WIDTH - 40
        line_y = 378
        pygame.draw.line(screen, (28, 38, 65), (line_start_x, line_y), (line_end_x, line_y), width=3)

        segment_width = (line_end_x - line_start_x) / (len(PIPELINE_STEPS) - 1)
        for i, step in enumerate(PIPELINE_STEPS):
            nx = line_start_x + (i * segment_width)
            is_done = i < current_step or game_state == "VICTORY"
            is_active = i == current_step and game_state in ("PLAYING", "MILESTONE_PAUSE")

            node_color = (0, 255, 160) if is_done else ((255, 90, 90) if is_active else (45, 60, 90))
            pygame.draw.circle(screen, node_color, (int(nx), line_y), 5)
            if is_active:
                pygame.draw.circle(screen, (255, 255, 255), (int(nx), line_y), 2)

            label_color = COLOR_TEXT if is_active else (COLOR_TEXT_MUTED if not is_done else (0, 220, 140))
            step_lbl = font_small.render(step["name"], True, label_color)
            screen.blit(step_lbl, (int(nx) - step_lbl.get_width() // 2, line_y + 11))

        # Content Card with Safe Inner Padding
        card_bg = pygame.Rect(24, 408, SCREEN_WIDTH - 48, 180)
        pygame.draw.rect(screen, (16, 21, 38), card_bg, border_radius=6)
        pygame.draw.rect(screen, (32, 45, 75), card_bg, width=1, border_radius=6)

        timer_color = (255, 90, 90) if client_touch_cooldown > 0 else (255, 220, 50)
        timer_lbl = font_header.render(f"PROJECT CLOCK: {elapsed_time:.1f}s", True, timer_color)
        screen.blit(timer_lbl, (SCREEN_WIDTH - timer_lbl.get_width() - 44, 424))

        if game_state == "VICTORY":
            screen.blit(font_header.render("STATUS: FINAL PROJECT DELIVERED!", True, (0, 255, 160)), (44, 424))
            screen.blit(font_body.render(f"Final Time: {elapsed_time:.1f}s  |  Coffee Mugs: {data_collected}/{len(initial_data_drops)}  |  Client Interventions: {time_penalties_added}", True, COLOR_TEXT), (44, 462))
            congrats_box = font_body.render("Great job! You successfully guided the project through all 6 phases of post-production.", True, COLOR_WALL_CYAN)
            screen.blit(congrats_box, (44, 492))
            
            replay_lbl = font_title.render("PRESS [R] TO REPLAY", True, (255, 220, 50))
            screen.blit(replay_lbl, (44, 532))
        else:
            completed_index = current_step - 1 if game_state == "MILESTONE_PAUSE" else current_step
            info = PIPELINE_STEPS[completed_index] if game_state == "MILESTONE_PAUSE" else PIPELINE_STEPS[current_step]
            
            screen.blit(font_header.render(f"ACTIVE STAGE: {info['name']}", True, (255, 90, 90)), (44, 424))
            
            summary_rect = pygame.Rect(44, 464, SCREEN_WIDTH - 88, 60)
            draw_wrapped_text(screen, info["summary"], font_body, COLOR_TEXT, summary_rect, line_spacing=5)

            hint_lbl = font_small.render(f"COFFEE MUGS COLLECTED: {data_collected}/{len(initial_data_drops)} (-3s each)  |  AVOID CLIENT NOTES (+10s)", True, COLOR_TEXT_MUTED)
            screen.blit(hint_lbl, (44, 546))

        # --- Popup Pause Card ---
        if game_state == "MILESTONE_PAUSE":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            card_w, card_h = 600, 220
            card_x = (SCREEN_WIDTH - card_w) // 2
            card_y = (350 - card_h) // 2
            card_rect = pygame.Rect(card_x, card_y, card_w, card_h)

            pygame.draw.rect(screen, (230, 235, 245), card_rect, border_radius=6)
            pygame.draw.rect(screen, (255, 255, 255), card_rect, width=2, border_radius=6)

            completed_step_info = PIPELINE_STEPS[current_step - 1]
            title_card_surf = font_header.render(f"STAGE COMPLETE: {completed_step_info['name']}", True, (15, 22, 38))
            screen.blit(title_card_surf, (card_x + 24, card_y + 22))

            text_area = pygame.Rect(card_x + 24, card_y + 64, card_w - 48, 85)
            draw_wrapped_text(screen, completed_step_info["summary"], font_body, (35, 45, 65), text_area, line_spacing=5)

            prompt_card_surf = font_title.render("PRESS [SPACE] TO CONTINUE", True, (0, 120, 190))
            screen.blit(prompt_card_surf, (card_x + (card_w - prompt_card_surf.get_width()) // 2, card_y + 168))

    pygame.display.flip()

pygame.quit()
sys.exit()