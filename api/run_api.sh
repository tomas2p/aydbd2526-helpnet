#!/bin/bash
source venv/bin/activate # Activar el entorno virtual

# Verificar si se deben instalar las dependencias
if [ "$1" == "install" ]; then
  if pip freeze | grep -q -f requirements.txt; then 
    echo "Las dependencias ya están instaladas." 
  else
    pip install -r requirements.txt # Instalar dependencias
  fi
  exit 0
fi

# Verificar si se debe ejecutar en modo prueba o iniciar la aplicación
if [ "$1" == "test" ]; then 
  shift # Eliminar el primer argumento "test"
  if [ $# -eq 0 ]; then
    pytest tests -v # Sin argumentos adicionales, ejecutar todos los tests
  else
    pytest "$@" # Con argumentos adicionales, pasarlos a pytest
  fi
else
  uvicorn app.main:app --reload --port 8000 # Iniciar la aplicación FastAPI
fi