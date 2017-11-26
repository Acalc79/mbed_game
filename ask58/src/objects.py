from enum import Enum, unique, auto
import random as rand

EPSILON = 0.001

@unique
class GameObjT(Enum):
    PLAYER = auto()
    ENEMY = auto()
    BULLET = auto()
    COLLECTIBLE = auto()
    SHIELD = auto()
    BACKGROUND = auto()
        
class GameObject:
    def __init__(self, obj_type, x, y, w, h):
        self._t = obj_type
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._vx = 0
        self._vy = 0
##        self.debug = False

    def get_edges(self):
        x, y = self.pos()
        w, h = self.size()
        return x, x+w, y, y+h

    def bounce(self):
        vx, vy = self.speed()
        self.speed((-vx, -vy))

    def bounce_x(self):
        vx, vy = self.speed()
        self.speed((-vx, vy))

    def bounce_y(self):
        vx, vy = self.speed()
        self.speed((vx, -vy))
    
    def collides_with(self, other):
        if not self.solid() or not other.solid():
            return False
        else:
            right0, left0, top0, bottom0 = self.get_edges()
            right1, left1, top1, bottom1 = other.get_edges()

            overlap_x = (right0 <= right1 and right1 <= left0) \
                     or (right0 <=  left1 and  left1 <= left0) \
                     or (right1 <=  left0 and  left0 <= left1) \
                     or (right1 <= right0 and right0 <= left1)
            overlap_y = (top0 <=    top1 and    top1 <= bottom0) \
                     or (top0 <= bottom1 and bottom1 <= bottom0) \
                     or (top1 <=    top0 and    top0 <= bottom1) \
                     or (top1 <= bottom0 and bottom0 <= bottom1)
            
            return overlap_x and overlap_y

    def do_collision_check(self, other):
        if self.solid() and other.solid() and self.collides_with(other):
            self.handle_collision_with(other)
            other.handle_collision_with(self)
            
    def handle_collision_with(self, other):
        raise NotImplementedError("Handle_collision_with of GameObject: "+self)
    
    def update(self, time):
        vx, vy = self.speed()
        self.move_by(time * vx, time * vy)

    def move_by(self, *d):
        dx, dy = d
        x, y = self.pos()
        self.pos((x+dx, y+dy))

    def type(self):
        return self._t

    def x(self):
        return self._x

    def y(self):
        return self._y

    def w(self):
        return self._w

    def h(self):
        return self._h

    def size(self, s=None):
        if s is not None:
            self._w, self._h = s
        else:
            return self.w(), self.h()

    def pos(self, pos=None):
        if pos is not None:
            self._x, self._y = pos
        else:
            return self.x(), self.y()

    def speed(self, v=None):
        if v is not None:
            self._vx, self._vy = v
        else:
            return self._vx, self._vy

    def solid(self):
        return self._solid

class PhantomObject(GameObject):
    def __init__(self, obj_type, x, y, w, h):
        super().__init__(obj_type, x, y, w, h)
        self._solid = False
            
class SolidObject(GameObject):
    def __init__(self, obj_type, x, y, w, h):
        super().__init__(obj_type, x, y, w, h)
        self._solid = True

class Player(SolidObject):
    def __init__(self, x, y, w, h, game_lost_handler):
        super().__init__(GameObjT.PLAYER, x, y, w, h) 
        self.game_lost_handler = game_lost_handler
        
    def handle_collision_with(self, other):
        if other.type() is GameObjT.ENEMY:
            self.game_lost_handler()
        elif other.type() is GameObjT.BULLET:
            self.game_lost_handler()

class Enemy(SolidObject):
    def __init__(self, vx, vy, delete_enemy, width, w, h):
        x = rand.random()*(width - w)
        y = 0
        super().__init__(GameObjT.ENEMY, x, y, w, h)
        self.speed((vx, vy))
        self.destruct = delete_enemy

    def handle_collision_with(self, other):
        if other.type() is GameObjT.BULLET:
            self.destruct()
            
class Bullet(SolidObject):
    def __init__(self, vx, vy, delete_bullet, x, y, w, h):
        super().__init__(GameObjT.BULLET, x, y, w, h)
        self.speed((vx, vy))
        self.destruct = delete_bullet

    def handle_collision_with(self, other):
        if other.type() in [GameObjT.PLAYER, GameObjT.SHIELD]:
            self.destruct()
            
class Collectible(SolidObject):
    def __init__(self, collect_event_handler, x, y, w, h):
        super().__init__(GameObjT.COLLECTIBLE, x, y, w, h)
        self.collect_event_handler = collect_event_handler
        
    def handle_collision_with(self, other):
        if other.type() is GameObjT.PLAYER:
            self.collect_event_handler()

class Shield(SolidObject):
    def __init__(self, x, y, w, h, hp, shield_end_handler):
        super().__init__(GameObjT.SHIELD, x, y, w, h)
        self.shield_end_handler
        self._hp = hp

    def handle_collision_with(self, other):
        if other.type() is GameObjT.BULLET:
            self.hp(self.hp() - 1)
            if self.hp() <= 0:
                self.shield_end_handler()

    def hp(self, hp=None):
        if hp is not None:
            self._hp = hp
        else:
            return self._hp

class Background(PhantomObject):
    def __init__(self, vx, vy, x, y, w, h):
        super().__init__(GameObjT.BACKGROUND, x, y, w, h)
        self.speed((vx, vy))

    def move_by(self, *d):
        dx, dy = d
        x, y = self.pos()
        self.pos(((x+dx) % self.w(), (y+dy) % self.h()))
