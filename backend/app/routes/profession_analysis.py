# app/routes/profession_analysis.py

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, List, Any
from datetime import datetime
from app.data.professions import PROFESSIONS_BY_NUMBER, FRIEND_ENEMY_NEUTRAL, ANTI_PAIRS

router = APIRouter(prefix="/profession-analysis", tags=["Profession Analysis"])


class ProfessionRequest(BaseModel):
    date_of_birth: str
    lo_shu_numbers: List[int] = []  # Optional: include numbers from Lo Shu Grid


# ---------------------- Helper Functions ----------------------

def reduce_to_single_digit(num: int) -> int:
    """Reduce a number to a single digit (1–9)."""
    while num > 9:
        num = sum(map(int, str(num)))
    return num


def calculate_mulank(dob: str) -> int:
    """Calculate Mulank (Personality Number) = date of birth day root."""
    try:
        dob_parsed = datetime.strptime(dob, "%d-%m-%Y")
    except ValueError:
        try:
            dob_parsed = datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Use DD-MM-YYYY or YYYY-MM-DD.")
    return reduce_to_single_digit(dob_parsed.day)


def calculate_bhagyank(dob: str) -> int:
    """Calculate Bhagyank (Destiny Number) = root of full DOB sum."""
    digits = [int(c) for c in dob if c.isdigit()]
    return reduce_to_single_digit(sum(digits))


# ---------------------- Core Profession Logic ----------------------

def get_profession_suggestions(pn: int, dn: int, lo_shu_numbers: List[int]) -> Dict[str, Any]:
    """Generate profession recommendations following numerology conditions."""
    anti_pair = (pn, dn) in ANTI_PAIRS

    pn_data = FRIEND_ENEMY_NEUTRAL.get(pn, {})
    dn_data = FRIEND_ENEMY_NEUTRAL.get(dn, {})

    friends = sorted(list(set(pn_data.get("friends", []) + dn_data.get("friends", []))))
    enemies = sorted(list(set(pn_data.get("enemies", []) + dn_data.get("enemies", []))))
    neutrals = sorted(list(set(pn_data.get("neutral", []) + dn_data.get("neutral", []))))

    first_preference = []
    second_preference = []
    not_recommended = []

    # ---------- CASE 1: NOT ANTI PAIR ----------
    if not anti_pair:
        # First Preference → PN and DN professions
        first_nums = [pn, dn]

        # Second Preference → Lucky (friends) numbers that exist in Lo Shu Grid
        lucky_in_grid = [n for n in friends if n in lo_shu_numbers and n not in first_nums]
        second_nums = lucky_in_grid

        # Not Recommended → Enemy numbers
        not_nums = enemies

    # ---------- CASE 2: ANTI PAIR ----------
    else:
        # First Preference → Lucky (friends) numbers that exist in Lo Shu Grid
        first_nums = [n for n in friends if n in lo_shu_numbers]

        # Second Preference → Neutral numbers that exist in Lo Shu Grid
        second_nums = [n for n in neutrals if n in lo_shu_numbers and n not in first_nums]

        # Not Recommended → Enemy numbers + PN + DN
        not_nums = list(set(enemies + [pn, dn]))

    # ---------- BUILD PROFESSION LISTS ----------
    for n in first_nums:
        first_preference += PROFESSIONS_BY_NUMBER.get(n, [])

    for n in second_nums:
        second_preference += PROFESSIONS_BY_NUMBER.get(n, [])

    for n in not_nums:
        not_recommended += PROFESSIONS_BY_NUMBER.get(n, [])

    # ---------- REMOVE CONTRADICTIONS ----------
    # Step 1: Convert to sets for safe filtering
    first_set = set(first_preference)
    second_set = set(second_preference)

    # Step 2: Remove from second preference if it exists in first
    second_set -= first_set

    # Step 3: Remove from not recommended if it exists in first or second
    not_set = set(not_recommended) - first_set - second_set

    # ---------- FINAL SORTED LISTS ----------
    first_preference = sorted(first_set)
    second_preference = sorted(second_set)
    not_recommended = sorted(not_set)

    # ---------- FINAL RESULT ----------
    return {
        "pn": pn,
        "dn": dn,
        "anti_pair": anti_pair,
        "friends": friends,
        "enemies": enemies,
        "neutrals": neutrals,
        "recommended_professions": {
            "first_preference": first_preference,
            "second_preference": second_preference
        },
        "not_recommended_professions": not_recommended
    }


# ---------------------- API Route ----------------------

@router.post("/")
def analyze_profession(req: ProfessionRequest):
    pn = calculate_mulank(req.date_of_birth)
    dn = calculate_bhagyank(req.date_of_birth)
    result = get_profession_suggestions(pn, dn, req.lo_shu_numbers)
    return {"dob": req.date_of_birth, **result}