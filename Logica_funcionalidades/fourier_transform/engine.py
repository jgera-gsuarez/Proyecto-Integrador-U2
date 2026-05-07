import sympy as sp

class TransformEngine:
    def __init__(self):
        # Definimos t (tiempo) y f (frecuencia) como símbolos base
        self.t = sp.symbols('t', real=True)
        self.f = sp.symbols('f', real=True)

    def compute_transform(self, parsed_expr: str):
        """
        Calcula la Transformada de Fourier simbólica:
        Integral de f(t) * exp(-2*pi*i*f*t) dt desde -inf hasta +inf
        """
        try:
            transformada = sp.fourier_transform(parsed_expr, self.t, self.f)

            if transformada is None:
                return "Error: SymPy no pudo encontrar una solución analítica."

            return sp.simplify(transformada)

        except Exception as e:
            return f"Error en el cálculo: {str(e)}"

    @staticmethod
    def get_magnitude_phase(transform_expr):
        """
        Extrae las expresiones simbólicas de Magnitud y Fase
        útiles para el archivo plotting.py de esta carpeta.
        """
        magnitude = sp.Abs(transform_expr)
        phase = sp.arg(transform_expr)
        return magnitude, phase