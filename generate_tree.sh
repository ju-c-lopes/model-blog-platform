#!/usr/bin/env bash

echo "# Project Structure (generated)"  > tree.txt
echo "" >> tree.txt

tree -a -I '.ruff_cache|z_*.html|.git|.venv|__pycache__|.pytest_cache|.vscode|.crossnote|*.code-workspace|tests' >> tree.txt
