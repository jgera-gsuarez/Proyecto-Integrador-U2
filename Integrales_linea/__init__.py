# utilidades compartidas
#from .core.parsing import parse_sympy_expr, parse_complex_math,parse_expr_math, parse_number_math
from .core.report import format_report#, format_kv_block
from .core.types import FourierResult
# integrales complejas
from .integrals.contours import CircleContour, PolygonContour
from .integrals.engine import integrate_by_residues  # y luego integrate() si lo agregas

# (opcional) exportar Fourier después
# from .fourier.engine import fourier_series, ...

from .core.parsing import parse_expr_math, parse_number_math

from .integrals.param_integrator import integrate_parametric, param_segment, param_arc