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
        fighter=Fighter(hp=100, defense=0, power=3, vision=4, code="inf"),
    )
    return unit


class EntityFactory:
    pass
