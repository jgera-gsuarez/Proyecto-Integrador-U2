import matplotlib.pyplot as plt

def setup_standard_figure(title: str, xlabel: str, ylabel: str):
    """Configuración estética común para cualquier gráfica del proyecto."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, which='both', linestyle='--', alpha=0.7)
    return fig, ax

def save_plot_to_file(fig, filename: str):
    """Utilidad común para exportar resultados."""
    fig.savefig(filename, dpi=300)
    print(f"Gráfica guardada en: {filename}")