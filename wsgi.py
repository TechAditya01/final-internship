from app import create_app

app = create_app()
import sys, os
print("CWD:", os.getcwd())
print("sys.path:", sys.path)
