from components.ai import UnitAI, StructureAI
from components.team import Team

from entity import Structure

city = Structure(
    char='$',
    name="City",
    ai_cls=StructureAI
)


def team_city(team: Team):
    this_city = city
    this_city.team = team
    return this_city

