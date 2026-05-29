#!/bin/bash

# Generate a random Django secret key
SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")

# Create .env file
cat > .env << EOF
SECRET_KEY='$SECRET_KEY'
DEBUG=True
EOF

echo ".env file created successfully"