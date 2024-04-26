import sys
import subprocess
import signal

backend_process = None
frontend_process = None

def run_backend():
    global backend_process
    backend_process = subprocess.Popen(["python", "backend/app.py"])
    # Note: If you are using macOS, you may need to change "python" to "python3.xx" depending on your Python version.

def run_frontend():
    global frontend_process
    frontend_process = subprocess.Popen(["python", "frontend/app.py"])
    # Note: If you are using macOS, you may need to change "python" to "python3.xx" depending on your Python version.

def terminate_processes():
    global backend_process, frontend_process
    if backend_process:
        backend_process.terminate()
    if frontend_process:
        frontend_process.terminate()

def signal_handler(sig, frame):
    print("Ctrl+C pressed, terminating processes...")
    terminate_processes()
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

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

    try:
        while True:
            pass  # Keep the main thread alive
    except KeyboardInterrupt:
        print("\nCtrl+C pressed, terminating processes...")
        terminate_processes()