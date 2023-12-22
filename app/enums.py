from enum import Enum

class Type(Enum):
    SPEECH = 'speech'
    GESTURE = 'gesture'
    OK = 'ok'

class CategoryPage(Enum):
    MAIN = 'main'
    SECONDARY = 'secondary'

class Direction(Enum):
    LEFT = 'left'
    RIGHT = 'right'
    UP = 'up'
    DOWN = 'down'