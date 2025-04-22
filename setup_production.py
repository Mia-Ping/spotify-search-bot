import os

# Create necessary directories at runtime, not during build
# This ensures the disk is properly mounted and writable

# Ensure directories exist
os.makedirs('/data/flask_session', exist_ok=True)
os.makedirs('/data/uploads', exist_ok=True)

# Update file paths in app.py for production
with open('app.py', 'r') as file:
    content = file.read()

# Replace session directory path
content = content.replace(
    "app.config['SESSION_FILE_DIR'] = './.flask_session/'", 
    "app.config['SESSION_FILE_DIR'] = '/data/flask_session/'"
)

# Replace upload folder path
content = content.replace(
    "app.config['UPLOAD_FOLDER'] = './uploads'", 
    "app.config['UPLOAD_FOLDER'] = '/data/uploads'"
)

# Write the updated content back to app.py
with open('app.py', 'w') as file:
    file.write(content)

print("Production environment setup complete!")
