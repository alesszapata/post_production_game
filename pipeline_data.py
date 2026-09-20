# pipeline_data.py

# Neon Cyberpunk Palette
COLOR_BG = (10, 10, 18)
COLOR_WALL = (0, 220, 255)            # Cyan glowing maze walls
COLOR_PLAYER = (255, 210, 0)          # Yellow / Producer Character
COLOR_FIRE = (255, 50, 50)            # Red Flame Issue
COLOR_WATER = (0, 255, 150)           # Green Spray Effect
COLOR_TEXT = (240, 240, 255)
COLOR_TEXT_MUTED = (140, 150, 180)
COLOR_UI_BG = (18, 20, 32)

# Grid Configuration
GRID_SIZE = 32

# Narrative Pipeline Steps
PIPELINE_STEPS = [
    {"name": "1. INGEST & ASSEMBLY", "desc": "Raw footage ingested, checksums verified, and rough assembly created."},
    {"name": "2. PICTURE CUT & LOCK", "desc": "Editorial refines story cut. Picture Lock confirms timing for audio and VFX."},
    {"name": "3. SOUND DESIGN & MIX", "desc": "ADR cleanup, Foley, score placement, and final surround sound mix."},
    {"name": "4. COLOR GRADING", "desc": "Colorist balances dynamic range and establishes artistic mood palettes."},
    {"name": "5. VFX & COMPOSITING", "desc": "Green screen cleanup, CGI integration, and title graphics placement."},
    {"name": "6. MASTER DELIVERY & QC", "desc": "Final Quality Control checks for broadcast specs and master export."}
]

# Tile Map Layout (1 = Wall, 0 = Corridor)
MAZE_MAP = [
    "111111111111111111111111111111",
    "100000000011000000000000000001",
    "101111110011001111111100111101",
    "101111110000001111111100111101",
    "100000000011000000000000000001",
    "111100111111111100111111110011",
    "111100111111111100111111110011",
    "100000000000000000000000000001",
    "101111001111111111110011111101",
    "101111001111111111110011111101",
    "100000000000000000000000000001",
    "111111111111111111111111111111",
]

# Adjusted Stage Coordinates to match corridor spaces precisely
STAGE_NODES = [
    (2, 1),   # Step 1: Ingest (Top Left)
    (27, 1),  # Step 2: Picture Cut (Top Right)
    (2, 4),   # Step 3: Sound Design (Middle Left)
    (27, 4),  # Step 4: Color Grading (Middle Right)
    (2, 10),  # Step 5: VFX (Bottom Left)
    (27, 10)  # Step 6: Master QC (Bottom Right)
]   