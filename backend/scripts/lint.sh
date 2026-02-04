#!/bin/bash
# Script to run linting and type checking

# Navigate to backend directory if running from root
if [ -d "backend" ]; then
    cd backend
fi

echo "🔍 Running Ruff (Linter)..."
ruff check .

echo -e "\n🔍 Running Mypy (Type Checker)..."
mypy .

echo -e "\n✅ Linting complete!"
