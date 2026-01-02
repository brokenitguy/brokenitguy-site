import time
import subprocess
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- CONFIGURATION ---
# The file we are watching
WATCH_FILE = "what i am doing.txt"
# The script we run when that file changes
SCRIPT_TO_RUN = "update.py"
# ---------------------

class LogHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_modified = 0

    def on_modified(self, event):
        # Only care if the specific file we want is modified
        if event.src_path.endswith(WATCH_FILE):
            # Debounce: Editors sometimes trigger 'modify' twice instantly.
            # This ensures we only run once every 2 seconds.
            current_time = time.time()
            if current_time - self.last_modified > 2:
                print(f"\n[DETECTED] Change in {WATCH_FILE}...")
                print("[ACTION] Triggering update sequence...")
                
                # Run the main update script
                try:
                    subprocess.run(["python3", SCRIPT_TO_RUN], check=True)
                    print("[SUCCESS] Site updated and pushed.")
                    print("------------------------------------------------")
                    print(f"Watching {WATCH_FILE} for changes... (Press Ctrl+C to stop)")
                except Exception as e:
                    print(f"[ERROR] Script failed: {e}")
                
                self.last_modified = current_time

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print("------------------------------------------------")
    print("   BROKENITGUY AUTO-WATCHER ACTIVATED")
    print("------------------------------------------------")
    print(f"Target: {WATCH_FILE}")
    print("Status: Listening...")

    event_handler = LogHandler()
    observer = Observer()
    observer.schedule(event_handler, path=current_dir, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()