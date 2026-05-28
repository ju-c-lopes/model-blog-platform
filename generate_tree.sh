#!/usr/bin/env bash

echo "# Project Structure (generated)"  > tree.txt
echo "" >> tree.txt

tree -a -I 'reports|*coverage*|htmlcov|.ruff_cache|z_*.html|.git|.venv|__pycache__|.pytest_cache|.vscode|.crossnote|*.code-workspace|tests|*bkp*|__init__.py' >> tree.txt
