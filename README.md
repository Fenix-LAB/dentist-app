# Aplicacion de escritorio para herramienta de Dentistas
## Descripción
Aplicación de escritorio para la...

## Requisitos
- Python 3.10
- Qt Designer

## Instalación
1. Clonar el repositorio (o descargarlo)
2. Crear un entorno virtual:
```bash
python -m venv venv
```
3. Activar el entorno virtual:
```bash
source venv/Scripts/activate
```
4. Instalar las dependencias:
```bash
pip install -r requirements.txt
```
5. Ejecutar la aplicación:
```bash
python app.py
```

## Crear .py a partir de .ui
1. Crear el archivo .py a partir del .ui:
```bash
pyuic6 -x archivo.ui -o archivo.py
# Para este caso:
pyuic5 -x GUI.ui -o gui_design.py
``` 