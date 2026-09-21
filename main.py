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
pygame.display.set_caption("Post Production Behind the Screen Pipeline")
clock = pygame.time.Clock()

# --- Custom Retro Editing App Icon Generator ---
def create_app_icon():
    # Creates a 32x32 retro computer monitor / timeline icon
    icon_surf = pygame.Surface((32, 32), pygame.SRCALPHA)
    # Monitor outer shell
    pygame.draw.rect(icon_surf, (45, 55, 75), (2, 2, 28, 20), border_radius=3)
    # Screen display area
    pygame.draw.rect(icon_surf, (14, 18, 32), (4, 4, 24, 16), border_radius=2)
    # Timeline tracks inside screen
    pygame.draw.rect(icon_surf, (0, 255, 180), (6, 7, 10, 3), border_radius=1)
    pygame.draw.rect(icon_surf, (255, 90, 90), (12, 12, 12, 3), border_radius=1)
    # Monitor stand base
    pygame.draw.rect(icon_surf, (70, 80, 100), (12, 22, 8, 4))
    pygame.draw.rect(icon_surf, (90, 100, 120), (8, 26, 16, 3), border_radius=1)
    return icon_surf

# Set window icon
pygame.display.set_icon(create_app_icon())

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
        elif sound_type == "victory":
            notes = [392.0, 523.25, 659.25, 783.99, 659.25, 523.25]
            note_duration = 0.14
            applause_duration = 0.75
            total_duration = len(notes) * note_duration + applause_duration
            total_samples = int(sample_rate * total_duration)
            buffer = bytearray()
            for sample_index in range(total_samples):
                t = sample_index / sample_rate
                melody_value = 0.0
                note_index = int(t / note_duration)
                if note_index < len(notes):
                    note_time = t - note_index * note_duration
                    envelope = min(1.0, note_time / (note_duration * 0.85))
                    note = notes[note_index]
                    crowd_wobble = 0.55 + 0.45 * math.sin(2 * math.pi * (3.5 + note_index * 0.2) * note_time)
                    harmonic = 0.7 * math.sin(2 * math.pi * note * note_time) + 0.3 * math.sin(2 * math.pi * (note * 2) * note_time + 0.5)
                    melody_value = 22000 * harmonic * crowd_wobble * envelope

                applause_time = t
                clap_phase = (applause_time * 4.5) % 1.0
                clap_envelope = max(0.0, 1.0 - clap_phase * 8.0)
                clap_wave = math.sin(2 * math.pi * (260 + 110 * math.sin(2 * math.pi * 3 * applause_time)) * applause_time)
                crowd_wave = math.sin(2 * math.pi * 70 * applause_time) * (0.55 + 0.45 * math.sin(2 * math.pi * 1.8 * applause_time))
                applause_fade = min(1.0, t / 0.12) * max(0.0, 1.0 - max(0.0, t - 1.0) / 0.59)
                applause_value = (10500 * clap_envelope * clap_wave + 2600 * crowd_wave) * applause_fade
                val = max(-32767, min(32767, int(melody_value + applause_value)))
                buffer += val.to_bytes(2, byteorder='little', signed=True)
                buffer += val.to_bytes(2, byteorder='little', signed=True)
            sound = pygame.mixer.Sound(buffer=bytes(buffer))
            sound.set_volume(0.14)
            sound.play()
            return
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
    pygame.draw.rect(surf, (70, 40, 28), (9, 2, 18, 10))
    pygame.draw.rect(surf, (255, 220, 177), (10, 4, 16, 12))
    pygame.draw.rect(surf, (0, 0, 0), (13, 7, 3, 3))
    pygame.draw.rect(surf, (0, 0, 0), (20, 7, 3, 3))
    pygame.draw.rect(surf, (70, 40, 28), (24, 6, 5, 9))
    pygame.draw.rect(surf, (45, 55, 75), (8, 5, 3, 8))
    pygame.draw.rect(surf, (45, 55, 75), (25, 5, 3, 8))
    pygame.draw.rect(surf, (45, 55, 75), (11, 3, 14, 2))
    pygame.draw.rect(surf, (220, 80, 120), (8, 16, 20, 12))
    pygame.draw.rect(surf, (255, 255, 255), (13, 18, 10, 5))
    pygame.draw.rect(surf, (55, 70, 110), (12, 30, 5, 6))
    pygame.draw.rect(surf, (55, 70, 110), (19, 30, 5, 6))
    return surf

