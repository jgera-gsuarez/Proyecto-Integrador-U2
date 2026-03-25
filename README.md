# Proyecto Integrador Unidad II
Este proyecto está completamente desarrollado con Python en PyCharm. Es una calculadora de integrales de línea y series de fourier, además de graficar las funciones. El reporte de los cálculos se puede exportar en un archivo .tex y se puede exportar ese archivo .tex para guardar el archivo PDF.

## Requisitos previos
Antes de empezar, debe tener:
  - **Pyhon 3.9 o superior** instalado
  - **Una distribución de LaTeX**(como MikTex en Windows o MacTex en macOS) si desea generar los reportes en PDF. El programa compila el archivo LaTeX con pdflatex de forma predetermianada.

## Guía de instalción
### Ejecución del proyecto
##### 1. Clonar el repositorio:
        
        git clone cd https://github.com/jgera-gsuarez/Proyecto-Integrador-U2 cd Proyecto-Integrador-U2
        
##### 2. Crear un entorno virtual (Recomendado):
Inicia con:

        python -m venv venv
        
  **En macOS/Linux:**
  
        source venv/bin/activate
        
  **En Windows:**
  
        venv\Scripts\activate
        
##### 3. Instalar dependencias:
Tu proyecto necesita librerías específicas.
  - sympy
  - mpmath
  - matplotlib (si usas gráficas)
El script para instalarlos automaticamente se encuentra en el archivo requirements.txt

    Para instalar ejecuta:
        
    pip install -r requirements.txt
        
##### 4. Correr el programa:
        
        python main.py
        
###### Nota para usuarios de MAC
*Si el programa no encuentra pdflatex, asegúrate de que el binario esté en tu PATH o configura la ruta manual en core/exporter.py.

## Instalación rápida
- En Mac ejecuta:
  
        sh setup_mac.sh
  
- En Windows haz doble clic en: **setup_windows.bat**
