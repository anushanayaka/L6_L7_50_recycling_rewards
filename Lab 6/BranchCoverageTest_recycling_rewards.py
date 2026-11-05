import pytest
from recycling_rewards import reward_points, collection_accepted, slot_status


# ---------------- reward_points ----------------
def test_below_minimum_weight():
    assert reward_points("paper", 3, False) == 0

def test_exactly_minimum_weight():
    # extra == 0 -> still the "extra <= 0" branch
    assert reward_points("plastic", 3, False) == 0

def test_unknown_material():
    with pytest.raises(ValueError):
        reward_points("glass", 10, False)

def test_known_material_does_not_raise():
    assert reward_points("plastic", 5, False) == 12

def test_negative_weight():
    with pytest.raises(ValueError):
        reward_points("paper", -1, False)

def test_zero_weight_is_valid():
    assert reward_points("paper", 0, False) == 0

def test_paper_with_bonus():
    # has_bonus True and material != metal -> minimum reduced to 4
    assert reward_points("paper", 8, True) == 24

def test_paper_without_bonus():
    # has_bonus False -> minimum stays 5
    assert reward_points("paper", 8, False) == 18

def test_metal_with_bonus_gets_no_discount():
    # has_bonus True but material == metal -> minimum stays 2
    assert reward_points("metal", 5, True) == 36

def test_metal_basic_rate():
    assert reward_points("metal", 5, False) == 36

def test_plastic_rate_not_metal():
    assert reward_points("plastic", 6, False) == 18

def test_extra_exactly_20_no_high_rate():
    # extra == 20 -> "extra > 20" is False
    assert reward_points("paper", 25, False) == 120

def test_paper_high_extra_rate():
    # extra > 20, not metal -> rate 6 + 4
    assert reward_points("paper", 30, False) == 250

def test_metal_high_extra_rate():
    # extra > 20 and metal -> rate 12 + 4 + 2
    assert reward_points("metal", 30, False) == 504


# ---------------- collection_accepted ----------------
def test_collection_accepted():
    assert collection_accepted(20, 2, False) is True

def test_hazardous_within_limit():
    assert collection_accepted(5, 1, True) is True

def test_hazardous_over_limit():
    assert collection_accepted(6, 1, True) is False

def test_too_heavy():
    assert collection_accepted(60, 1, False) is False

def test_exactly_max_weight_allowed():
    assert collection_accepted(50, 3, False) is True

def test_too_many_bags():
    assert collection_accepted(20, 4, False) is False


# ---------------- slot_status ----------------
def test_slot_open_morning():
    assert slot_status(20, True, False) == "open"

def test_slot_open_evening():
    assert slot_status(10, False, False) == "open"

def test_slot_morning_late():
    assert slot_status(5, True, False) == "late"

def test_slot_evening_holiday_open():
    assert slot_status(25, False, True) == "open"

def test_slot_late_evening_holiday():
    assert slot_status(15, False, True) == "late"

def test_slot_missed_morning():
    assert slot_status(4, True, False) == "missed"

def test_slot_missed_evening():
    assert slot_status(-10, False, False) == "missed"