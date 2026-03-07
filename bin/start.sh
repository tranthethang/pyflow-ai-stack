#!/bin/bash
# Start the application
cd "$(dirname "$0")/.."
source .venv/bin/activate &&
python -m examples.web_api_usage
