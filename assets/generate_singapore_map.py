"""Generate a placeholder pixelated Singapore map image."""
import pygame
import os

# Initialize pygame
pygame.init()

# Create 800x600 surface for the map
WIDTH, HEIGHT = 800, 600
screen = pygame.Surface((WIDTH, HEIGHT))

# Colors (pixel art palette)
WATER = (70, 110, 160)  # Ocean blue
LAND_BASE = (110, 150, 80)  # Green land
LAND_LIGHT = (140, 180, 110)  # Highlight
LAND_DARK = (80, 120, 50)  # Shadow
BORDER = (50, 80, 40)  # Coastline

# Fill with water
screen.fill(WATER)

# Singapore island shape (pixel grid aligned, centered)
center_x, center_y = WIDTH // 2, HEIGHT // 2

# Define island outline (diamond-ish shape for Singapore)
# Coordinates relative to center
island_points = [
    (center_x, center_y - 160),      # North (Woodlands)
    (center_x + 60, center_y - 120),  # Northeast
    (center_x + 100, center_y - 60),  # East (Tampines)
    (center_x + 80, center_y),        # East coast
    (center_x + 60, center_y + 80),   # Southeast (Marina)
    (center_x + 20, center_y + 140),  # South (Sentosa area)
    (center_x - 20, center_y + 120),  # Southwest
    (center_x - 80, center_y + 60),   # West (Jurong)
    (center_x - 120, center_y - 20),  # West
    (center_x - 100, center_y - 80),  # Northwest
    (center_x - 40, center_y - 140),  # North
]

# Draw main island
pygame.draw.polygon(screen, LAND_BASE, island_points)

# Draw inner highlight (for depth)
inner_points = [
    (center_x, center_y - 140),
    (center_x + 50, center_y - 100),
    (center_x + 85, center_y - 50),
    (center_x + 70, center_y),
    (center_x + 50, center_y + 70),
    (center_x + 15, center_y + 120),
    (center_x - 15, center_y + 100),
    (center_x + 15, center_y + 100),  # Correction
    (center_x - 70, center_y + 50),
    (center_x - 105, center_y - 10),
    (center_x - 90, center_y - 70),
    (center_x - 35, center_y - 125),
]

# Simplified inner highlight
inner_offset = 15
inner_highlight = [(x + (center_x - x) // 10, y + (center_y - y) // 10) for x, y in island_points]
pygame.draw.polygon(screen, LAND_LIGHT, inner_highlight)

# Draw border
pygame.draw.polygon(screen, BORDER, island_points, 4)

# Add some pixel details (small islands)
small_islands = [
    (center_x + 110, center_y + 100, 15),  # Sentosa-ish
    (center_x - 130, center_y + 40, 10),   # Small western island
    (center_x + 130, center_y - 80, 8),    # Northeast small
]

for ix, iy, size in small_islands:
    pygame.draw.ellipse(screen, LAND_BASE, (ix - size, iy - size//2, size*2, size))
    pygame.draw.ellipse(screen, BORDER, (ix - size, iy - size//2, size*2, size), 2)

# Add pixel dithering along coast for retro feel
import random
random.seed(42)  # Consistent pattern
for i, (x, y) in enumerate(island_points):
    next_point = island_points[(i + 1) % len(island_points)]
    # Add some random pixel blocks along edges
    for _ in range(5):
        t = random.random()
        px = int(x + (next_point[0] - x) * t)
        py = int(y + (next_point[1] - y) * t)
        # Snap to 8-pixel grid for pixel art look
        px = (px // 8) * 8
        py = (py // 8) * 8
        pygame.draw.rect(screen, LAND_DARK, (px, py, 8, 8))

# Mark zone locations with subtle indicators
zone_markers = [
    (center_x - 100, center_y - 60, (160, 100, 90)),    # Tanglin (danger - red tint)
    (center_x, center_y - 10, (180, 160, 80)),          # Orchard (moderate - yellow tint)
    (center_x + 80, center_y - 40, (100, 160, 100)),    # ION (safe - green tint)
]

for zx, zy, color in zone_markers:
    # Subtle zone indicator (very light)
    indicator = pygame.Surface((60, 40), pygame.SRCALPHA)
    pygame.draw.ellipse(indicator, (*color, 30), (0, 0, 60, 40))
    screen.blit(indicator, (zx - 30, zy - 20))

# Ensure assets directory exists
os.makedirs("flood_sim/assets", exist_ok=True)

# Save the image
output_path = "flood_sim/assets/singapore-map.png"
pygame.image.save(screen, output_path)
print(f"Generated placeholder Singapore map: {output_path}")

pygame.quit()
