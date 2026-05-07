from dataclasses import dataclass
from typing import Dict, Any
import sympy as sp

@dataclass
class IntegralResult:
    integral: sp.Expr
    report: Dict[str, Any]