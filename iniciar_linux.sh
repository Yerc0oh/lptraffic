#!/usr/bin/env bash
set -eu
cd "$(dirname "$0")"
PYTHON=python3.11
command -v "$PYTHON" >/dev/null || { echo 'Instale Python 3.11.'; exit 1; }
[ -d venv ] || "$PYTHON" -m venv venv
source venv/bin/activate
if [ ! -f venv/.dependencies_ok ] || [ requirements.txt -nt venv/.dependencies_ok ]; then
  python -m pip install -r requirements.txt && touch venv/.dependencies_ok || { echo 'No se pudieron instalar las dependencias.'; exit 1; }
fi
python -m streamlit run app.py
