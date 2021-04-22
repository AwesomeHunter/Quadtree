import pygame as pg
from pygame import Vector2

from random import randrange
from point import Point
from quadtree import Quadtree


class App:
    
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    FPS = 60
    
    def __init__(self, board_size, min_size):
        pg.init()
        pg.display.set_caption("Squares")
        self.size = 2 ** board_size
        self.screen = pg.display.set_mode((self.size, self.size))
        self.screen.fill(self.WHITE)
        self.running = True
        self.points = []
        self.min_quad_size = 2 ** (board_size - min_size)
        self.quadtree = Quadtree(Vector2(0, 0), self.size, min_size)
        
    def add_point(self, position, velocity, radius):
        self.points.append(Point(position, velocity, radius))
        
    def correct_point_params(self, point):
        for i in [0, 1]:
            if point.position[i] < point.radius:
                point.position[i] = point.radius
                point.velocity[i] *= -0.90
            elif point.position[i] + point.radius > self.size:
                point.position[i] = self.size - point.radius
                point.velocity[i] *= -0.90
        
    def spawn_particles(self, amount, radius):
        for i in range(amount):
            position = Vector2(pg.mouse.get_pos())
            velocity = Vector2(randrange(-20, 20), randrange(-20, 5))
            self.add_point(position, velocity, radius)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.spawn_particles(50, self.min_quad_size)

    def draw_border(self, pos, size):
        pg.draw.line(self.screen, self.BLACK, pos, pos + Vector2(0, size))
        pg.draw.line(self.screen, self.BLACK, pos, pos + Vector2(size, 0))
        pg.draw.line(self.screen, self.BLACK, pos + Vector2(size, 0), pos + Vector2(size, size))
        pg.draw.line(self.screen, self.BLACK, pos + Vector2(0, size), pos + Vector2(size, size))

    def draw_tree(self, quadtree):
        if not quadtree.children:
            self.draw_border(quadtree.position, quadtree.size)
            return
        for child in quadtree.children:
            self.draw_tree(child)
            
    def get_point_corners(self, point):
        corner_vectors = [Vector2(-1, -1), Vector2(-1, 1), Vector2(1, -1), Vector2(1, 1)]
        return [point.position + vector * point.radius for vector in corner_vectors]
            
    def update_tree(self, quadtree):
        quadtree.clear()
        for point in self.points:
            for corner in self.get_point_corners(point):
                quadtree.add_point(corner)
    
    def get_point_color(self, point):
        r_val = 255 * min((1.0 - point.life_left()), 0.5)
        g_val = 255 * point.life_left()
        b_val = 0
        return r_val, g_val, b_val
    
    def draw_points(self):
        for point in self.points:
            pg.draw.circle(self.screen, self.get_point_color(point), point.position, point.radius)
    
    def update_points(self, dtime):
        updated_points = []
        for point in self.points:
            if point.life_time != 0:
                point.update(dtime)
                self.correct_point_params(point)
                updated_points.append(point)
        self.points = updated_points

    def run(self):
        pg.display.update()
        clock = pg.time.Clock()
        while self.running:
            dt = clock.tick(60) * 0.001 * self.FPS
            self.handle_events()
            self.update_points(dt)
            self.update_tree(self.quadtree)
            self.screen.fill(self.WHITE)
            self.draw_points()
            self.draw_tree(self.quadtree)
            pg.display.update()
        pg.quit()
