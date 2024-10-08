#!/bin/bash
set -e

# Start the Flask application using Gunicorn
gunicorn --bind 0.0.0.0:$PORT app:app