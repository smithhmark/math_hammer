
def wounds_per_phase(attacker, wargear, attackee, situation):
    return 0

def expected_wounds_generic(attack, defense):
    pass

_outs = {
    6: 1,
    5: 2,
    4: 3,
    3: 4,
    2: 5,
    1: 6,
}

def outs_at_or_above(value):
    return _outs[value]

def wound_outs(strength, toughness):
    ratio = strength / toughness
    if ratio >= 2.0:
        return 5
    elif ratio > 1.0:
        return 4
    elif ratio == 1.0:
        return 3
    elif ratio > 0.5:
        return 2
    else:
        return 1


def hit_probability(skill):
    return outs_at_or_above(skill) / 6
