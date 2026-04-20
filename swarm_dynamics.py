import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set the width and height of the screen
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Interactive Boids Simulation")

# Colors
DARK_BG = (30, 30, 40)
BOID_COLOR = (0, 200, 255)
UI_BG = (50, 50, 60)
WHITE = (255, 255, 255)
SLIDER_COLOR = (100, 100, 255)
BUTTON_COLOR = (200, 50, 50)
BUTTON_HOVER = (250, 80, 80)


class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, initial_val, text, is_int=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.text = text
        self.is_int = is_int
        self.dragging = False
        self.font = pygame.font.SysFont(None, 24)

    def draw(self, surface):
        display_val = int(self.value) if self.is_int else f"{self.value:.3f}"
        txt_surf = self.font.render(f"{self.text}: {display_val}", True, WHITE)
        surface.blit(txt_surf, (self.rect.x, self.rect.y - 20))

        pygame.draw.rect(surface, WHITE, self.rect)
        handle_x = self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width
        pygame.draw.circle(surface, SLIDER_COLOR, (int(handle_x), self.rect.centery), 8)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            if self.rect.collidepoint(mouse_pos) or math.dist(mouse_pos, (self.rect.x + (self.value - self.min_val) / (
                    self.max_val - self.min_val) * self.rect.width, self.rect.centery)) < 15:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x = max(self.rect.x, min(event.pos[0], self.rect.x + self.rect.width))
            ratio = (mouse_x - self.rect.x) / self.rect.width
            val = self.min_val + ratio * (self.max_val - self.min_val)
            self.value = int(val) if self.is_int else val


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = pygame.font.SysFont(None, 26)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = BUTTON_HOVER if self.rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        txt_surf = self.font.render(self.text, True, WHITE)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        surface.blit(txt_surf, txt_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False


class Boid:
    def __init__(self):
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)
        self.dx = random.uniform(-4, 4)
        self.dy = random.uniform(-4, 4)

    def update(self, boids, sep_weight, align_weight, coh_weight, visual_range):
        margin = 50
        turn_factor = 0.8
        if self.x < margin:
            self.dx += turn_factor
        elif self.x > width - margin:
            self.dx -= turn_factor

        if self.y < margin:
            self.dy += turn_factor
        elif self.y > height - margin:
            self.dy -= turn_factor

        self.fly_towards_center(boids, coh_weight, visual_range)
        self.avoid_others(boids, sep_weight)
        self.match_velocity(boids, align_weight, visual_range)

        speed = math.sqrt(self.dx ** 2 + self.dy ** 2)
        max_speed = 5
        min_speed = 2
        if speed > max_speed:
            self.dx = (self.dx / speed) * max_speed
            self.dy = (self.dy / speed) * max_speed
        elif speed < min_speed and speed > 0:
            self.dx = (self.dx / speed) * min_speed
            self.dy = (self.dy / speed) * min_speed

        self.x += self.dx
        self.y += self.dy

    def draw(self):
        angle = math.atan2(self.dy, self.dx)
        size = 8
        p1 = (self.x + math.cos(angle) * size, self.y + math.sin(angle) * size)
        p2 = (self.x + math.cos(angle + 2.5) * size, self.y + math.sin(angle + 2.5) * size)
        p3 = (self.x + math.cos(angle - 2.5) * size, self.y + math.sin(angle - 2.5) * size)
        pygame.draw.polygon(screen, BOID_COLOR, [p1, p2, p3])

    def fly_towards_center(self, boids, weight, visual_range):
        center_x, center_y, num_neighbors = 0, 0, 0
        for other in boids:
            if other != self and math.dist((self.x, self.y), (other.x, other.y)) < visual_range:
                center_x += other.x
                center_y += other.y
                num_neighbors += 1
        if num_neighbors > 0:
            self.dx += ((center_x / num_neighbors) - self.x) * weight
            self.dy += ((center_y / num_neighbors) - self.y) * weight

    def avoid_others(self, boids, weight):
        for other in boids:
            if other != self and math.dist((self.x, self.y), (other.x, other.y)) < 25:
                self.dx += (self.x - other.x) * weight
                self.dy += (self.y - other.y) * weight

    def match_velocity(self, boids, weight, visual_range):
        avg_dx, avg_dy, num_neighbors = 0, 0, 0
        for other in boids:
            if other != self and math.dist((self.x, self.y), (other.x, other.y)) < visual_range:
                avg_dx += other.dx
                avg_dy += other.dy
                num_neighbors += 1
        if num_neighbors > 0:
            self.dx += ((avg_dx / num_neighbors) - self.dx) * weight
            self.dy += ((avg_dy / num_neighbors) - self.dy) * weight


# --- UI Setup ---
slider_sep = Slider(20, 40, 150, 8, 0.0, 0.2, 0.05, "Separation")
slider_align = Slider(20, 90, 150, 8, 0.0, 0.2, 0.05, "Alignment")
slider_coh = Slider(20, 140, 150, 8, 0.0, 0.02, 0.005, "Cohesion")
slider_vision = Slider(20, 190, 150, 8, 30, 200, 75, "Visual Range", is_int=True)
slider_count = Slider(20, 240, 150, 8, 50, 150, 50, "Boid Count", is_int=True)

btn_birds = Button(20, 320, 60, 30, "Birds")
btn_fish = Button(90, 320, 60, 30, "Fish")
btn_bugs = Button(160, 320, 60, 30, "Bugs")

presets = [btn_birds, btn_fish, btn_bugs]

reset_button = Button(20, 270, 150, 40, "Reset Flock")
sliders = [slider_sep, slider_align, slider_coh, slider_vision, slider_count]

boids = [Boid() for _ in range(int(slider_count.value))]

# Main loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        for slider in sliders:
            slider.handle_event(event)

        if btn_birds.is_clicked(event):
            slider_sep.value = 0.05
            slider_align.value = 0.05
            slider_coh.value = 0.005
            slider_vision.value = 80

        elif btn_fish.is_clicked(event):
            slider_sep.value = 0.08
            slider_align.value = 0.15
            slider_coh.value = 0.015
            slider_vision.value = 45

        elif btn_bugs.is_clicked(event):
            slider_sep.value = 0.15
            slider_align.value = 0.002  # כמעט 0 יישור
            slider_coh.value = 0.02
            slider_vision.value = 25

        if reset_button.is_clicked(event):
            # Reset simulation: clear list and regenerate
            boids = [Boid() for _ in range(int(slider_count.value))]

    # Dynamically add/remove boids based on count slider
    target_count = int(slider_count.value)
    while len(boids) < target_count:
        boids.append(Boid())
    while len(boids) > target_count:
        boids.pop()

    screen.fill(DARK_BG)

    w_sep = slider_sep.value
    w_align = slider_align.value
    w_coh = slider_coh.value
    vision = slider_vision.value

    # Update and draw boids
    for boid in boids:
        boid.update(boids, w_sep, w_align, w_coh, vision)
        boid.draw()

    # Draw UI Panel background
    pygame.draw.rect(screen, UI_BG, (10, 10, 200, 310), border_radius=10)

    for slider in sliders:
        slider.draw(screen)

    for preset_btn in presets:
        preset_btn.draw(screen)

    reset_button.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
