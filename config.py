import os

# Base directory for the application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Uploads directories
UPLOAD_FOLDER_CVS = os.path.join(BASE_DIR, 'uploads', 'cvs')
UPLOAD_FOLDER_JDS = os.path.join(BASE_DIR, 'uploads', 'jds')

# Ensure upload directories exist
os.makedirs(UPLOAD_FOLDER_CVS, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_JDS, exist_ok=True)

# Database configuration (SQLite or JSON)
DATABASE_URI = os.path.join(BASE_DIR, 'database', 'data.db')  # For SQLite
# DATABASE_URI = os.path.join(BASE_DIR, 'database', 'data.json')  # For JSON (if using JSON-based storage)

# Allowed file extensions for CVs and JDs
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

# Maximum file size in bytes (e.g., 10MB)
MAX_CONTENT_LENGTH = 10 * 1024 * 1024

# Matching Algorithm settings
SIMILARITY_THRESHOLD = 0.5  # Adjust as needed (Threshold for considering a match)

# Application secret key (for security and sessions)
SECRET_KEY = os.urandom(24)

# Define other app settings here as needed
