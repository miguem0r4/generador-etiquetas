 
import fitz # PyMuPDF
import pandas as pd
from PIL import Image
import os
 
# ==============================
# 📄 RUTAS (EDITA ESTO)
# ==============================
 
pdf_path = r"C:\Users\USER\Downloads\PDFETIQUETAS.pdf"
excel_path = r"C:\Users\USER\Downloads\LISTAEE.xlsx"
 
# Carpeta Descargas\ETIQUETAS
downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
output_folder = os.path.join(downloads_path, "ETIQUETAS")
 
# Crear carpeta si no existe
os.makedirs(output_folder, exist_ok=True)
 
# ==============================
# 📊 LEER EXCEL
# ==============================
 
df = pd.read_excel(excel_path, header=None)
nombres = df.iloc[:, 0].dropna().tolist()
 
# ==============================
# 📕 ABRIR PDF
# ==============================
 
doc = fitz.open(pdf_path)
 
# Validación
if len(nombres) < len(doc):
    print("⚠️ Hay menos nombres que páginas en el PDF")
elif len(nombres) > len(doc):
    print("⚠️ Hay más nombres que páginas en el PDF")
 
# ==============================
# 🔄 PROCESAMIENTO
# ==============================
 
for i in range(len(doc)):
    page = doc[i]
 
    # 🔥 Mejor calidad
    mat = fitz.Matrix(3, 3)
    pix = page.get_pixmap(matrix=mat)
 
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
 
    width, height = img.size
 
    # ✂️ Recorte PROPORCIONAL (esquina superior derecha)
    crop_area = (
        int(width * 0.64), # derecha
        0, # arriba
        width,
        int(height * 0.13) # altura
    )
 
    cropped = img.crop(crop_area)
 
    # Nombre desde Excel
    try:
        nombre = str(nombres[i])
    except IndexError:
        nombre = f"pagina_{i+1}"
 
    # Limpiar nombre
    nombre = nombre.replace("/", "_").replace("\\", "_")
 
    # Guardar imagen
    output_path = os.path.join(output_folder, f"{nombre}.png")
    cropped.save(output_path)
 
    print(f"✅ Guardado: {output_path}")
 
doc.close()
 
print("\n🎉 Proceso terminado con éxito")
 
división pdf
 
import os
from PyPDF2 import PdfReader, PdfWriter
import pandas as pd
 
# Rutas
pdf_path = r"C:\Users\USER\Downloads\combinacion.pdf"
excel_path = r"C:\Users\USER\Downloads\LISTAEE.xlsx"
 
# Carpeta de salida
output_folder = r"C:\Users\USER\Downloads\radicados"
os.makedirs(output_folder, exist_ok=True)
 
# Leer Excel (columna A)
df = pd.read_excel(excel_path, header=None)
nombres = df[0].dropna().tolist()
 
# Leer PDF
reader = PdfReader(pdf_path)
total_paginas = len(reader.pages)
 
# Validación básica
if total_paginas // 2 > len(nombres):
    print("⚠️ No hay suficientes nombres en el Excel para todas las páginas.")
 
# Procesar de 2 en 2
indice_nombre = 0
 
for i in range(0, total_paginas, 2):
    writer = PdfWriter()
 
    # Agregar página i
    writer.add_page(reader.pages[i])
 
    # Agregar página i+1 si existe
    if i + 1 < total_paginas:
        writer.add_page(reader.pages[i + 1])
 
    # Nombre del archivo desde Excel
    if indice_nombre < len(nombres):
        nombre_archivo = str(nombres[indice_nombre])
    else:
        nombre_archivo = f"archivo_{indice_nombre+1}"
 
    output_path = os.path.join(output_folder, f"{nombre_archivo}.pdf")
 
    # Guardar PDF
    with open(output_path, "wb") as f:
        writer.write(f)
 
    indice_nombre += 1
 
print("✅ Proceso completado. PDFs generados en la carpeta 'radicados'.")
 
insertar etiquetas en pdf
 
import os
import pandas as pd
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
 
# Rutas
pdf_path = r"C:\Users\USER\Downloads\combinacion.pdf"
excel_path = r"C:\Users\USER\Downloads\LISTAEE.xlsx"
imagenes_folder = r"C:\Users\USER\Downloads\IMAGENES ETIQUETAS"
 
output_folder = r"C:\Users\USER\Downloads\radicadostest2"
os.makedirs(output_folder, exist_ok=True)
 
# Leer Excel
df = pd.read_excel(excel_path, header=None)
nombres = df[0].dropna().tolist()
 
# Leer PDF
reader = PdfReader(pdf_path)
total_paginas = len(reader.pages)
 
def crear_overlay(imagen_path, page_width, page_height):
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(page_width, page_height))
 
    # 🔥 Tamaño (ajústalo si quieres)
    scale = 2
    img_width = 100 * scale
    img_height = 50 * scale
 
    # Posición (arriba derecha)
    x = page_width - img_width - 10
    y = page_height - img_height - 10
 
    c.drawImage(ImageReader(imagen_path), x, y, width=img_width, height=img_height)
    c.save()
 
    packet.seek(0)
    return PdfReader(packet)
 
indice_nombre = 0
 
# 🔥 recorrer PDF de 2 en 2
for i in range(0, total_paginas, 2):
 
    if indice_nombre >= len(nombres):
        print("⚠️ No hay más nombres en el Excel")
        break
 
    writer = PdfWriter()
 
    nombre_archivo = str(nombres[indice_nombre]).strip()
    imagen_path = os.path.join(imagenes_folder, f"{nombre_archivo}.png")
   
      # ⚠️ Validar si existe
    if not os.path.exists(imagen_path):
        print(f"⚠️ No se encontró imagen para: {nombre_archivo}")
        indice_nombre += 1
        continue
 
    for j in range(2):
        if i + j < total_paginas:
            page = reader.pages[i + j]
 
            # ✅ SOLO en la primera página del bloque
            if j == 0 and os.path.exists(imagen_path):
                overlay_pdf = crear_overlay(
                    imagen_path,
                    float(page.mediabox.width),
                    float(page.mediabox.height)
                )
                page.merge_page(overlay_pdf.pages[0])
 
            writer.add_page(page)
 
    # Guardar PDF
    output_path = os.path.join(output_folder, f"{nombre_archivo}.pdf")
 
    with open(output_path, "wb") as f:
        writer.write(f)
 
    print(f"✅ Creado: {nombre_archivo}.pdf")
 
    indice_nombre += 1
 
print("🔥 Proceso completado")
