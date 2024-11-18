import os
import shutil

# Remove all __pycache__ directories in the current directory and its subdirectories

def remove_pycache():
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            print(f"Removing: {pycache_path}")
            shutil.rmtree(pycache_path)

if __name__ == '__main__':
    remove_pycache()
