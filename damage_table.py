"""
Advance wars uses a damage table for the base damage of each unit-unit matchup
This will let units use a method to attack that gives their own code and the enemy unit's code,
i.e.
cursor.selection.attack(blocking_entity)
    damage = damage_table[self.code][enemy.code]
"""

"""
{"a-a": 45, "apc": 50, "art": 50, "bcp": 120, "bsh": 00, "bbt": 0, "bbm": 120, "bmr": 75, "car": 00, "crs": 0,"fgh": 65,
"inf": 105, "lnd": 00,"mdt": 10,"mec": 105,"mgt": 1,"mis": 55,"neo": 55,"pip": 25,"rcn": 60,"rck": 55,"sth": 75,"sub": 0,"tcp": 120,"tnk": 25},
"""

table = dict(
    a_a_p={"a_a": 45, "apc": 50, "art": 50, "bcp": 120, "bsh": 0, "bbt": 0, "bbm": 120, "bmr": 75, "car": 0, "crs": 0,
           "fgh": 65, "inf": 105, "lnd": 0, "mdt": 10, "mec": 105, "mga": 1, "mis": 55, "neo": 5, "pip": 25, "rcn": 60,
           "rkt": 55, "sth": 75, "sub": 0, "tcp": 120, "tnk": 25},
    apc={"a_a": 0, "apc": 0, "art": 0, "bcp": 0, "bsh": 0, "bbt": 0, "bbm": 0, "bmr": 0, "car": 0, "crs": 0, "fgh": 0,
         "inf": 0, "lnd": 0, "mdt": 0, "mec": 0, "mga": 0, "mis": 0, "neo": 0, "pip": 0, "rcn": 0, "rkt": 0, "sth": 0,
         "sub": 0, "tcp": 0, "tnk": 0},
    art_p={"a_a": 75, "apc": 70, "art": 75, "bcp": 0, "bsh": 40, "bbt": 55, "bbm": 0, "bmr": 0, "car": 45, "crs": 65,
           "fgh": 0, "inf": 90, "lnd": 55, "mdt": 45, "mec": 85, "mga": 15, "mis": 80, "neo": 40, "pip": 70, "rcn": 80,
           "rkt": 80, "sth": 0, "sub": 60, "tcp": 0, "tnk": 70},
    bcp_p={"a_a": 25, "apc": 60, "art": 65, "bcp": 0, "bsh": 25, "bbt": 25, "bbm": 0, "bmr": 0, "car": 25, "crs": 55,
           "fgh": 0, "inf": 0, "lnd": 25, "mdt": 25, "mec": 0, "mga": 10, "mis": 65, "neo": 20, "pip": 55, "rcn": 55,
           "rkt": 65, "sth": 0, "sub": 25, "tcp": 0, "tnk": 55},
    bcp={"a_a": 6, "apc": 20, "art": 25, "bcp": 65, "bsh": 0, "bbt": 0, "bbm": 0, "bmr": 0, "car": 0, "crs": 0,
           "fgh": 0, "inf": 75, "lnd": 0, "mdt": 1, "mec": 75, "mga": 1, "mis": 35, "neo": 1, "pip": 6, "rcn": 30,
           "rkt": 35, "sth": 0, "sub": 1, "tcp": 95, "tnk": 6},
    bsh_p={"a_a": 85, "apc": 80, "art": 80, "bcp": 0, "bsh": 50, "bbt": 95, "bbm": 0, "bmr": 0, "car": 60, "crs": 95,
           "fgh": 0, "inf": 95, "lnd": 95, "mdt": 55, "mec": 90, "mga": 25, "mis": 90, "neo": 50, "pip": 80, "rcn": 90,
           "rkt": 85, "sth": 0, "sub": 95, "tcp": 0, "tnk": 80},
    bbt={"a_a": 0, "apc": 0, "art": 0, "bcp": 0, "bsh": 0, "bbt": 0, "bbm": 0, "bmr": 0, "car": 0, "crs": 0, "fgh": 0,
         "inf": 0, "lnd": 0, "mdt": 0, "mec": 0, "mga": 0, "mis": 0, "neo": 0, "pip": 0, "rcn": 0, "rkt": 0, "sth": 0,
         "sub": 0, "tcp": 0, "tnk": 0},
    bbm={"a_a": 0, "apc": 0, "art": 0, "bcp": 0, "bsh": 0, "bbt": 0, "bbm": 0, "bmr": 0, "car": 0, "crs": 0, "fgh": 0,
         "inf": 0, "lnd": 0, "mdt": 0, "mec": 0, "mga": 0, "mis": 0, "neo": 0, "pip": 0, "rcn": 0, "rkt": 0, "sth": 0,
         "sub": 0, "tcp": 0, "tnk": 0},
    bmr_p={"a_a": 95, "apc": 105, "art": 105, "bcp": 0, "bsh": 75, "bbt": 95, "bbm": 0, "bmr": 0, "car": 75, "crs": 85,
           "fgh": 0, "inf": 110, "lnd": 95, "mdt": 95, "mec": 110, "mga": 35, "mis": 105, "neo": 90, "pip": 105,
           "rcn": 105, "rkt": 105, "sth": 0, "sub": 95, "tcp": 0, "tnk": 105},
    car_p={"a_a": 0, "apc": 0, "art": 0, "bcp": 115, "bsh": 0, "bbt": 0, "bbm": 120, "bmr": 100, "car": 0, "crs": 0,
           "fgh": 100, "inf": 0, "lnd": 0, "mdt": 0, "mec": 0, "mga": 0, "mis": 0, "neo": 0, "pip": 0, "rcn": 0,
           "rkt": 0,
           "sth": 100, "sub": 0, "tcp": 115, "tnk": 0},
    crs_p={"a_a": 0, "apc": 0, "art": 0, "bcp": 0, "bsh": 5, "bbt": 25, "bbm": 0, "bmr": 0, "car": 5, "crs": 25,
           "fgh": 0, "inf": 0, "lnd": 25, "mdt": 0, "mec": 0, "mga": 0, "mis": 0, "neo": 0, "pip": 0, "rcn": 0,
           "rkt": 0,
           "sth": 0, "sub": 90, "tcp": 0, "tnk": 0},
    crs={"a_a": 0, "apc": 0, "art": 0, "bcp": 115, "bsh": 0, "bbt": 0, "bbm": 120, "bmr": 65, "car": 0, "crs": 0,
           "fgh": 55, "inf": 0, "lnd": 0, "mdt": 0, "mec": 0, "mga": 0, "mis": 0, "neo": 0, "pip": 0, "rcn": 0,
           "rkt": 0,
           "sth": 100, "sub": 0, "tcp": 115, "tnk": 0},
    fgh_p={"a_a": 0, "apc": 0, "art": 0, "bcp": 100, "bsh": 0, "bbt": 0, "bbm": 120, "bmr": 100, "car": 0, "crs": 0,
           "fgh": 55, "inf": 0, "lnd": 0, "mdt": 0, "mec": 0, "mga": 0, "mis": 0, "neo": 0, "pip": 0, "rcn": 0,
           "rkt": 0,
           "sth": 85, "sub": 0, "tcp": 100, "tnk": 0},
    inf={"a_a": 5, "apc": 14, "art": 15, "bcp": 7, "bsh": 0, "bbt": 0, "bbm": 0, "bmr": 0, "car": 0, "crs": 0, "fgh": 0,
         "inf": 55, "lnd": 0, "mdt": 1, "mec": 45, "mga": 1, "mis": 26, "neo": 1, "pip": 5, "rcn": 12, "rkt": 25,
         "sth": 0, "sub": 0, "tcp": 30, "tnk": 5},
    lnd={"a_a": 0, "apc": 0, "art": 0, "bcp": 0, "bsh": 0, "bbt": 0, "bbm": 0, "bmr": 0, "car": 0, "crs": 0, "fgh": 0,
         "inf": 0, "lnd": 0, "mdt": 0, "mec": 0, "mga": 0, "mis": 0, "neo": 0, "pip": 0, "rcn": 0, "rkt": 0, "sth": 0,
         "sub": 0, "tcp": 0, "tnk": 0},
    mdt_p={"a_a": 105, "apc": 105, "art": 105, "bcp": 0, "bsh": 10, "bbt": 35, "bbm": 0, "bmr": 0, "car": 10,
           "crs": 45,
           "fgh": 0, "inf": 0, "lnd": 35, "mdt": 55, "mec": 0, "mga": 25, "mis": 105, "neo": 45, "pip": 85,
           "rcn": 105,
           "rkt": 105, "sth": 0, "sub": 10, "tcp": 0, "tnk": 85},
    mdt={"a_a": 17, "apc": 45, "art": 45, "bcp": 12, "bsh": 0, "bbt": 0, "bbm": 0, "bmr": 0, "car": 0, "crs": 0,
         "fgh": 0, "inf": 105, "lnd": 0, "mdt": 1, "mec": 95, "mga": 1, "mis": 35, "neo": 1, "pip": 1, "rcn": 45,
         "rkt": 55, "sth": 0, "sub": 0, "tcp": 45, "tnk": 8},
    mec_p={"a_a": 65, "apc": 75, "art": 70, "bcp": 0, "bsh": 0, "bbt": 0, "bbm": 0, "bmr": 0, "car": 0, "crs": 0,
           "fgh": 0, "inf": 0, "lnd": 0, "mdt": 15, "mec": 0, "mga": 5, "mis": 85, "neo": 15, "pip": 55, "rcn": 85,
           "rkt": 85, "sth": 0, "sub": 0, "tcp": 0, "tnk": 55},
    mec={"a_a": 6, "apc": 20, "art": 32, "bcp": 9, "bsh": 0, "bbt": 0, "bbm": 0, "bmr": 0, "car": 0, "crs": 0,
         "fgh": 0, "inf": 65, "lnd": 0, "mdt": 1, "mec": 55, "mga": 1, "mis": 35, "neo": 1, "pip": 1, "rcn": 18,
         "rkt": 35, "sth": 0, "sub": 0, "tcp": 35, "tnk": 6},
    mga_p={"a_a": 195, "apc": 195, "art": 195, "bcp": 0, "bsh": 45, "bbt": 105, "bbm": 0, "bmr": 0, "car": 45,
           "crs": 65,
           "fgh": 0, "inf": 0, "lnd": 75, "mdt": 125, "mec": 0, "mga": 65, "mis": 195, "neo": 115, "pip": 180,
           "rcn": 195, "rkt": 195, "sth": 0, "sub": 45, "tcp": 0, "tnk": 180},
    mga={"a_a": 17, "apc": 65, "art": 65, "bcp": 22, "bsh": 0, "bbt": 0, "bbm": 0, "bmr": 0, "car": 0, "crs": 0,
         "fgh": 0, "inf": 135, "lnd": 0, "mdt": 1, "mec": 125, "mga": 1, "mis": 55, "neo": 1, "pip": 10,
         "rcn": 65, "rkt": 75, "sth": 0, "sub": 0, "tcp": 55, "tnk": 10},

    mis_p={"a_a": 0, "apc": 0, "art": 0, "bcp": 120, "bsh": 0, "bbt": 0, "bbm": 120, "bmr": 100, "car": 0, "crs": 0,
           "fgh": 100, "inf": 0, "lnd": 0, "mdt": 0, "mec": 0, "mga": 0, "mis": 0, "neo": 0, "pip": 0, "rcn": 0,
           "rkt": 0,
           "sth": 100, "sub": 0, "tcp": 120, "tnk": 0},
    neo_p={"a_a": 115, "apc": 125, "art": 115, "bcp": 0, "bsh": 15, "bbt": 40, "bbm": 0, "bmr": 0, "car": 15,
           "crs": 50,
           "fgh": 0, "inf": 0, "lnd": 50, "mdt": 75, "mec": 0, "mga": 35, "mis": 125, "neo": 55, "pip": 105,
           "rcn": 125, "rkt": 125, "sth": 0, "sub": 15, "tcp": 0, "tnk": 105},
    neo={"a_a": 17, "apc": 65, "art": 65, "bcp": 22, "bsh": 0, "bbt": 0, "bbm": 0, "bmr": 0, "car": 0, "crs": 0,
         "fgh": 0, "inf": 125, "lnd": 0, "mdt": 1, "mec": 115, "mga": 1, "mis": 55, "neo": 1, "pip": 10,
         "rcn": 65, "rkt": 75, "sth": 0, "sub": 0, "tcp": 55, "tnk": 10},
    pip_p={"a_a": 85, "apc": 80, "art": 80, "bcp": 105, "bsh": 55, "bbt": 60, "bbm": 120, "bmr": 75, "car": 60,
           "crs": 85,
           "fgh": 65, "inf": 95, "lnd": 60, "mdt": 55, "mec": 90, "mga": 25, "mis": 90, "neo": 50, "pip": 80, "rcn": 90,
           "rkt": 85, "sth": 75, "sub": 85, "tcp": 105, "tnk": 80},
    rcn={"a_a": 4, "apc": 45, "art": 45, "bcp": 12, "bsh": 0, "bbt": 0, "bbm": 0, "bmr": 0, "car": 0, "crs": 0,
         "fgh": 0, "inf": 70, "lnd": 0, "mdt": 1, "mec": 65, "mga": 1, "mis": 28, "neo": 1, "pip": 6, "rcn": 35,
         "rkt": 55, "sth": 0, "sub": 0, "tcp": 35, "tnk": 6},
    rkt_p={"a_a": 85, "apc": 80, "art": 80, "bcp": 0, "bsh": 55, "bbt": 60, "bbm": 0, "bmr": 0, "car": 60, "crs": 85,
           "fgh": 0, "inf": 95, "lnd": 60, "mdt": 55, "mec": 90, "mga": 25, "mis": 90, "neo": 50, "pip": 80, "rcn": 90,
           "rkt": 85, "sth": 0, "sub": 85, "tcp": 0, "tnk": 80},
    sth_p={"a_a": 50, "apc": 85, "art": 75, "bcp": 85, "bsh": 45, "bbt": 65, "bbm": 120, "bmr": 70, "car": 45,
           "crs": 35,
           "fgh": 45, "inf": 90, "lnd": 65, "mdt": 70, "mec": 90, "mga": 15, "mis": 85, "neo": 60, "pip": 80, "rcn": 85,
           "rkt": 85, "sth": 55, "sub": 55, "tcp": 95, "tnk": 75},
    sub_p={"a_a": 0, "apc": 0, "art": 0, "bcp": 0, "bsh": 55, "bbt": 95, "bbm": 0, "bmr": 0, "car": 75, "crs": 25,
           "fgh": 0, "inf": 0, "lnd": 95, "mdt": 0, "mec": 0, "mga": 0, "mis": 0, "neo": 0, "pip": 0, "rcn": 0,
           "rkt": 0,
           "sth": 0, "sub": 55, "tcp": 0, "tnk": 0},
    tcp={"a_a": 0, "apc": 0, "art": 0, "bcp": 0, "bsh": 0, "bbt": 0, "bbm": 0, "bmr": 0, "car": 0, "crs": 0, "fgh": 0,
         "inf": 0, "lnd": 0, "mdt": 0, "mec": 0, "mga": 0, "mis": 0, "neo": 0, "pip": 0, "rcn": 0, "rkt": 0, "sth": 0,
         "sub": 0, "tcp": 0, "tnk": 0},
    tnk_p={"a_a": 65, "apc": 75, "art": 70, "bcp": 0, "bsh": 1, "bbt": 10, "bbm": 0, "bmr": 0, "car": 1, "crs": 5,
           "fgh": 0, "inf": 0, "lnd": 10, "mdt": 15, "mec": 0, "mga": 10, "mis": 85, "neo": 15, "pip": 55, "rcn": 85,
           "rkt": 85, "sth": 0, "sub": 1, "tcp": 0, "tnk": 55},
    tnk={"a_a": 6, "apc": 45, "art": 45, "bcp": 10, "bsh": 0, "bbt": 0, "bbm": 0, "bmr": 0, "car": 0, "crs": 0,
         "fgh": 0, "inf": 75, "lnd": 0, "mdt": 1, "mec": 70, "mga": 1, "mis": 30, "neo": 1, "pip": 6, "rcn": 40,
         "rkt": 55, "sth": 0, "sub": 0, "tcp": 40, "tnk": 6}

)
