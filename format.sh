#!/bin/bash
# Format code using black and isort
source .venv/bin/activate &&

black .

isort .