def create_pixel_client():
    surf = pygame.Surface((36, 36), pygame.SRCALPHA)
    pygame.draw.rect(surf, (240, 200, 150), (10, 4, 16, 12))
    pygame.draw.rect(surf, (0, 0, 0), (13, 7, 3, 3))
    pygame.draw.rect(surf, (0, 0, 0), (20, 7, 3, 3))
    pygame.draw.rect(surf, (30, 30, 30), (8, 16, 20, 14))
    pygame.draw.rect(surf, (200, 50, 50), (17, 18, 3, 7))
    pygame.draw.rect(surf, (50, 50, 50), (12, 30, 5, 6))
    pygame.draw.rect(surf, (50, 50, 50), (19, 30, 5, 6))
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
    s1 = pygame.Surface((100, 100), pygame.SRCALPHA)
    pygame.draw.rect(s1, (170, 180, 200), (6, 2, 24, 32), border_radius=4)
    pygame.draw.rect(s1, (0, 255, 180), (10, 7, 16, 4), border_radius=1)
    pygame.draw.rect(s1, (0, 255, 180), (10, 15, 16, 4), border_radius=1)
    icons[0] = s1

    s2 = pygame.Surface((100, 100), pygame.SRCALPHA)
    pygame.draw.rect(s2, (60, 60, 75), (2, 6, 32, 22), border_radius=4)
    pygame.draw.rect(s2, (255, 255, 255), (5, 10, 6, 6))
    pygame.draw.rect(s2, (255, 255, 255), (15, 10, 6, 6))
    pygame.draw.rect(s2, (255, 255, 255), (25, 10, 6, 6))
    icons[1] = s2

    s3 = pygame.Surface((100, 100), pygame.SRCALPHA)
    pygame.draw.rect(s3, (50, 50, 65), (2, 2, 32, 32), border_radius=4)
    pygame.draw.rect(s3, (0, 255, 140), (7, 18, 4, 11), border_radius=1)
    pygame.draw.rect(s3, (0, 255, 220), (13, 11, 4, 18), border_radius=1)
    pygame.draw.rect(s3, (255, 220, 0), (19, 14, 4, 15), border_radius=1)
    icons[2] = s3

    s4 = pygame.Surface((100, 100), pygame.SRCALPHA)
    pygame.draw.circle(s4, (50, 50, 65), (18, 18), 16)
    pygame.draw.arc(s4, (255, 70, 70), (4, 4, 28, 28), 0, 2.09, 3)
    pygame.draw.arc(s4, (70, 255, 70), (4, 4, 28, 28), 2.09, 4.18, 3)
    icons[3] = s4

    s5 = pygame.Surface((100, 100), pygame.SRCALPHA)
    pygame.draw.line(s5, (200, 150, 100), (4, 32), (25, 11), 3)
    pygame.draw.circle(s5, (255, 255, 120), (28, 8), 6)
    icons[4] = s5

    s6 = pygame.Surface((100, 100), pygame.SRCALPHA)
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
COLOR_TEXT = (240, 244, 255)
COLOR_TEXT_MUTED = (130, 145, 175)

PIPELINE_STEPS = [
    {
        "name": "1. INGEST", 
        "summary": "Offload camera cards onto secure drives with checksum verification. Next: Edit.",
        "completion": "Congrats! You saved the camera footage onto secure drives and verified the backups."
    },
    {
        "name": "2. EDIT", 
        "summary": "Cut selects, lock picture, export an XML for color and an AAF/OMF for audio. Next: Sound.",
        "completion": "Congrats! You locked the picture and exported the files needed for sound and color."
    },
    {
        "name": "3. SOUND", 
        "summary": "Import audio packages into a DAW for dialogue cleanup, Foley, and final mixing. Next: Color.",
        "completion": "Congrats! You cleaned up the dialogue, added Foley, and completed the final mix."
    },
    {
        "name": "4. COLOR", 
        "summary": "Conform the XML timeline with camera-originals to match tones and grade shots. Next: VFX.",
        "completion": "Congrats! You conformed the timeline and gave the footage its final color grade."
    },
    {
        "name": "5. VFX", 
        "summary": "Composite digital elements, clean up artifacts, and bake in graphical titles. Next: Master.",
        "completion": "Congrats! You finished the visual effects, cleanup, and graphical titles."
    },
    {
        "name": "6. MASTER", 
        "summary": "Run QC checks, verify delivery codecs, and export web/social formats. Next: Release!",
        "completion": "Congrats! You passed QC and exported the final delivery masters."
    }
]

wall_lines = [
    ((30, 20), (930, 20), COLOR_WALL_CYAN),
    ((930, 20), (930, 350), COLOR_WALL_CYAN),
    ((930, 350), (30, 350), COLOR_WALL_CYAN),
    ((30, 350), (30, 20), COLOR_WALL_CYAN),
    ((280, 20), (280, 140), COLOR_WALL_CYAN),
    ((280, 210), (280, 350), COLOR_WALL_CYAN),
    ((680, 20), (680, 140), COLOR_WALL_CYAN),
    ((680, 210), (680, 350), COLOR_WALL_CYAN),
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
    (150, 95),   # 0: Ingestion
    (810, 95),   # 1: Editing
    (580, 95),   # 2: Sound Mix
    (150, 275),  # 3: Color Grade
    (600, 275),  # 4: VFX & Graphics
    (835, 275),  # 5: Master
]

