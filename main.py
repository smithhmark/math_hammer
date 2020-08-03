
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
    return 1.0
  else: 
    return 1.0 - outs / 6

_expected_damage_table = {
    "d3": 2.0,
    "d6": 3.5,
}

def average_damage(damage):
    if isinstance(damage, str):
        return _expected_damage_table[damage]
    else:
        return damage

def apply_wargear_strength(unit_strength, weapon_strength):
    if isinstance(weapon_strength, str):
        if weapon_strength[0] == '+':
            st = int(weapon_strength[1:])
            return unit_strength + st
        else:
            return int(weapon_strength)
    else:
        return unit_strength + weapon_strength

def is_melee(wargear):
    if "melee" in wargear.get("type", ''):
        return True
    else:
        return False

def get_wargear_attacks(wargear):
    last_word = wargear['type'].split()[-1]
    try:
        attacks = int(last_word)
        return attacks
    except TypeError:
        return 0

def get_attack_stats_base(attacker, wargear):
    if is_melee(wargear):
        skill = attacker.get('ws',0)
        attacks = attacker.get('a', 0)
    else:
        skill = attacker.get('bs',0)
        attacks = get_wargear_attacks(wargear)
    stats = {
        "s": apply_wargear_strength(attacker.get('s',0), wargear.get('s', 0)),
        "damage": int(wargear.get("d", 0)),
        "attacks": attacks,
        "skill": skill,
        "ap": int(wargear.get("ap", 0))
    }
    return stats

def get_defender_stats_base(defender):
    return {
        "t": defender['t'],
        'invuln': defender['invuln'],
        "w": defender['w'],
        "fnp": defender.get('fnp',0),
        'sv': defender['sv'],
    }

def expected_damage(attacking_stats, defending_stats):
    hit_prob = hit_probability(attacking_stats['skill'])
    print(f"hit_prob:{hit_prob}")
    print(attacking_stats)
    wound_prob = wound_probability(attacking_stats['s'], defending_stats['t'])
    print(f"wound_prob:{wound_prob}")
    beats_save = defeat_armor_probability(defending_stats['sv'], attacking_stats['ap'])
    beats_invuln = defeat_invuln_probability(defending_stats['invuln'])
    print(f"beats_save:{beats_save}")
    print(f"beats_invuln:{beats_invuln}")
    damage = average_damage(attacking_stats['damage'])
    print(f"damage:{damage}")
    attacks = attacking_stats['attacks']
    print(f"attacks:{attacks}")

    return hit_prob * wound_prob * min(beats_save, beats_invuln) * damage * attacks