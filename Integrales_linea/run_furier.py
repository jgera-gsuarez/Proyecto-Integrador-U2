from Integrales_linea.fourier.engine import compute_fourier, format_fourier_report
from Integrales_linea.fourier.plotter import plot_fourier_basic

def main():
    res = compute_fourier(
        input_spec={"type": "expr", "expr": "x"},
        interval={"a": "-pi", "b": "pi"},
        N=10,
        method="auto",
        samples=1000
    )

    print(format_fourier_report(res))

    if res.status == "ok":
        plot_fourier_basic(res.plot_data, title="Prueba Fourier: f(x)=x en [-pi, pi]")

if __name__ == "__main__":
    main()