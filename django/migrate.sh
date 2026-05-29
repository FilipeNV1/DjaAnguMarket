#!/bin/bash

# Check if Django model is valid
echo "Checking Django models..."
python3 manage.py check

# Check if the previous command was successful
if [ $? -eq 0 ]; then
    echo "Models are valid. Proceeding with migrations..."

    # Clean migrations directory (keep only __init__.py)
    echo "Cleaning app/migrations directory..."
    find app/migrations -type f ! -name '__init__.py' -delete
    find app/migrations -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null

    # Create migrations
    echo "Creating migrations for app..."
    python3 manage.py makemigrations app

    # Export SQL to txt file
    echo "Exporting SQL to sql.txt..."
    python3 manage.py sqlmigrate app 0001 > sql.txt

    # Apply migrations to database
    echo "Applying migrations to database..."
    python3 manage.py migrate

    echo "Migration process completed successfully!"
else
    echo "Model validation failed. Please fix the errors before running migrations."
    exit 1
fi