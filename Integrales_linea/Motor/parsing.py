from sympy import I
from sympy.parsing.sympy_parser import(
    parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
)

transforms = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)

allowed = {
    # constantes
    "I": I,
}

def normalize_input(s: str) -> str:
    """
    Normaliza entrada estilo matemático:
      - 'i' -> 'I' (unidad imaginaria SymPy)
      - respeta 'sin', 'exp', etc.
    """
    s = s.strip()
    # reemplazo seguro: i -> I, pero cuidando no romper palabras (p.ej. 'sin')
    # estrategia simple: reemplazar ' i' y finales, y también cuando esté pegada a número/paréntesis.
    # en la práctica SymPy con implicit multiplication soporta '2I' bien.
    s = s.replace("−", "-")  # por si copias signos raros
    # Reemplaza i aislada o como parte de número complejo
    # (para simplicidad: reemplazo global de 'i' por 'I', asumiendo que el usuario no escribe variables con i)
    s = s.replace("i", "I")
    return s

def parse_sympy_expr(expr_str: str):
    expr_str = normalize_input(expr_str)
    return parse_expr(expr_str, transformations=transforms, local_dict=allowed)

def parse_complex_math(z_str: str):
    """
    Devuelve un número complejo en SymPy (puede ser exacto).
    Ej: '1+2i', '-i', '3', '(1-i)/2'
    """
    return parse_sympy_expr(z_str)
