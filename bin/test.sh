#!/bin/bash
cd "$(dirname "$0")/.."
source .venv/bin/activate &&

# Chạy pytest với coverage cho pyflow_ai_stack và tạo báo cáo HTML
python -m pytest --cov=pyflow_ai_stack --cov-report=html --cov-report=term tests/
