from tkinter import Y
import pygame
import math 
pygame.init()
# first lines of code to create a snazzy display, pretty swag.
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Sim")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 128, 0)
PINK = (255, 192, 203)
PURPLE = (135,206,255)

FONT = pygame.font.SysFont("comicsans", 16)

#Creating the planets and it's values, just so we know what we doing.
class Planet:                          # this shit is for conversion into meters, trust me you'll need this later
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 200 / AU # 1 AU is equal to 100 pixels
    TIMESTEP = 3600 * 24 # 1 Day basically

# initializing several variables 
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0
    
    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

            pygame.draw.circle(win, self.color, (x,y), self.radius)

        if not self.sun:
            distance_text = FONT.render(f"{self.distance_to_sun/1000, 1}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))
#functions to define physic and the attraction of objects, adding distance between the objects and the force of attraction between them
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
# determining if the object is the sun, how close is the object to it
        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta)  * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
             if self == planet:
                continue
    
             fx, fy = self.attraction(planet)
             total_fx += fx
             total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))



# Placing some parameter so the game doesn't run at 1405935 shitframes per second and kills my cpu that's what clock = function is for lmao

def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet (0, 0, 30, YELLOW, 1.98892 * 10 **30) # Numbers for mass are in kilograms, as the IPS needs to
    sun.sun = True

    wenis = Planet(-1*Planet.AU, 0, 16, GREEN, 5.9742 * 10**24)
    wenis.y_vel = 29.783 * 1000

    barbie = Planet(-1.543*Planet.AU, 0, 20, PINK, 6.39 * 10**23)
    barbie.y_vel = 24.077 * 1000

    skye = Planet(0.387 * Planet.AU, 0, 12, PURPLE, 3.30 * 10**23)
    skye.y_vel = -47.4 * 1000

    joseph = Planet(0.723 * Planet.AU, 0, 17, WHITE, 4.8685 * 10**24)
    joseph.y_vel = -35.02 * 1000

    planets = [sun, wenis, barbie, skye, joseph]

    while run: 
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        for planet in planets: 
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()
    pygame.quit()
main()
