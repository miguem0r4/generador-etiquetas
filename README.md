# Generador de Etiquetas

Procesamiento de PDFs con datos desde Excel: extracción de imágenes, división de PDFs e inserción de overlays.

## Requisitos

- Python 3.10+
- pip

## Instalación

```bash
git clone <repo>
cd etiquetas
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
# .venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

## Uso

### Interfaz gráfica

```bash
python main.py
```

Tres pestañas:
- **Extraer Imágenes** — extrae recortes de cada página del PDF y los guarda como PNG nombrados desde el Excel
- **Dividir PDF** — agrupa páginas del PDF en pares y guarda cada grupo como PDF independiente
- **Insertar Overlays** — superpone una imagen (PNG) en la primera página de cada par del PDF

Todos los parámetros (ratios de recorte, escalas, offsets, etc.) se configuran desde la misma interfaz en cada pestaña, o globalmente desde el botón **Configuración**.

### Línea de comandos

```bash
# Extraer imágenes
python main.py --cli --mode extract --pdf documento.pdf --excel nombres.xlsx --output ./salida

# Dividir PDF en pares
python main.py --cli --mode split --pdf documento.pdf --excel nombres.xlsx --output ./salida

# Insertar overlays
python main.py --cli --mode overlay --pdf documento.pdf --excel nombres.xlsx --images ./imagenes --output ./salida

# Usar un archivo de configuración específico
python main.py --cli --mode extract --pdf in.pdf --excel in.xlsx --output ./out --config ./mi-config.yaml
```

### Ayuda

```bash
python main.py --help
```

## Estructura del proyecto

```
etiquetas/
├── main.py                        # Entry point (GUI | CLI)
├── config.yaml                    # Configuración por defecto
├── requirements.txt               # Dependencias
├── GeneradorEtiquetas.spec        # PyInstaller spec
└── etiquetas_app/
    ├── core/                      # Lógica de negocio
    │   ├── models.py              # Dataclasses configurables
    │   ├── excel_reader.py        # Lectura compartida de Excel
    │   ├── extract_images.py      # Extracción de imágenes
    │   ├── split_pdf.py           # División de PDF
    │   └── overlay_pdf.py         # Inserción de overlays
    ├── gui/                       # Interfaz gráfica (customtkinter)
    │   ├── app.py                 # Ventana principal
    │   ├── settings_dialog.py     # Diálogo de configuración
    │   ├── tabs/                  # Pestañas por funcionalidad
    │   └── widgets/               # Componentes reutilizables
    └── utils/
        ├── config.py              # Carga/guardado de config YAML
        └── validators.py          # Validación de rutas
```

## Configuración

La configuración se guarda en `~/.config/etiquetas/config.yaml` y se edita desde el botón **Configuración** de la GUI. También puede editarse manualmente:

```yaml
paths:
  default_output: ~/Downloads/ETIQUETAS
  images_folder: ~/Downloads/IMAGENES ETIQUETAS

extract:
  crop_left_ratio: 0.64
  crop_top_ratio: 0.0
  crop_right_ratio: 1.0
  crop_bottom_ratio: 0.13
  render_scale: 3

overlay:
  image_scale: 2
  image_width: 100
  image_height: 50
  offset_x: 10
  offset_y: 10

split:
  pages_per_group: 2

theme: dark
```

## Empaquetar como ejecutable

```bash
pip install pyinstaller
pyinstaller GeneradorEtiquetas.spec
```

El ejecutable se generará en `dist/GeneradorEtiquetas`.
