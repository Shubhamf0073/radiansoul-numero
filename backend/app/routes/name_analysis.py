from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

CHALDEAN_TABLE = {
    "A": 1, "I": 1, "J": 1, "Q": 1, "Y": 1,
    "B": 2, "K": 2, "R": 2,
    "C": 3, "G": 3, "L": 3, "S": 3,
    "D": 4, "M": 4, "T": 4,
    "E": 5, "H": 5, "N": 5, "X": 5,
    "U": 6, "V": 6, "W": 6,
    "O": 7, "Z": 7,
    "F": 8, "P": 8
}

# Single Number Interpretations
SINGLE_MEANINGS = {
    1: "Leadership, individuality, ambition, and creativity.",
    2: "Sensitivity, diplomacy, cooperation, and intuition.",
    3: "Expression, joy, and artistic talent.",
    4: "Practicality, stability, and discipline.",
    5: "Freedom, adaptability, and change.",
    6: "Responsibility, family, love, and nurturing.",
    7: "Wisdom, introspection, and spirituality.",
    8: "Power, authority, and material success.",
    9: "Compassion, completion, and humanitarianism."
}

# Common Compound Numbers
COMPOUND_MEANINGS = {
    10: "The Wheel of Fortune - rise and fall through destiny.",
    11: "Spiritual insight, illumination, and inspiration.",
    12: "Sacrifice for higher goals or delays in success.",
    13: "Rebirth, transformation, and regeneration.",
    14: "Karmic debt - lessons through misuse of freedom.",
    15: "Magnetic charm, success through creativity.",
    16: "Sudden changes, spiritual awakening after ego loss.",
    17: "Immortality through work or legacy.",
    18: "Material struggle, karmic lessons, and conflict.",
    19: "The Prince of Heaven - victory after trials.",
    20: "Awakening, judgment, and new beginnings.",
    21: "The Crown of Magi - success, wisdom, and power.",
    22: "Master builder, achievement through service.",
    23: "Royal Star of the Lion - great luck and protection.",
    24: "Love, family, and domestic peace.",
    25: "Wisdom gained through experience.",
    26: "Success mixed with responsibility or loss.",
    27: "Spiritual strength and humanitarian power.",
    28: "Fluctuating success, lessons in balance.",
    29: "Conflict and deception leading to growth.",
    30: "Creative self-expression, often through communication.",
    31: "Originality and strong individuality.",
    32: "Communication and persuasion lead to success.",
    33: "Master teacher - compassion and inspiration.",
    35: "Change and travel leading to self-discovery.",
}

class NameInput(BaseModel):
    full_name: str

def reduce_to_single(num: int):
    if num in [11, 22, 33]:
        return num
    while num > 9:
        num = sum(int(digit) for digit in str(num))
    return num

@router.post("/name-analysis")
def name_analysis(data: NameInput):
    name = data.full_name.upper().replace(" ", "")
    total_value = sum(CHALDEAN_TABLE.get(ch, 0) for ch in name)

    compound = total_value
    single = reduce_to_single(compound)

    compound_meaning = COMPOUND_MEANINGS.get(compound, "Unique vibration – not in standard compound list.")
    single_meaning = SINGLE_MEANINGS.get(single, "No single-digit meaning found.")

    return {
        "full_name": data.full_name,
        "compound_number": compound,
        "compound_meaning": compound_meaning,
        "single_number": single,
        "single_meaning": single_meaning,
        "summary": f"{data.full_name} vibrates to compound {compound} ({compound_meaning}), reducing to {single} ({single_meaning})."
    }