"""Generate placeholder background images for the flood simulation."""
import pygame
import os

pygame.init()

# Create 800x600 surfaces for each level (scaled down from 1200x800)
SCALE = 2/3  # 800/1200 = 600/800 = 2/3

# ION Mall - Glass facade with steps
def create_ion_mall():
    surf = pygame.Surface((800, 600))
    # Sky gradient
    for y in range(300):
        color = (135 - y//8, 206 - y//8, 235 - y//8)
        pygame.draw.line(surf, color, (0, y), (800, y))
    # Building facade - glass panels
    pygame.draw.rect(surf, (50, 50, 70), (67, 112, 667, 300))
    # Glass panels
    for i in range(8):
        for j in range(4):
            x = 80 + i * 80
            y = 127 + j * 67
            pygame.draw.rect(surf, (100, 150, 200), (x, y, 67, 52))
            pygame.draw.rect(surf, (150, 200, 255), (x+3, y+3, 60, 45))
    # Entrance area
    pygame.draw.rect(surf, (80, 80, 100), (300, 262, 200, 150))
    pygame.draw.ellipse(surf, (200, 200, 220), (333, 287, 133, 112))
    # Steps leading up
    for i in range(8):
        y = 315 + i * 15
        shade = 180 - i * 10
        pygame.draw.rect(surf, (shade, shade, shade), (0, y, 800, 15))
    # People silhouettes
    for i in range(5):
        x = 133 + i * 100
        pygame.draw.ellipse(surf, (60, 40, 40), (x, 375, 13, 30))
        pygame.draw.circle(surf, (255, 200, 150), (x+7, 368), 9)
    return surf

# Orchard Road - Street scene
def create_orchard_road():
    surf = pygame.Surface((800, 600))
    # Night sky
    surf.fill((20, 20, 40))
    # Buildings
    pygame.draw.rect(surf, (40, 40, 60), (0, 75, 200, 300))
    pygame.draw.rect(surf, (50, 50, 70), (600, 75, 200, 300))
    # Road surface
    pygame.draw.rect(surf, (60, 60, 70), (0, 413, 800, 187))
    # Road markings
    for i in range(8):
        x = i * 100
        pygame.draw.rect(surf, (200, 200, 100), (x, 487, 33, 7))
    # Bus (left side)
    pygame.draw.rect(surf, (50, 100, 50), (33, 360, 100, 90))
    pygame.draw.rect(surf, (100, 150, 100), (40, 367, 27, 30))
    pygame.draw.rect(surf, (100, 150, 100), (73, 367, 27, 30))
    pygame.draw.circle(surf, (30, 30, 30), (60, 450), 17)
    pygame.draw.circle(surf, (30, 30, 30), (107, 450), 17)
    # Taxi
    pygame.draw.rect(surf, (255, 200, 50), (167, 390, 67, 45))
    pygame.draw.rect(surf, (100, 150, 200), (173, 397, 20, 19))
    pygame.draw.circle(surf, (30, 30, 30), (187, 435), 13)
    pygame.draw.circle(surf, (30, 30, 30), (213, 435), 13)
    # More cars
    pygame.draw.rect(surf, (150, 50, 50), (367, 397, 60, 38))
    pygame.draw.rect(surf, (200, 200, 200), (467, 393, 53, 41))
    # Decorative lanterns (hanging)
    colors = [(255, 50, 50), (255, 200, 50), (50, 150, 255), (255, 100, 150)]
    for i in range(10):
        x = 67 + i * 70
        y = 38 + (i % 3) * 30
        color = colors[i % 4]
        pygame.draw.circle(surf, color, (x, y), 17)
        pygame.draw.line(surf, (100, 100, 100), (x, 0), (x, y-17))
    return surf

# Tanglin Carpark - Basement parking
def create_carpark():
    surf = pygame.Surface((800, 600))
    # Concrete walls/ceiling
    surf.fill((120, 120, 130))
    # Floor with blue markings
    pygame.draw.rect(surf, (80, 100, 120), (0, 450, 800, 150))
    # Blue floor area
    pygame.draw.rect(surf, (60, 80, 120), (0, 487, 800, 113))
    # Parking lines
    for i in range(7):
        x = i * 120
        pygame.draw.line(surf, (200, 200, 200), (x, 487), (x, 600), 3)
    # Yellow car (left)
    pygame.draw.rect(surf, (255, 220, 100), (53, 465, 67, 60))
    pygame.draw.rect(surf, (100, 150, 200), (60, 472, 27, 22))
    pygame.draw.rect(surf, (100, 150, 200), (93, 472, 20, 22))
    pygame.draw.circle(surf, (40, 40, 40), (73, 525), 12)
    pygame.draw.circle(surf, (40, 40, 40), (100, 525), 12)
    # Black cars (center)
    pygame.draw.rect(surf, (40, 40, 50), (320, 468, 60, 52))
    pygame.draw.circle(surf, (30, 30, 30), (340, 521), 11)
    pygame.draw.circle(surf, (30, 30, 30), (360, 521), 11)
    pygame.draw.rect(surf, (40, 40, 50), (453, 468, 60, 52))
    pygame.draw.circle(surf, (30, 30, 30), (473, 521), 11)
    pygame.draw.circle(surf, (30, 30, 30), (493, 521), 11)
    # White car (right)
    pygame.draw.rect(surf, (220, 220, 230), (653, 465, 63, 56))
    pygame.draw.rect(surf, (100, 150, 200), (660, 472, 23, 22))
    pygame.draw.circle(surf, (40, 40, 40), (673, 521), 11)
    pygame.draw.circle(surf, (40, 40, 40), (697, 521), 11)
    # Pillars (green/white)
    for x in [233, 567]:
        pygame.draw.rect(surf, (100, 150, 100), (x, 300, 40, 300))
        pygame.draw.rect(surf, (200, 220, 200), (x+7, 300, 27, 300))
    # Ceiling pipes
    pygame.draw.rect(surf, (80, 80, 90), (0, 75, 800, 22))
    pygame.draw.rect(surf, (100, 100, 110), (0, 38, 800, 15))
    # Drain in floor
    pygame.draw.ellipse(surf, (40, 40, 50), (387, 540, 27, 15))
    return surf

# Generate and save
if __name__ == "__main__":
    os.makedirs(".", exist_ok=True)
    
    ion = create_ion_mall()
    pygame.image.save(ion, "ion-mall.png")
    print("Generated ion-mall.png")
    
    orchard = create_orchard_road()
    pygame.image.save(orchard, "orchard-road.png")
    print("Generated orchard-road.png")
    
    carpark = create_carpark()
    pygame.image.save(carpark, "tanglin-carpark.png")
    print("Generated tanglin-carpark.png")
