from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

import sys, os
print("CWD:", os.getcwd())
print("sys.path:", sys.path)
