# run.py

import sys
import subprocess

def run_backend():
    subprocess.Popen(["python", "backend/app.py"])

def run_frontend():
    subprocess.Popen(["python", "frontend/app.py"])

if __name__ == "__main__":
    if len(sys.argv) == 1:
        run_backend()
        run_frontend()
    elif len(sys.argv) == 2:
        if sys.argv[1] == "backend":
            run_backend()
        elif sys.argv[1] == "frontend":
            run_frontend()
        else:
            print("Invalid argument. Use 'backend' or 'frontend'.")
            sys.exit(1)
    else:
        print("Usage: python run.py [backend|frontend]")
        sys.exit(1)
