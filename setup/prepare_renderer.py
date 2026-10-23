"""Adapt the renderer build inside the image to its Python and system OSMesa."""
from pathlib import Path

path = Path('/opt/epos-renderer/CMakeLists.txt')
text = path.read_text()
start = text.index('# Python library')
end = text.index('# Others.')
text = text[:start] + '''# Discover the container's Python and system OSMesa.
find_package(PythonLibs REQUIRED)
find_package(pybind11 CONFIG REQUIRED)
find_library(OSMESA_LIBRARIES OSMesa REQUIRED)
''' + text[end:]
path.write_text(text)