initial_data_drops = [
    {"pos": [380, 110], "active": True},
    {"pos": [380, 260], "active": True},
    {"pos": [580, 140], "active": True},
    {"pos": [580, 200], "active": True},
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
            text_x = max(8, min(int(self.x), SCREEN_WIDTH - surf.get_width() - 8))
            text_y = max(8, min(int(self.y), SCREEN_HEIGHT - surf.get_height() - 8))
            bg_rect = pygame.Rect(
                text_x - padding_x,
                text_y - padding_y,
                surf.get_width() + (padding_x * 2),
                surf.get_height() + (padding_y * 2)
            )
            bg_rect.x = max(0, min(bg_rect.x, SCREEN_WIDTH - bg_rect.width))
            bg_rect.y = max(0, min(bg_rect.y, SCREEN_HEIGHT - bg_rect.height))
            pygame.draw.rect(surface, (14, 18, 32), bg_rect, border_radius=6)
            pygame.draw.rect(surface, (45, 60, 95), bg_rect, width=1, border_radius=6)
            surface.blit(surf, (bg_rect.x + padding_x, bg_rect.y + padding_y))

def draw_wrapped_text(surface, text, font, color, rect, line_spacing=4):
    usable_width = max(80, min(rect.width, SCREEN_WIDTH - rect.left - 16))
    words = text.split(' ')
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        if font.size(test_line)[0] <= usable_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    
    y = rect.top
    for line in lines:
        line_surf = font.render(line, True, color)
        surface.blit(line_surf, (rect.left, y))
        y += font.get_height() + line_spacing

def draw_centered_multiline_text(surface, text, font, color, center_x, y, max_width=120, line_spacing=4):
    words = text.split()
    if not words:
        return

    lines = []
    current_line = []
    for word in words:
        candidate = ' '.join(current_line + [word])
        if font.size(candidate)[0] <= max_width or not current_line:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))

    for idx, line in enumerate(lines[:2]):
        line_surf = font.render(line, True, color)
        x = center_x - line_surf.get_width() // 2
        surface.blit(line_surf, (x, y + idx * (font.get_height() + line_spacing)))

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
victory_sound_played = False
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

def get_safe_message_position(x, y, offset=90):
    margin = 26
    if x < SCREEN_WIDTH * 0.25:
        x = min(x + offset, SCREEN_WIDTH - margin)
    elif x > SCREEN_WIDTH * 0.75:
        x = max(x - offset, margin)
    x = max(margin, min(x, SCREEN_WIDTH - margin))
    y = max(30, min(y, SCREEN_HEIGHT - 90))
    return int(x), int(y)

