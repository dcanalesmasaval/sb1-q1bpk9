#!/bin/bash
set -e

# Install frontend dependencies
npm install

# Build frontend
npm run build

# Install backend dependencies
pip install -r requirements.txt

echo "Build completed successfully!"