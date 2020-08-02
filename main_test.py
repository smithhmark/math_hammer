import pytest

import main

@pytest.fixture
def necron_immortal_stats_dict():
    return {
        'move': 6,
        'bs': 3,
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
    }

@pytest.fixture
def galvanic_rifle_wargear_dict():
    return {
        'range': '30',
        'type': 'Rapid Fire 1',
        's': '4',
        'ap': '0',
        'd': '1',
        "rules": "Each time you make a wound roll of 6+ for this weapon, that hit is resolved with an AP of -1."
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
    
