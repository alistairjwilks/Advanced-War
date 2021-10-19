from components.ai import TutorialEnemy, UnitAI
from components.fighter import Fighter
from components.team import Team
from entity import Cursor, Actor

player = Cursor() # we're not using a player actor


def infantry(team: Team):
    unit = Actor(
        char='i',
        team=team,
        name="Infantry",
        ai_cls=UnitAI,
        fighter=Fighter(hp=100, move=3, vision=4, code="inf"),
    )
    return unit


def mech(team: Team):
    unit = Actor(
        char='m',
        team=team,
        name="Mech",
        ai_cls=UnitAI,
        fighter=Fighter(hp=100, movement=2, vision=4, code="mec", primary_wpn=True, ammo=1),
    )
    return unit

def tank(team: Team):
    unit = Actor(
        char='t',
        team=team,
        name="Tank",
        ai_cls=UnitAI,
        fighter=Fighter(hp=100, movement=5, vision=4, code="tnk", primary_wpn=True, ammo=1),
    )
    return unit

class EntityFactory:
    pass
