from components.ai import TutorialEnemy
from components.fighter import Fighter
from entity import Cursor, Actor

player = Cursor() # we're not using a player actor

orc = Actor(
    char="o",
    color=(63, 127, 63),
    name="Orc",
    ai_cls=TutorialEnemy,
    fighter=Fighter(hp=10, defense=0, power=3, vision=4),
)

infantry = Actor(
    char="i",
    color=(255, 0, 0),
    name="Infantry",
    ai_cls=TutorialEnemy,
    fighter=Fighter(hp=100, defense=0, power=3, vision=4),
)

troll = Actor(
    char="T",
    color=(0, 127, 0),
    name="Troll",
    ai_cls=TutorialEnemy,
    fighter=Fighter(hp=20, defense=1, power=4, vision=2)
)