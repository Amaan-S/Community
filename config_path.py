import os
import sys

# Set BASE_DIR to the root of your project (taajj-group)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the project root, Directories, and Main to sys.path for easy imports
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'Directories'))
sys.path.insert(0, os.path.join(BASE_DIR, 'Main'))
