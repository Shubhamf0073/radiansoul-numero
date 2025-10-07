from datetime import datetime
from .mapping import CHALDEAN_MAP

def reduce_number(num: int) -> int:
    """Reduce a number to a single digit (1-8)."""
    while num > 8:
        num = sum(int(d) for d in str(num))
        if num == 9:
            num = 8
    return num

def name_to_number(name: str) -> int:
    """Convert a name to its Chaldean numerology number."""
    total = sum(CHALDEAN_MAP.get(ch.upper(), 0) for ch in name if ch.isalpha())
    return reduce_number(total)

def life_path_number(dob: str) -> int:
    """Calculate the life path number from date of birth (DD-MM-YYYY)."""
    digits = [int(d) for d in dob if d.isdigit()]
    total = sum(digits)
    return reduce_number(total)

def destiny_number(name: str) -> int:
    """Destiny number is derived from full name vibration."""
    return name_to_number(name)

def soul_urge_number(name: str) -> int:
    """Soul urge number is from vowels in name."""
    vowels = "AEIOU"
    total = sum(CHALDEAN_MAP.get(ch, 0) for ch in name.upper() if ch in vowels)
    return reduce_number(total)

def personality_number(name: str) -> int:
    """Personality comes from consonants in name."""
    vowels = "AEIOU"
    total = sum(CHALDEAN_MAP.get(ch, 0) for ch in name.upper() if ch.isalpha() and ch not in vowels)
    return reduce_number(total)