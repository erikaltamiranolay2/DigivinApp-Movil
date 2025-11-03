#!/usr/bin/env bash
set -e

echo "🔍 Detectando versión de Python..."
PYVER=$(python3 -c "import sys; print(sys.version_info[:2])" 2>/dev/null || echo "N/A")

if [[ "$PYVER" == *"3, 12"* ]]; then
  echo "⚠️ Detectado Python 3.12: aplicando parche para pyjnius..."
else
  echo "✅ No estás usando Python 3.12, puedes compilar directamente."
  exit 0
fi

cd /workspaces/DigivinApp-Movil/digivin-app/mobile_app

# Fijar pyjnius a versión compatible
if grep -q "requirements" buildozer.spec; then
  sed -i 's/requirements *=.*/requirements = python3,kivy,pyjnius==1.5.0/' buildozer.spec
fi

# Forzar descarga del código actualizado
echo "🧹 Limpiando builds anteriores..."
buildozer android clean || true

# Buscar archivo jnius_utils.pxi y parcharlo
PXI_PATH=$(find .buildozer -type f -name "jnius_utils.pxi" | head -n 1 || true)
if [ -f "$PXI_PATH" ]; then
  echo "🔧 Parchando $PXI_PATH ..."
  sed -i 's/isinstance(arg, long)/isinstance(arg, int)/g' "$PXI_PATH"
  echo "✅ Parche aplicado."
else
  echo "⚠️ No se encontró jnius_utils.pxi aún. Se aplicará automáticamente en la próxima compilación."
fi

echo "🚀 Reconstruyendo la app..."
buildozer -v android debug || true

echo "✅ Proceso completado. Si el build sigue fallando, intenta usar Python 3.11."
