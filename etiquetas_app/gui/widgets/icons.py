import base64
import io

import customtkinter as ctk
from PIL import Image

_GITHUB_ICON_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAABb0lEQVR4nN2VsUsCYRiHH4+gc7EcqzVLLbW"
    "ppaE/wZSgEP+HQCgKIgIHwaH/oyFCHJIUsiCVKzQT9MTWCiMd0rbEBlG6q7T0XPzBLe+9PM/33d33Hgw5OnVh"
    "1mJvDgJ8KNwrmIKW8J8Ywm83tJIIWsPVEqFX46AZQYEgCHg9m4ROjsmlJXJpiXgswlEw0OmRcxlK+SxG42SnFo9F"
    "KOWz2BYXFLwxtSDgP8TtcnIRv2LLt81rpYLdZsPr2ehrBwqBxTyP2+XkrVbDt7NLvf4OQCKZIpFMDS5YctgBkOVi"
    "B94t0vVlzx7FO9DpWqe8+eVUlPLZztVeQDvLK6uYrA5MVgePT8+9BZm7LABm8xx6vR4Ak9WBdHPbc6V/2kFBLnIa"
    "CjNhMBAM+JmZnkIUxxFFsW/Bt69ob/+Aglxk3b1G9CzMR6NBtVIlch6lXH75t0AHw5lF0BrdIzgqhiJQ/+a0SJsp"
    "qAtawhUCrSTDeBpd8wkQnIMgyO2vfAAAAABJRU5ErkJggg=="
)


def github_icon(size: int = 20) -> ctk.CTkImage:
    buf = io.BytesIO(base64.b64decode(_GITHUB_ICON_B64))
    img = Image.open(buf)
    img = img.resize((size, size), Image.LANCZOS)
    return ctk.CTkImage(img, size=(size, size))
