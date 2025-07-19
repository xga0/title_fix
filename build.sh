#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # exit on error

echo "Starting build process..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r backend/requirements.txt

# Install the title_fix package in development mode
echo "Installing title_fix package..."
pip install -e .

# Install Node.js dependencies and build React app
echo "Installing Node.js dependencies..."
cd frontend
npm ci

echo "Building React app..."
npm run build

echo "Build completed successfully!" 