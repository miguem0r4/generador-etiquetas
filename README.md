# Generador de Etiquetas

![Build](https://github.com/miguem0r4/generador-etiquetas/actions/workflows/build.yml/badge.svg)
[![Download](https://img.shields.io/github/v/release/miguem0r4/generador-etiquetas)](https://github.com/miguem0r4/generador-etiquetas/releases/latest)

Procesamiento de PDFs con datos desde Excel: extracción de imágenes, división de PDFs e inserción de overlays.

## Descargar ejecutable (recomendado)

**No requiere Python ni instalar nada.** Solo descargar y ejecutar.

1. Ir a [Releases](https://github.com/miguem0r4/generador-etiquetas/releases/latest)
2. Descargar:
   - **Windows**: `GeneradorEtiquetas.exe`
   - **Linux**: `GeneradorEtiquetas` (dar permisos: `chmod +x GeneradorEtiquetas`)
3. Ejecutar el archivo descargado

## Cómo usar

| Pestaña | Qué hace |
|---|---|
| **Extraer Imágenes** | Recorta la esquina superior derecha de cada página del PDF y guarda cada recorte como PNG con el nombre indicado en el Excel |
| **Dividir PDF** | Agrupa páginas del PDF de a pares y guarda cada par como un PDF independiente nombrado desde el Excel |
| **Insertar Overlays** | Superpone una imagen en la primera página de cada par del PDF |

Pasos:
1. Abrir el programa
2. Seleccionar pestaña según lo que necesites
3. Click **"Examinar"** para elegir PDF, Excel y carpeta de salida
4. Ajustar parámetros si es necesario
5. Click **"Ejecutar"**

## Archivo de ejemplo

En el repositorio incluimos [`ejemplo_nombres.xlsx`](ejemplo_nombres.xlsx) con nombres de muestra para probar el programa. El Excel debe tener los nombres en la columna A, sin encabezado (el programa ignora la primera fila si es texto).

## Si querés correr desde el código fuente

```bash
git clone https://github.com/miguem0r4/generador-etiquetas.git
cd generador-etiquetas
pip install -r requirements.txt
python main.py
```

También funciona por línea de comandos:

```bash
python main.py --cli --mode extract --pdf documento.pdf --excel nombres.xlsx --output ./salida
python main.py --cli --mode split   --pdf documento.pdf --excel nombres.xlsx --output ./salida
python main.py --cli --mode overlay --pdf documento.pdf --excel nombres.xlsx --images ./imagenes --output ./salida
```

## Configuración

La configuración se guarda en `~/.config/etiquetas/config.yaml` y se edita desde el botón **Configuración** de la GUI.
