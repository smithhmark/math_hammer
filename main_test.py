import pytest

import main

def assert_approx_eq(v1, v2, ep=0.00001):
    if (v2 < v1 + ep) and (v2 > v1 - ep):
        assert True
    else:
        tmp_str = f"{v1} !~= {v2}"
        assert False, tmp_str #f"{v1} !~= {v2}"

@pytest.fixture
def necron_immortal_stats_dict():
    return {
        'move': 6,
        'bs': 3,
        'ws': 3,
        's': 4,
        't': 4,
        'w': 1,
        'a': 1,
        'ld': 10,
        'sv': 3,
        'invuln': 0,
    }

@pytest.fixture
def skitarii_ranger_stats_dict():
    return {
        'm': 6,
        'bs': 4,
        'ws': 3,
        's': 3,
        't': 3,
        'w': 1,
        'a': 1,
        'ld': 6,
        'sv': 4,
        'invuln': 6,
    }

@pytest.fixture
def genestealer_stats_dict():
    return {
        'm': 8,
        'bs': 3,
        'ws': 4,
        's': 4,
        't': 4,
        'w': 1,
        'a': 3,
        'ld': 9,
        'sv': 5,
        'invuln': 5,
    }

@pytest.fixture
def galvanic_rifle_wargear_dict():
    return {
        'range': '30',
        'type': 'Rapid Fire 1',
        's': '4',
        'ap': '0',
        'd': '1',
        "rules": ["Each time you make a wound roll of 6+ for this weapon, that hit is resolved with an AP of -1."]
    }

@pytest.fixture
def gauss_blaster_wargear_dict():
    return {
        'range': '24',
        'type': 'Rapid Fire 1',
        's': '5',
        'ap': '-2',
        'd': '1',
        "rules": [],
    }
    
@pytest.fixture
def skitarii_attacking_with_galvanic_rifle():
    return {
        "skill": 4,
        "strength": 4,
        "ap": 0,
        "damage": 1,
    }

def test_hit_probability_base():
    skill = 6
    assert main.hit_probability(skill) == 1/6

    skill = 2
    assert main.hit_probability(skill) == 5/6

def test_wound_outs():
    strength = 3
    toughness = 3
    assert main.wound_outs(strength, toughness) == 3
    toughness = 4
    assert main.wound_outs(strength, toughness) == 2
    toughness = 5
    assert main.wound_outs(strength, toughness) == 2
    toughness = 6
    assert main.wound_outs(strength, toughness) == 1
    toughness = 2
    assert main.wound_outs(strength, toughness) == 4
    toughness = 1
    assert main.wound_outs(strength, toughness) == 5

    assert main.wound_outs(5, 3) == 4
    
def test_defeats_save_base():
    sv = 2
    assert_approx_eq(main.defeat_save_probability(sv), float(1/6))
    sv = 6
    assert_approx_eq(main.defeat_save_probability(sv), float(5/6))

def test_defeats_invuln():
    sv = 2
    assert_approx_eq(main.defeat_invuln_probability(sv), float(1/6))
    sv = 6
    assert_approx_eq(main.defeat_invuln_probability(sv), float(5/6))

def test_defeat_armor():
    sv = 4
    ap = 0
    assert_approx_eq(main.defeat_armor_probability(sv, ap), float(3/6))
    sv = 4
    ap = -1
    assert_approx_eq(main.defeat_armor_probability(sv, ap), float(4/6))
    sv = 4
    ap = -2
    assert_approx_eq(main.defeat_armor_probability(sv, ap), float(5/6))
    sv = 6
    ap = 0
    assert_approx_eq(main.defeat_armor_probability(sv, ap), float(5/6))
    sv = 6
    ap = -1
    assert_approx_eq(main.defeat_armor_probability(sv, ap), 1.0)
    sv = 6
    ap = -2
    assert_approx_eq(main.defeat_armor_probability(sv, ap), 1.0)

def test_average_damage():
    damage = 1
    assert main.average_damage(damage) == 1
    damage = 3
    assert main.average_damage(damage) == 3
    damage = "d3"
    assert main.average_damage(damage) == 2
    damage = "d6"
    assert main.average_damage(damage) == 3.5


def test_attack_stats(necron_immortal_stats_dict, gauss_blaster_wargear_dict):
    attacker = necron_immortal_stats_dict
    using_wargear = gauss_blaster_wargear_dict
    final_stats = main.get_attack_stats_base(attacker, using_wargear)
    assert "attacks" in final_stats
    assert "damage" in final_stats
    assert "skill" in final_stats
    assert "ap" in final_stats

    assert final_stats['attacks'] == 1
    assert final_stats['skill'] == 3
    assert final_stats['ap'] == -2
    assert final_stats['damage'] == 1

def test_expected_damage(necron_immortal_stats_dict, gauss_blaster_wargear_dict, skitarii_ranger_stats_dict):
    attack_stats = main.get_attack_stats_base(necron_immortal_stats_dict, gauss_blaster_wargear_dict)
    defense_stats = main.get_defender_stats_base(skitarii_ranger_stats_dict)
    expt_damage = main.expected_damage(attack_stats, defense_stats)
    assert_approx_eq(expt_damage, 0.37, 0.001)

def test_apply_wargear_strength(necron_immortal_stats_dict, gauss_blaster_wargear_dict):
    unit_s = necron_immortal_stats_dict['s']
    wargear_s = gauss_blaster_wargear_dict['s']
    got = main.apply_wargear_strength(unit_s, wargear_s)

    assert got == 5