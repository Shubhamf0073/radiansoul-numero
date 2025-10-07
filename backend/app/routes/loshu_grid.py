# app/routes/loshu_grid.py

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime

router = APIRouter(prefix="/loshu-grid", tags=["Lo Shu Grid"])

# ------------------ MODELS ------------------

class LoShuRequest(BaseModel):
    date_of_birth: str
    include_zero: Optional[bool] = False
    include_kua: Optional[bool] = False
    gender: Optional[str] = None

# ------------------ HELPERS ------------------

def reduce_to_single_digit(num: int) -> int:
    """Reduce number to a single digit."""
    while num > 9:
        num = sum(int(d) for d in str(num))
    return num

def extract_digits(dob: str, include_zero: bool) -> List[int]:
    """Extract digits from DOB."""
    digits = [int(c) for c in dob if c.isdigit()]
    if not include_zero:
        digits = [d for d in digits if d != 0]
    return digits

def calculate_mulank(day: int) -> int:
    """Calculate Mūlank (root of birth day)."""
    return reduce_to_single_digit(day)

def calculate_bhagyank(dob: str) -> int:
    """Calculate Bhāgyank (root of full DOB sum)."""
    digits = [int(c) for c in dob if c.isdigit()]
    return reduce_to_single_digit(sum(digits))

def calculate_kua_number(year: int, gender: str) -> int:
    """Calculate Kua number."""
    last_two = year % 100
    base = reduce_to_single_digit(last_two)
    gender = gender.lower()

    if year >= 2000:
        kua = 9 - base if gender == "male" else base + 6
    else:
        kua = 10 - base if gender == "male" else base + 5

    return reduce_to_single_digit(kua)

# ------------------ INTERPRETATIONS ------------------

INTERPRETATIONS = {
    "mental_plane": {
        "strong": "Strong imagination and logical abilities.",
        "weak": "Needs focus and consistency in thought."
    },
    "emotional_plane": {
        "strong": "Emotionally expressive and caring.",
        "weak": "Emotionally detached or overly sensitive."
    },
    "physical_plane": {
        "strong": "Organized and dependable.",
        "weak": "May struggle with discipline or planning."
    }
}

# ------------------ MAIN ROUTE ------------------

@router.post("/")
def calculate_loshu_grid(req: LoShuRequest) -> Dict[str, Any]:
    dob_raw = req.date_of_birth.strip()
    include_zero = getattr(req, "include_zero", False)

    # Parse date
    try:
        dob_parsed = datetime.strptime(dob_raw, "%d-%m-%Y")
    except ValueError:
        try:
            dob_parsed = datetime.strptime(dob_raw, "%Y-%m-%d")
        except ValueError:
            return {"error": "Invalid date format. Use DD-MM-YYYY or YYYY-MM-DD."}

    day = dob_parsed.day
    year = dob_parsed.year

    # Core numbers
    mulank = calculate_mulank(day)
    bhagyank = calculate_bhagyank(dob_raw)

    # Base digits from DOB
    digits = extract_digits(dob_raw, include_zero)

    # Create separate lists for logic vs display
    digits_for_counts = digits + [mulank, bhagyank]  # used for interpretation logic
    digits_for_grid = digits  # used for the actual grid

    # Counts for logic (includes mulank & bhagyank)
    counts = {str(i): 0 for i in range(1, 10)}
    for d in digits_for_counts:
        if 1 <= d <= 9:
            counts[str(d)] += 1

    # Counts for the visual grid (only DOB digits)
    grid_counts = {str(i): 0 for i in range(1, 10)}
    for d in digits_for_grid:
        if 1 <= d <= 9:
            grid_counts[str(d)] += 1

    # Visual Lo Shu layout (Chaldean grid style, with actual digits)
    def digit_str(n, count):
        return str(n) * count if count > 0 else ""

    visual_grid = [
        ["", "", digit_str(2, counts["2"])],       # top row
        ["", digit_str(5, counts["5"]), ""],       # middle row
        ["", digit_str(1, counts["1"]), digit_str(6, counts["6"])]  # bottom row
    ]

    # Prepare lo_shu_grid dict for frontend display
    lo_shu_grid = {str(i): grid_counts[str(i)] for i in range(1, 10)}
    # ✅ Define kua_number safely
    kua_number = None

    # Insert Kua in center (optional)
    if req.include_kua:
        if not req.gender:
            return {"error": "Gender is required when include_kua=True."}
        kua_number = calculate_kua_number(year, req.gender)
        visual_grid[1][1] = kua_number

    # Missing and repeated
    missing_numbers = [i for i in range(1, 10) if counts[str(i)] == 0]
    repeated_numbers = {i: counts[str(i)] for i in range(1, 10) if counts[str(i)] > 1}

    # Arrows
    arrows = {
        "top_row_4_9_2": all(counts[str(n)] > 0 for n in [4, 9, 2]),
        "middle_row_3_5_7": all(counts[str(n)] > 0 for n in [3, 5, 7]),
        "bottom_row_8_1_6": all(counts[str(n)] > 0 for n in [8, 1, 6]),
        "left_col_4_3_8": all(counts[str(n)] > 0 for n in [4, 3, 8]),
        "center_col_9_5_1": all(counts[str(n)] > 0 for n in [9, 5, 1]),
        "right_col_2_7_6": all(counts[str(n)] > 0 for n in [2, 7, 6]),
    }

    # Plane strengths
    mental = "strong" if any(counts[str(n)] > 0 for n in [3, 6, 9]) else "weak"
    emotional = "strong" if any(counts[str(n)] > 0 for n in [2, 5, 8]) else "weak"
    physical = "strong" if any(counts[str(n)] > 0 for n in [1, 4, 7]) else "weak"

    interpretation = {
        "mental_plane": INTERPRETATIONS["mental_plane"][mental],
        "emotional_plane": INTERPRETATIONS["emotional_plane"][emotional],
        "physical_plane": INTERPRETATIONS["physical_plane"][physical],
    }

    return {
        "date_of_birth": dob_raw,
        "mulank": mulank,
        "bhagyank": bhagyank,
        "kua_number": kua_number,
        "gender": req.gender if req.include_kua else None,
        "digits_used": digits,
        "counts": counts,
        "visual_grid": visual_grid,
        "missing_numbers": missing_numbers,
        "repeated_numbers": repeated_numbers,
        "arrows": arrows,
        "interpretation": interpretation,
        "lo_shu_grid": lo_shu_grid,
    }
