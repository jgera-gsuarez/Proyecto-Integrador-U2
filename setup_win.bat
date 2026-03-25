@echo off
echo --- Configurando Proyecto de Fourier e Integrales (Windows) ---
:: Crear entorno virtual
python -m venv venv
:: Activar e instalar dependencias
call venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
echo ------------------------------------------------------------
echo ¡Instalación completa! Para ejecutar el programa usa:
echo venv\Scripts\activate ^&^& python main.py
echo ------------------------------------------------------------
pause