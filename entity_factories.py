from components.ai import UnitAI
from components.fighter import Fighter, IndirectFighter
from components.team import Team
from entity import Cursor, Actor

player = Cursor()  # we're not using a player actor


def anti_air(team: Team):
    return Actor(
        char='k',
        team=team,
        cost=8000,
        name="Anti-Air",
        ai_cls=UnitAI,
        fighter=Fighter(movement=6, ammo=9, fuel=60, vision=2, code="a_a", move_type="tread")
    )


def apc(team: Team):
    return Actor(
        char='p',
        team=team,
        cost=5000,
        name="APC",
        ai_cls=UnitAI,
        fighter=Fighter(movement=6, ammo=0, fuel=70, vision=1, code="apc", move_type="tread")
    )


def artillery(team: Team):
    return Actor(
        char='r',
        team=team,
        name="Artillery",
        ai_cls=UnitAI,
        cost=6000,
        fighter=IndirectFighter(movement=5, ammo=9, fuel=50, vision=1, min_range=2, atk_range=3, code="art", move_type="tread")
    )


def battle_copter(team: Team):
    return Actor(
        char='b',
        team=team,
        name="B-Copter",
        ai_cls=UnitAI,
        cost=9000,
        fighter=Fighter(movement=6, ammo=6, fuel=99, fuel_cost=2, vision=3, code="bcp", move_type="air")
    )


def battleship(team: Team):
    return Actor(
        char='B',
        team=team,
        cost=28000,
        name="Battleship",
        ai_cls=UnitAI,
        fighter=IndirectFighter(movement=5, ammo=9, fuel=99, fuel_cost=1, vision=2, min_range=2, atk_range=6, code="bsh",
                        move_type="sea")
    )


def black_boat(team: Team):
    return Actor(
        char='Y',
        team=team,
        cost=7500,
        name="Black Boat",
        ai_cls=UnitAI,
        fighter=Fighter(movement=7, ammo=0, fuel=60, fuel_cost=1, vision=1, code="bbt", move_type="lander")  # lander
    )


def black_bomb(team: Team):
    return Actor(
        char='Z',
        team=team,
        cost=25000,
        name="Black Boat",
        ai_cls=UnitAI,
        fighter=Fighter(movement=9, ammo=0, fuel=45, fuel_cost=5, vision=1, code="bbm", move_type="air")
    )


def bomber(team: Team):
    return Actor(
        char='M',
        team=team,
        cost=22000,
        name="Black Boat",
        ai_cls=UnitAI,
        fighter=Fighter(movement=7, ammo=9, fuel=99, fuel_cost=5, vision=2, code="bmr", move_type="air")
    )


def carrier(team: Team):
    return Actor(
        char='C',
        team=team,
        cost=30000,
        name="Carrier",
        ai_cls=UnitAI,
        fighter=Fighter(movement=5, ammo=9, fuel=99, fuel_cost=1, vision=4, min_range=3, atk_range=8, code="car",
                        move_type="sea")
    )


def cruiser(team: Team):
    return Actor(
        char='c',
        team=team,
        cost=18000,
        name="Carrier",
        ai_cls=UnitAI,
        fighter=Fighter(movement=6, ammo=9, fuel=99, fuel_cost=1, vision=3, code="crs", move_type="sea")
    )


def fighter(team: Team):
    return Actor(
        char='F',
        team=team,
        cost=20000,
        name="Fighter",
        ai_cls=UnitAI,
        fighter=Fighter(movement=9, ammo=9, fuel=99, fuel_cost=5, vision=2, code="fgh", move_type="air")
    )


def infantry(team: Team):
    return Actor(
        char='i',
        team=team,
        name="Infantry",
        ai_cls=UnitAI,
        cost=1000,
        fighter=Fighter(movement=3, vision=2, code="inf", move_type="inf"),
    )


def lander(team: Team):
    return Actor(
        char='L',
        team=team,
        name="Lander",
        ai_cls=UnitAI,
        cost=12000,
        fighter=Fighter(movement=6, vision=1, fuel=99, fuel_cost=1, code="lnd", move_type="lander"),
    )


def med_tank(team: Team):
    return Actor(
        char='T',
        team=team,
        name="Md. Tank",
        ai_cls=UnitAI,
        cost=16000,
        fighter=Fighter(movement=5, amoo=8, vision=1, fuel=50, code="mdt", move_type="tread"),
    )


def mech(team: Team):
    return Actor(
        char='m',
        team=team,
        name="Mech",
        ai_cls=UnitAI,
        cost=3000,
        fighter=Fighter(movement=2, vision=2, code="mec", move_type="mec", ammo=3, fuel=70),
    )


def megatank(team: Team):
    return Actor(
        char='M',
        team=team,
        name="Megatank",
        ai_cls=UnitAI,
        cost=28000,
        fighter=Fighter(movement=4, vision=1, code="mga", move_type="tread", ammo=3, fuel=50),
    )


def missile(team: Team):
    return Actor(
        char='K',
        team=team,
        name="Missile",
        ai_cls=UnitAI,
        cost=12000,
        fighter=IndirectFighter(movement=4, vision=5, code="mis", move_type="tire", ammo=6, fuel=50, min_range=3, atk_range=5),
    )


def neotank(team: Team):
    return Actor(
        char='N',
        team=team,
        name="Neotank",
        ai_cls=UnitAI,
        cost=22000,
        fighter=Fighter(movement=6, vision=1, code="neo", move_type="tread", ammo=9, fuel=99),
    )


def piperunner(team: Team):
    return Actor(
        char='X',
        team=team,
        name="Piperunner",
        ai_cls=UnitAI,
        cost=20000,
        fighter=IndirectFighter(movement=9, vision=4, code="pip", move_type="pipe", ammo=9, fuel=99, min_range=2, atk_range=5),
    )


def recon(team: Team):
    return Actor(
        char='v',
        team=team,
        name="Recon",
        ai_cls=UnitAI,
        cost=4000,
        fighter=Fighter(movement=8, vision=5, code="rcn", move_type="tire", fuel=80),
    )


def rocket(team: Team):
    return Actor(
        char='R',
        team=team,
        name="Rocket",
        ai_cls=UnitAI,
        cost=15000,
        fighter=IndirectFighter(movement=5, vision=1, code="rkt", move_type="tire", ammo=6, fuel=50, min_range=3, atk_range=5),
    )


def stealth(team: Team):
    return Actor(
        char='S',
        team=team,
        name="Stealth Jet",
        ai_cls=UnitAI,
        cost=24000,
        fighter=Fighter(movement=6, vision=4, code="sth", move_type="air", ammo=6, fuel=60, fuel_cost=5, ),
    )


def sub(team: Team):
    return Actor(
        char='s',
        team=team,
        name="Submarine",
        ai_cls=UnitAI,
        cost=20000,
        fighter=Fighter(movement=5, vision=5, code="sub", move_type="sea", ammo=6, fuel=60, fuel_cost=1),
    )


def t_copter(team: Team):
    return Actor(
        char='x',
        team=team,
        name="T-Copter",
        ai_cls=UnitAI,
        cost=5000,
        fighter=Fighter(movement=6, vision=2, code="tcp", move_type="air", fuel=99, fuel_cost=2),
    )


def tank(team: Team):
    unit = Actor(
        char='t',
        team=team,
        name="Tank",
        ai_cls=UnitAI,
        cost=7000,
        fighter=Fighter(hp=100, movement=6, vision=3, code="tnk", move_type="tread", primary_wpn=True, ammo=9),
    )
    return unit
