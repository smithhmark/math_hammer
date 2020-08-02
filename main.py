
def wounds_per_phase(attacker, wargear, attackee, situation):
    return 0

def expected_wounds_generic(attack, defense):
    pass

_d6_outs = {
    6: 1,
    5: 2,
    4: 3,
    3: 4,
    2: 5,
    1: 6,
}

def outs_at_or_above(value):
    return _d6_outs[value]

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

def wound_probability(strength, toughness):
    return wound_outs(strength, toughness) / 6

def hit_probability(skill):
    return outs_at_or_above(skill) / 6

def save_probability(sv):
    return _d6_outs[sv]/6

def defeat_save_probability(sv):
    if sv:
        return 1.0 - save_probability(sv)
    else:
        return 1.0

def defeat_invuln_probability(invuln):
    if invuln:
        return 1.0 - save_probability(invuln)
    else:
        return 1.0

def defeat_armor_probability(sv, ap):
  outs = 6 - sv + 1 + ap
  if outs <= 0:
    return 0.0
  else: 
    return 1 - outs / 6

_expected_damage_table = {
    "d3": 2,
    "d6": 3.5,
}

def expected_damage(damage):
    if isinstance(damage, str):
        return _expected_damage_table[damage]
    else:
        return damage