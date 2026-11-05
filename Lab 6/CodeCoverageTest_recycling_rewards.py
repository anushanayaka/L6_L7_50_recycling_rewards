import pytest
from recycling_rewards import reward_points, collection_accepted, slot_status


# ---------------- reward_points ----------------
def test_below_minimum_weight():
    assert reward_points("paper", 3, False) == 0

def test_unknown_material():
    with pytest.raises(ValueError):
        reward_points("glass", 10, False)

def test_negative_weight():
    with pytest.raises(ValueError):
        reward_points("paper", -1, False)

def test_paper_with_bonus():
    # minimum 5 - 1 = 4, extra = 4, rate 6
    assert reward_points("paper", 8, True) == 24

def test_metal_basic_rate():
    # minimum 2, extra = 3, rate 12
    assert reward_points("metal", 5, False) == 36

def test_paper_high_extra_rate():
    # extra = 25 (> 20), rate 6 + 4 = 10
    assert reward_points("paper", 30, False) == 250

def test_metal_high_extra_rate():
    # extra = 28 (> 20), rate 12 + 4 + 2 = 18
    assert reward_points("metal", 30, False) == 504


# ---------------- collection_accepted ----------------
def test_collection_accepted():
    assert collection_accepted(20, 2, False) is True

def test_hazardous_within_limit():
    assert collection_accepted(5, 1, True) is True

def test_too_heavy():
    assert collection_accepted(60, 1, False) is False

def test_too_many_bags():
    assert collection_accepted(20, 4, False) is False


# ---------------- slot_status ----------------
def test_slot_open_morning():
    assert slot_status(25, True, False) == "open"

def test_slot_late_evening_holiday():
    # cutoff = 10 + 15 = 25, late if >= 10
    assert slot_status(15, False, True) == "late"

def test_slot_missed():
    assert slot_status(-10, False, False) == "missed"