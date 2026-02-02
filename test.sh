#!/bin/bash

# Chạy pytest với coverage cho app/services và tạo báo cáo HTML
python3 -m pytest --cov=app/services --cov-report=html --cov-report=term tests/
