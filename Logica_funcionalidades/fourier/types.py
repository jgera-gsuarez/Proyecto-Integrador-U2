from dataclasses import dataclass
from typing import Callable, Dict, Any, List, Optional
import sympy as sp

@dataclass
class FourierResult:
    status: str                      # "ok" o "error"
    message: str                     # detalle en caso de error

    # Configuración
    a: sp.Expr
    b: sp.Expr
    T: sp.Expr
    n_harmonics: int
    method_used: str                 # "symbolic" o "numeric"

    # Coeficientes
    a0: sp.Expr
    an: List[sp.Expr]                # n=1..N
    bn: List[sp.Expr]                # n=1..N

    # Reconstrucción (callable numérico)
    f_callable: Optional[Callable[[float], float]]
    s_callable: Optional[Callable[[float], float]]

    # Datos para plot (si los generas)
    plot_data: Optional[Dict[str, Any]]

    # Reporte estructurado (para formatear)
    report: Dict[str, Any]