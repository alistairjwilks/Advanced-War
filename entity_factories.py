from components.ai import TutorialEnemy, UnitAI
from components.fighter import Fighter
from entity import Cursor, Actor

player = Cursor() # we're not using a player actor

infantry = Actor(
    char="i",
    color=(255, 0, 0),
    name="Infantry",
    ai_cls=UnitAI,
    fighter=Fighter(hp=100, defense=0, power=3, vision=4, code="inf"),
)

artillery = Actor(
    char="a",
    color=(255, 0, 0),  # red - TODO use team color
    name="Artillery",
    ai_cls=UnitAI,
    fighter=Fighter(
        hp=100, defense=0, power=3,
        vision=4, movement=4,
        atk_range=4, min_range=2,
        code="art"),
)
