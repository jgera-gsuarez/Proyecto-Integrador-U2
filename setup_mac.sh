#!/bin/bash
echo "--- Configurando Proyecto de Fourier e Integrales (macOS) ---"
# Crear entorno virtual si no existe
python3 -m venv venv
# Activar e instalar
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "------------------------------------------------------------"
echo "¡Instalación completa! Para ejecutar el programa escribe:"
echo "source venv/bin/activate && python main.py"
echo "------------------------------------------------------------"