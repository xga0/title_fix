#!/usr/bin/env bash
# Start script for Render deployment

# Start the FastAPI server
cd backend
uvicorn main:app --host 0.0.0.0 --port $PORT 