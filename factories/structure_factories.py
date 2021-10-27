from components.ai import UnitAI, StructureAI
from components.team import Team

from entity import Structure

city = Structure(
    char='$',
    name="City",
    ai_cls=StructureAI
)


def team_city(team: Team):
    team_city = city
    team_city.team = team
    return team_city