def reset_game():
    global player_rect, client_rect, data_collected, elapsed_time, time_penalties_added, current_step, data_drops, client_touch_cooldown, victory_sound_played
    player_rect.topleft = (440, 175)
    client_rect.topleft = (750, 240)
    data_collected = 0
    elapsed_time = 0.0
    time_penalties_added = 0
    current_step = 0
    client_touch_cooldown = 0
    victory_sound_played = False
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
                    msg_x, msg_y = get_safe_message_position(player_rect.centerx, player_rect.centery - 15)
                    floating_texts.append(FloatingText("-3s CAFFEINE BOOST", msg_x, msg_y, (0, 255, 180)))
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
                msg_x, msg_y = get_safe_message_position(player_rect.centerx, player_rect.centery - 20)
                floating_texts.append(FloatingText(f'"{funny_quote}" (+10s)', msg_x, msg_y, (255, 80, 80)))
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
            if current_step >= len(PIPELINE_STEPS):
                game_state = "VICTORY"
                victory_sound_played = False
            else:
                game_state = "MILESTONE_PAUSE"

    if game_state == "VICTORY" and not victory_sound_played:
        play_sound("victory")
        victory_sound_played = True

    # --- Render ---
    screen.fill(COLOR_BG)

    if game_state == "INTRO":
        title_surf = font_header.render("POST PRODUCTION BEHIND THE SCREEN PIPELINE", True, COLOR_WALL_CYAN)
        screen.blit(title_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 60))
        
        credit_surf = font_title.render("Developed by Alessandra Zapata", True, (255, 220, 50))
        screen.blit(credit_surf, (SCREEN_WIDTH // 2 - credit_surf.get_width() // 2, 88))

        intro_desc_1 = font_body.render("An interactive educational game exploring how modern video projects move from raw files to final release.", True, COLOR_TEXT)
        intro_desc_2a = font_body.render("Step onto the chaotic studio floor: navigate through the workspace, extinguish rushing production", True, COLOR_TEXT_MUTED)
        intro_desc_2b = font_body.render("flames, grab coffee mugs for time boosts, hit milestones, and dodge those dreaded client revisions!", True, COLOR_TEXT_MUTED)
        
        screen.blit(intro_desc_1, (SCREEN_WIDTH // 2 - intro_desc_1.get_width() // 2, 120))
        screen.blit(intro_desc_2a, (SCREEN_WIDTH // 2 - intro_desc_2a.get_width() // 2, 145))
        screen.blit(intro_desc_2b, (SCREEN_WIDTH // 2 - intro_desc_2b.get_width() // 2, 168))

        intro_box = pygame.Rect(100, 205, 760, 265)
        pygame.draw.rect(screen, (14, 18, 32), intro_box, border_radius=8)
        pygame.draw.rect(screen, COLOR_WALL_CYAN, intro_box, width=1, border_radius=8)
        
        rules_title = font_header.render("HOW TO PLAY:", True, (255, 220, 50))
        rule_1 = font_body.render("• Move using Arrow Keys or W-A-S-D.", True, COLOR_TEXT)
        rule_2 = font_body.render("• Travel through active stations to complete production steps in order.", True, COLOR_TEXT)
        rule_3 = font_body.render("• Collect coffee mugs ☕ to gain energy and save 3 seconds (-3s).", True, COLOR_TEXT)
        rule_4 = font_body.render("• Avoid the chasing Client! Getting caught adds +10s in revision delays.", True, COLOR_TEXT)
        
        screen.blit(rules_title, (130, 220))
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
            pygame.draw.line(screen, color, p1, p2, width=5)

        for drop in data_drops:
            if drop["active"]:
                screen.blit(coffee_mug_img, (drop["pos"][0] - 16, drop["pos"][1] - 16))

        for idx, (sx, sy) in enumerate(STAGE_POSITIONS):
            screen.blit(station_icons[idx], (sx - 18, sy - 34))
            label_text = PIPELINE_STEPS[idx]["name"]
            draw_centered_multiline_text(screen, label_text, font_title, COLOR_TEXT, sx, sy + 6, max_width=110, line_spacing=2)

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
            
            replay_lbl = font_title.render("PRESS [R] TO REPLAY    |    PRESS [ESC] TO EXIT", True, (255, 220, 50))
            screen.blit(replay_lbl, (44, 532))
        else:
            completed_index = current_step - 1 if game_state == "MILESTONE_PAUSE" else current_step
            info = PIPELINE_STEPS[completed_index] if game_state == "MILESTONE_PAUSE" else PIPELINE_STEPS[current_step]
            
            screen.blit(font_header.render(f"ACTIVE STAGE: {info['name']}", True, (255, 90, 90)), (44, 424))
            
            summary_rect = pygame.Rect(44, 464, SCREEN_WIDTH - 88, 60)
            draw_wrapped_text(screen, info["summary"], font_body, COLOR_TEXT, summary_rect, line_spacing=5)

            hint_lbl = font_small.render(f"COFFEE MUGS COLLECTED: {data_collected}/{len(initial_data_drops)} (-3s each)  |  AVOID CLIENT NOTES (+10s)", True, COLOR_TEXT_MUTED)
            screen.blit(hint_lbl, (44, 546))

        # --- Milestone Pause Popup Card (Single Instance) ---
        if game_state == "MILESTONE_PAUSE":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))

            popup_rect = pygame.Rect(180, 130, 600, 310)
            pygame.draw.rect(screen, (16, 21, 38), popup_rect, border_radius=8)
            pygame.draw.rect(screen, COLOR_WALL_CYAN, popup_rect, width=2, border_radius=8)

            completed_step_info = PIPELINE_STEPS[current_step - 1]
            
            title_popup = font_header.render(f"STAGE COMPLETE: {completed_step_info['name']}", True, (0, 255, 160))
            screen.blit(title_popup, (popup_rect.centerx - title_popup.get_width() // 2, popup_rect.top + 35))

            desc_y = popup_rect.top + 90
            draw_wrapped_text(screen, completed_step_info["completion"], font_body, COLOR_TEXT, 
                              pygame.Rect(popup_rect.left + 40, desc_y, popup_rect.width - 80, 100), line_spacing=6)

            prompt_popup = font_title.render("PRESS [SPACE] TO CONTINUE", True, (255, 220, 50))
            screen.blit(prompt_popup, (popup_rect.centerx - prompt_popup.get_width() // 2, popup_rect.bottom - 60))

    pygame.display.flip()

pygame.quit()
sys.exit()
