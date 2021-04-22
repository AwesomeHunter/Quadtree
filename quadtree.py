from pygame import Vector2

class Quadtree:
    
    def __init__(self, position, size, level):
        self.position = position
        self.size = size
        self.children = []
        self.level = level
        
    def child_size(self):
        return self.size // 2
    
    def children_positions(self):
        vectors = [Vector2(0, 0), Vector2(1, 0), Vector2(0, 1), Vector2(1, 1)]
        return [self.position + vector * self.child_size() for vector in vectors]

    def is_point_in_child(self, child, point):
        top_left = child.position
        bottom_right = child.position + Vector2(child.size, child.size)
        return (top_left.x <= point.x < bottom_right.x and top_left.y <= point.y < bottom_right.y)
    
    def create_children(self):
        self.children = [Quadtree(position, self.child_size(), self.level - 1) for position in self.children_positions()]
    
    def add_point(self, position):
        if self.level == 0:
            return
        if not self.children:
            self.create_children()
        for child in self.children:
            if self.is_point_in_child(child, position):
                child.add_point(position)
                
    def clear(self):
        self.children = []
