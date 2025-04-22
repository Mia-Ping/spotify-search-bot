#!/bin/bash

# Update app.py to use the correct paths for production
sed -i 's|app.config\['\''SESSION_FILE_DIR'\''\] = '\''./.flask_session/'\''|app.config\['\''SESSION_FILE_DIR'\''\] = '\''/data/flask_session/'\''|g' app.py
sed -i 's|app.config\['\''UPLOAD_FOLDER'\''\] = '\''./uploads'\''|app.config\['\''UPLOAD_FOLDER'\''\] = '\''/data/uploads/'\''|g' app.py

# Create necessary directories
mkdir -p /data/flask_session
mkdir -p /data/uploads

# Make sure permissions are correct
chmod -R 755 /data

# Start the application
exec gunicorn app:app
