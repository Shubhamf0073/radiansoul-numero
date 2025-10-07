# app/routes/profession_analysis_report.py

from fastapi import APIRouter
from pydantic import BaseModel
from app.routes.loshu_grid import calculate_loshu_grid as generate_lo_shu_grid
from app.routes.profession_analysis import (
    calculate_mulank,
    calculate_bhagyank,
    get_profession_suggestions
)

router = APIRouter(prefix="/profession-analysis-report", tags=["Profession Analysis Report"])


class NumerologyRequest(BaseModel):
    date_of_birth: str
    include_kua: bool = False
    gender: str | None = None


@router.post("/report")
def profession_analysis_report(req: NumerologyRequest):
    # Step 1: Generate Lo Shu Grid
    lo_shu_result = generate_lo_shu_grid(req)

    # Step 2: Extract numbers (those with counts > 0)
    lo_shu_numbers = [int(num) for num, count in lo_shu_result["counts"].items() if count > 0]

    # Step 3: Calculate PN and DN
    pn = calculate_mulank(req.date_of_birth)
    dn = calculate_bhagyank(req.date_of_birth)

    # Step 4: Run profession analysis with Lo Shu numbers
    profession_result = get_profession_suggestions(pn, dn, lo_shu_numbers)

    # Step 5: Combine results
    final_report = {
        "date_of_birth": req.date_of_birth,
        "lo_shu_grid": lo_shu_result["counts"],
        "missing_numbers": lo_shu_result["missing_numbers"],
        "repeated_numbers": lo_shu_result["repeated_numbers"],
        "interpretation": lo_shu_result["interpretation"],
        "profession_analysis": profession_result
    }

    return final_report